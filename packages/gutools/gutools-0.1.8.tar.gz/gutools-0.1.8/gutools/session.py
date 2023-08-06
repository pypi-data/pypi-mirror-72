import asyncio
import os
import re
import time
import sys
import signal
import random
import glob
import shlex
import subprocess

import yaml
import ujson as json
import psutil
# import warnings
# warnings.simplefilter('always', DeprecationWarning)

from datetime import datetime
from logging import debug, info, warn, error
from functools import partial

# 3rd
from daemon import daemon, pidfile
from codenamize import codenamize

# mine
from aiopb.aiopb import Hub
from gutools.tools import build_uri, parse_uri, snake_case, \
    update_context, identity, yaml_encode, yaml_decode, wlikelyhood, \
    fileiter, copyfile, dset, load_config, save_config, expandpath, \
    _call, async_call, serializable_container, update_container_value, \
    walk, rebuild

from gutools.system import send_signals, SmartPIDLockFile, get_fingerprint, \
    compare_fingerprint, find_process, test_process, test_alive
from gutools.uobjects import UObject, kget, vget
from gutools.persistence import DB, DBWorkspace, FSLayout
from gutools.unet import TL
from gutools.bash_completer import hasheable_cmdline
from gutools.uapplication import UApplication  # TODO: needed?
from gutools.uagents import UAgent
from gutools.colors import *


class UProcess(UObject):
    __args__ = ('name', 'alias', 'uri', 'state',
                'pid', 'restart', 'shutdown', 'date')
    __kwargs__ = {}
    __slots__ = __args__ + tuple(set(__kwargs__).difference(__args__))


class SessionWorkspace(DBWorkspace):
    scheme = """
    CREATE TABLE IF NOT EXISTS {}
      (
      {},
      date DATETIME DEFAULT (datetime(CURRENT_TIMESTAMP, 'localtime')),
      PRIMARY KEY (name),
      UNIQUE (alias)
    );
    """.format(
        snake_case(UProcess.__name__),
        ','.join(UProcess.__slots__[:-1]),
       )


ext_decoder = {
    'yaml': yaml_decode,
    'json': json.decode,
    'pid': int,
    'out': identity,
    'err': identity,
}

ext_encoder = {
    'yaml': yaml_encode,
    'json': json.encode,
    'pid': str,
    'out': identity,
    'err': identity,
}

ext_aliases = {
    'fp': 'yaml',
}

for k, v in ext_aliases.items():
    ext_decoder[k] = ext_decoder[v]
    ext_encoder[k] = ext_encoder[v]


def daemonize(f):
    """Decorator for daemonized methods"""
    return f


ATTACHED_SCHEME = 'attached'


