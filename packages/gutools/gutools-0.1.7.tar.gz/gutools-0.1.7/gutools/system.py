import os
import re
import signal
import time
import psutil
from lockfile.pidlockfile import PIDLockFile

from gutools.tools import wlikelyhood
# Process

def send_signals(iterator, signals, tries=3, pause=1, done_callback=None):
    """iterator returns (name,pid) items"""
    def get_names(running):
        return set([name for name, _ in running])

    for sig in signals:
        running = [item for item in iterator()]
        if not running:
            break

        # if sig in (signal.SIGKILL, ):
            # print(f"{RED}KILLING: {CYAN}{len(running)} {RED}processes {RESET}")
        # else:
            # print(f"{BLUE}Stopping: {CYAN}{len(running)} {BLUE}processes {RESET}")

        for _ in range(tries):
            names = get_names(running)
            for name, pid in running:
                print(f' {name}\t<----\tsignal: {sig}')
                test_process(pid, sig=sig)

            time.sleep(pause)
            running = [item for item in iterator()]
            names2 = get_names(running)

            for name in names.difference(names2):
                done_callback and done_callback(name)
                # pidfile = self._get_filename('pid', name)
                # if os.path.exists(pidfile):
                    # os.remove(pidfile)

            names = names2
            if not running:
                break


def test_process(pid, sig=0):
    if not pid:
        return
    if isinstance(pid, str):
        try:
            pid = int(open(pid).read().strip())
        except Exception as why:
            try:
                pid = int(pid)
            except ValueError:
                return
    try:
        os.kill(pid, sig)
    except OSError as why:  # is finished?
        if why.errno == 3 or why.strerror.find("No such process"):
            return False
    return pid

def test_alive(pid):
    if not pid:
        return
    if isinstance(pid, str):
        try:
            pid = int(open(pid).read().strip())
        except Exception as why:
            try:
                pid = int(pid)
            except ValueError:
                return
    try:
        proc = psutil.Process(pid)
        proc.cwd()
    except Exception as why:  # is finished?
        return None
    return proc


def get_fingerprint(proc: psutil.Process) -> dict:
    # BINDED/LISTEN sockets
    fp = {
        'files': [],
        'listen': [],
        'established': [],
        'udp': [],
        'cmdline': proc.cmdline(),
    }
    try:

        for con in proc.connections():
            key = con.status.lower().replace('none', 'udp')
            if key in ('listen', 'udp'):
                addr = con.laddr
            else:
                addr = con.raddr
            fp[key].append(f'{addr.ip}:{addr.port}')

        # Open files
        files = fp['files']
        for fd in proc.open_files():
            info = f"{fd.path}"
            files.append(info)

    except Exception:
        foo = 1

    return fp

def compare_fingerprint(fp0, fp):
    s = wlikelyhood(fp0, fp, listen=20, established=2, files=30, cmdline=50)
    return s

def find_process(rexp):
    if isinstance(rexp, str):
        rexp = re.compile(rexp, re.DOTALL|re.I)
    for pid in psutil.pids():
        process = psutil.Process(pid)
        cmdline = process.cmdline()
        m = cmdline and rexp.search(cmdline[0])
        if m:
            yield process



class SmartPIDLockFile(PIDLockFile):
    def __init__(self, path, threaded=False, timeout=None):
        if os.path.exists(path) and not test_process(path):
            os.remove(path)
        super().__init__(path, threaded, timeout)