class USession(object):
    """Create a session workspace to store persistent information related to
    a process group.
    """
    WORKSPACE = SessionWorkspace  # Need to be overrided

    # file config
    default_config = {
        'copy': {
            'bin': 'bin/*.*',
            'out': '',
            'pid': '',
            'fp': '',
            'err': '',
        },
        'templates': {
            'scripts': 'bin/*.sh',
        },
        'dependences': {},
    }
    """Default configuration for a USession. Can be overrided."""

    def __init__(self, path):
        self.path = expandpath(path)
        self.layout = FSLayout(self.path)

        self.db_file = self.layout.get_path('db', 'session', touch=True)
        self.db = DB(self.db_file)
        self.workspace = self.WORKSPACE(self.db)
        self.config = self.layout.get_content('etc', 'session',
                                              default=self.default_config)

    def init(self):
        """Initialize the file structure, adding missing files from
        config['copy'] section.
        """
        info(f'Initialize structure in {self.path}')

        top = os.path.dirname(os.path.abspath(__file__))
        for name, pattern in self.config.get('copy', {}).items():
            self.layout.get_path('<folder>', name, touch=True)
            for path in fileiter(top, wildcard=pattern):
                where = os.path.join(self.path, path.split(top)[-1][1:])
                copyfile(path, where, override=False)

    def activate(self):
        """Activate Session Supervisor and optionally launch attached
        processes based on configuration.
        """
        scheme = self.__class__.__name__.lstrip('U').lower()
        uri = f"{scheme}://supervisor"
        self.start_daemon(target=self._supervisor, uri=uri, alias='supervisor')

    def deactivate(self):
        """Deactivate Session Supervisor and optionally attached processes
        based on configuration.
        """
        def get_candidates():
            for d, filename, pid in self.layout.iter_file_content('pid'):
                if test_alive(pid):
                    for process in self.workspace.find(UProcess, name=d['name'], shutdown=1):
                        # assert pid == process.pid
                        yield d['name'], pid

        def done(name):
            print(f' {RED}{name}\t\t[done]{RESET}')

        # signals = [signal.SIGINT, signal.SIGQUIT, signal.SIGTERM, signal.SIGKILL]
        signals = [signal.SIGQUIT, signal.SIGTERM, signal.SIGKILL]
        send_signals(get_candidates, signals, done_callback=done)

    def start_daemon(self, target, **kw):
        """Start a service (target) as a daemon process.

        `target` could be a function or an UApplication instance.
        """
        context = self._get_daemon_context(**kw)
        with _call(daemon.DaemonContext, **context) as bel:
            try:
                context = self._prepare_start(**context)
                # run forever ...
                async_call(target, **context)
            except Exception as why:
                print(f"{YELLOW}ERROR: {RED}{why}{RESET}")

    def stop(self, uri=None, name=None, **kw):
        """Stop a daemon process."""
        # try to find the process in DB
        assert False, "TODO: remove dependeces from DB"
        for process in list(self.workspace.find(UProcess, uri=uri, name=name)):
            if process.pid:
                print(f"{BLUE}Killing '{process.name}' ", end='', flush=True)
                for tries in range(100):
                    if test_process(process.pid, signal.SIGTERM):
                        time.sleep(0.2)
                        print(".", end='', flush=True)
                    else:
                        process.pid = None
                        process.state = 'dead'
                        # self.workspace.update(process)
                        print(f"{RED}[dead]", flush=True)
                        break
                    # give a  chance to end and pid has been removed
            else:
                print(f"{YELLOW}Process '{process.name}' is already dead")

        # try to find process in pid file
        for filename in fileiter('pid', wildcard=f'{name}.pid'):
            test_process(filename, signal.SIGTERM)

        print(f"{RESET}")

    # alias=None, label='running', shutdown=True):
    def attach(self, **kw):
        """Attach a process/service to the session.

        - `proc`: psutil.Process instance.
        - `alias`: human alias for the process.

        As optional keywords:

        - `restart`: whenever a process must restarted if dies.
        - `shutdown`: whenever a process must be shutdown when session is \
        deactivated.
        """
        proc = kw.get('proc')
        uri = kw.get('uri')
        name = kw.get('name')
        state = kw.setdefault('state', 'unknown')
        alias = kw.get('alias')

        # test_alive(self.layout.get_content('etc'))
        # if not proc:
            # for process in self.workspace.find(**kw):

        if proc:
            update_context(kw, proc)
            fp = get_fingerprint(proc)
            kw.setdefault('cmdline', fp['cmdline'])
            uri = build_uri(scheme=ATTACHED_SCHEME,
                            path=hasheable_cmdline(fp['cmdline']))
            kw.setdefault('uri', uri)

        if uri:
            name = kw.setdefault('name', codenamize(uri))

        if name:
            # save process config file
            wanted = ['alias', 'cmdline', 'name', ]
            conf = dict([(k, v) for (k, v) in kw.items() if k in wanted])
            self.layout.update_content('etc', conf, name)
            if alias:
                self.layout.set_alias('etc', alias, name)

        if proc and name:
            # create a fingerprint file for launching the file when needed
            # and include a pidfile in pid structure
            self.layout.set_content('pid', proc.pid, name)
            filename = self.layout.set_content('fp', fp, name, state)
            update_context(kw, filename=filename)

        # insert process in DB
        process = UProcess(**kw)
        self.workspace.update(process)
        update_context(kw, process=process)
        return kw

    def status(self):
        """**TBD:** Return session processes and status.
        """
        raise NotImplemented("implementation pending")

    def dettach_process(self, proc: psutil.Process = None, alias=None):
        """**TBD:** Dettach a process from the session.

        Any of the following arguments can be used:

        - `proc`: psutil.Process instance.
        - `alias`: human alias of the process.
        """
        raise NotImplemented("implementation pending")

    def add_dependence(self, parent, child):
        """Add a dependence between processes"""
        modified = False
        for parent in parent.split(','):
            for child in child.split(','):
                d = self.config.setdefault('dependences', dict())
                # don't use set() to preserve serialization
                s = d.setdefault(child, list())
                if parent not in s:
                    s.append(parent)
                    modified = True

        if modified:
            self.layout.set_content('etc', self.config, 'session', )

    def remove_dependence(self, parent, child):
        """Remove a dependence between processes"""
        modified = False
        for parent in parent.split(','):
            for child in child.split(','):
                d = self.config.get('dependences', dict())
                # don't use set() to preserve serialization
                s = d.get(parent, list())
                if child in s:
                    s.remove(child)
                    modified = True

        if modified:
            self.layout.set_content('etc', self.config, 'session', )

    def launch_process(self, match_if_same_cmdline=True, **kw):
        """Launch a previous captured process by name.

        - `match_if_same_cmdline`: consider the process to be the same if \
        cmdline is the same that stored one.
        - `kw`: contains search criteria keywords:
            Examples of search keywords are:

            - name='adaptable-joint'
            - state='operative'
            - alias='master.tws'
            - restart=1
            - shutdown=0
            - uri='session://supervisor'

        #. try to find a process that match criteria.
        #. if score is low but has the same command line (optional)
           we consider that is the same process in another non-registered state

        #. update DB when process is found
        #. launch a new process using the command line from config.
        """
        for process, score, proc, state, fp in self.find_processes(**kw):
            if proc:
                if score >= 0.9 or \
                   match_if_same_cmdline and fp['cmdline'] == proc.cmdline():
                    # self.layout.set_content('fp', fp, process.name, 'running')
                    self.workspace.update(process, pid=process.pid, state=state)
                    continue

            # launch a new process if all dependeces are matched
            for dep in kget(self.config['dependences'], process.name, process.alias) or []:
                parent, state = dep.split(':')
                pname, parent = vget(processes, parent, 'name', 'alias')
                if not (parent and parent.state == state):
                    break  # any dependence is not matched
            else:
                # launch the process
                conf = self.layout.get_content('etc', process.name)
                conf = self._launch_process(**conf)

    def _launch_process(self, **data):
        if 'cmdline' not in data:
            uri = parse_uri(data['uri'])
            data['cmdline'] = cmdline = [
                uri['path'],
            ]
            for k, v in uri['query_'].items():
                cmdline.append(f'{k}={v}')

        conf = self._prepare_start(**data)
        name = conf['name']

        stdout = open(self.layout.get_path('out', name), 'w')
        stderr = open(self.layout.get_path('err', name), 'w')
        # conf = self.layout.get_content('etc', name)
        p = subprocess.Popen(conf['cmdline'], stdout=stdout, stderr=stderr)
        self.layout.set_content('pid', p.pid, name)

        process = UProcess(**conf)
        self.workspace.update(process, pid=p.pid, state='starting')

        # wait until process seems to be 'stable' or timeout
        fp0, fp, state = None, None, conf['state']
        for trie in range(15):  # timeout=30 secs
            proc = psutil.Process(p.pid)
            fp0, fp = fp, get_fingerprint(proc)
            self.layout.set_content('fp', fp, name, state)
            if fp0 == fp:
                break
            print(f"[{trie}] waiting for process '{process.alias or name}' to be stable...({state})")
            time.sleep(5)
            state = 'running'

        update_context(conf, proc=proc, fp=fp, process=process)
        return conf

    def _prepare_start(self, uri=None, name=None, alias=None, **conf):
        name = name or codenamize(uri)
        alias = alias or name

        uri_ = parse_uri(uri)
        update_context(conf, uri_, uri_['query_'])
        realm = conf.setdefault('realm', uri_['path'])

        conf.setdefault('cmdline', sys.argv)
        update_context(conf, uri=uri, name=name, alias=alias)
        self.layout.set_content('etc', conf, name)
        self.layout.set_alias('etc', alias, name)

        conf['pid'] = pid = os.getpid()
        conf['state'] = 'starting'

        # TODO: config, tl, hub, db, session, etc
        # loop = conf['loop'] = asyncio.get_event_loop()
        hub = conf['hub'] = Hub(realm=realm)

        # TODO: add any maintenance/domestic procedures
        procedures = [dummy_main, ]
        app = _call(UApplication, procedures=procedures,
                    fixtures=conf, **conf)
        app.tl = TL(app=app, uid=conf.get('uid', name))

        proc = psutil.Process(pid)
        fp = get_fingerprint(proc)
        # self.layout.set_content('fp', fp, name, conf['state'])
        process = UProcess(**conf)
        self.workspace.update(process)

        update_context(conf, fp=fp, proc=proc, process=process,
                       app=app, tl=app.tl, hub=app.hub)

        # app.run()
        # run(app.tl.start())

        return conf

    def launch_service(self, uri, alias=None):
        """Launch a service (a method instance) parsing calling arguments\
        from uri.

        Example:

        ``session.launch_service(
        uri="ib://tws:9090/download-historical?uid=historical&account=0&tws=tws.demo",
        alias="downloader")``
        """
        uri_ = parse_uri(uri)
        func = self
        for name in uri_['path'].split('/'):
            name = name.replace('-', '_')
            func = getattr(func, name, self)

        alias = alias or name
        if func:
            self.start_daemon(target=func, uri=uri, alias=alias)
        else:
            raise RuntimeError(f"can't find a function linked with f{uri}")

    def _supervisor(self):
        "Supervisor daemon tasks"

        def check_attached_processes():
            self.launch_process(restart=1)

        def hide_check_attached_processes():
            processes = dict()

            # update fps states
            for process in list(self.workspace.find(UProcess, restart=1)):
                fps = self._get_available_fps(name=process.name)
                score, proc, label, fp = self._best_matching_fps(
                    fps, process.pid)
                if score < 0.90:
                    process.state, process.pid = None, None
                else:
                    process.state, process.pid = label, proc.pid
                self.workspace.update(process)
                processes[process.name] = process

            for name, process in processes.items():
                if not process.pid:
                    # check dependeces/pre-requsites
                    for dep in kget(self.config['dependences'], process.name, process.alias) or []:
                        parent, state = dep.split(':')
                        pname, parent = vget(processes,
                                             parent, 'name', 'alias')
                        if not (parent and parent.state == state):
                            break
                    else:
                        # launch the process/service
                        self.launch_process(name=process.name)
                        # # TODO: process and service are the same?
                        # if process.uri.startswith(ATTACHED_SCHEME):
                            # self.launch_process(name=process.name)
                        # else:
                            # self.launch_service(process.uri)
            foo = 1

        def clean_dead_pid():
            count = 0
            for filename in fileiter('pid', wildcard='*.pid'):
                print(f" {YELLOW}Testing {filename:40}", end='')
                proc = test_alive(filename)
                name = os.path.basename(filename)
                name = os.path.splitext(name)[0]
                path = self.layout.get_path('etc', name)
                if os.path.exists(path) and proc:
                    count += 1
                    print(f"{GREEN}[ok] {proc.pid}")
                else:
                    print(f"{RED}[dead]")
                    os.remove(filename)
            print(f" {GREEN}[{count}]{YELLOW} running processes{RESET}")

        FUNCTIONS = [clean_dead_pid, check_attached_processes]
        functions = []

        # for tries in range(n):
        while True:
            if not functions:
                functions.extend(FUNCTIONS)
                # random.shuffle(functions)
            if functions:
                func = functions.pop()
                print(f"{BLUE}- Running: {func.__name__}{RESET}")
                func()
            time.sleep(5)

        print("Bye!")

    def _get_daemon_context(self, **kw):
        gpath = self.layout.get_path
        s = partial(dset, kw)
        name = s('name', codenamize(kw['uri']))

        s('pid', gpath('pid', name))
        s('pidfile', SmartPIDLockFile(path=kw['pid']))
        s('files_preserve', list(range(0, 255)))
        s('stdin', None)
        s('stdout', open, gpath('out', name), 'w')
        s('stderr', open, gpath('err', name), 'w')
        s('working_directory', self.path)
        s('shutdown', 0)
        s('restart', 0)
        # s('signal_map', {})
        return kw

    def _demo_task(self, n):
        for i in range(n):
            print(f"doing something cool: {i}")
            time.sleep(5)
        print("-End demo task-")

    def _get_available_fps(self, name=None):
        fingerprints = dict()
        if isinstance(name, str):
            regexp = re.compile(name, re.DOTALL)
        else:
            regexp = None
        for info, filename, fp0 in self.layout.iter_file_content('fp'):
            name = info['name']
            if regexp and not regexp.match(name):
                continue
            fps = fingerprints.setdefault(name, dict())
            fps[info['label']] = fp0

        return fingerprints

    def _best_matching_fp(self, fp0, *pids):
        pids = [p for p in pids if p] or psutil.pids()

        best_score, best_proc, best_fp = 0, None, None
        for pid_ in pids:
            proc = psutil.Process(pid_)
            fp = get_fingerprint(proc)
            s = compare_fingerprint(fp0, fp)
            if s > best_score:
                best_score, best_proc, best_fp = s, proc, fp

        return best_score, best_proc, best_fp

    def _best_matching_fps(self, fps, pids=[], name=None, deep_serch=False):
        candidates = set([])
        if not isinstance(pids, list):
            pids = [pids]
        pids = [p for p in pids if p]
        if not pids:
            deep_serch = True
        candidates.update(pids)

        if deep_serch:
            candidates.update(psutil.pids())

        def do_search(pids):
            best_score, best_proc, best_label, best_fp = 0, None, None, None
            for pid_ in pids:
                # if pid_ < 1024:  #  not in Linux
                    # continue  # system proceces
                try:
                    proc = psutil.Process(pid_)
                    fp = get_fingerprint(proc)
                except Exception as why:
                    continue  # may be a zomby/protected process

                for pname, fps_ in fps.items():
                    if name not in (pname, None):
                        continue

                    for label, fp0 in fps_.items():
                        # if not label and exclude_no_label:
                            # continue
                        s = compare_fingerprint(fp0, fp)
                        if s > best_score:
                            best_score, best_proc, best_label, best_fp = s, proc, label, fp
                            if s == 1.0:
                                return best_score, best_proc, best_label, best_fp

            return best_score, best_proc, best_label, best_fp

        return do_search(candidates)

    def locate_process(self, **data):
        for process in self.workspace.find(UProcess, **data):
            fps = self._get_available_fps(name=process.name)
            score, proc, state, fp = self._best_matching_fps(fps, name=process.name)
            if score > 0.9:
                return score, proc, state, fp
        return [None] * 4

    def find_processes(self, join='AND', **query):
        """Find running processes that match a query"""
        for process in self.workspace.find(UProcess, join=join, **query):
            fps = self._get_available_fps(name=process.name)
            score, proc, state, fp = self._best_matching_fps(
                fps, name=process.name)
            yield process, score, proc, state, fp

    def _get_preferred_fp(self, name):
        desired_labels = ['operative', 'running', 'launch', ]
        candidates = dict()
        # for d, filename, fp0 in self.layout.iter_file_content('fp', name):
            # candidates[d['label']] = d, filename, fp0

        for d, filename, fp0 in self.layout.iter_file_content('fp', name):
            candidates[d['label']] = d, filename, fp0

        if not candidates:
            return {}, '', {}

        desired_labels.extend(candidates.keys())
        for label in desired_labels:
            if label not in candidates:
                continue
            d, filename, fp0 = candidates[label]
            break

        return d, filename, fp0

    def check_structure(self):
        """Check is a USession folder has been Initialized."""
        debug(f'Checking structure in {self.path}')
        return os.path.exists(self.db_file)

    # def load(self):
        # warnings.warn("Load is not longer necessary", DeprecationWarning, stacklevel=2)
        # self.config = load_config(self.session_config_file)
        # if self.config:
            # self.db = DB(self.db_file)
            # self.workspace = self.WORKSPACE(self.db)
        # else:
            # raise RuntimeError("Config not found: maybe need session init here ?")

    def update_config(self, value, *keys):
        """Helper to save the session configuration."""
        container = self.config
        if update_container_value(container, value, *keys):
            self.layout.set_content('etc', container, 'session')
