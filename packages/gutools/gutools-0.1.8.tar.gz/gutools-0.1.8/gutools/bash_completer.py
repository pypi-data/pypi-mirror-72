import os
import re
import glob
import psutil

from gutools.tools import _call, get_calling_function
from gutools.controllers.arguments import *
from cement import App, Controller, ex

# -------------------------------------------------------------------
# helpers for expand argument values
# -------------------------------------------------------------------


def exp_file(args):
    partial_path = args[-1]

    if '*' in partial_path:
        return args

    partial_path += '*'
    return [f for f in glob.iglob(partial_path)]


def exp_pid(attr):
    "Expand all matching running processes pid"
    candidates = set([])
    excluded = (os.getpid(), )
    for pid in psutil.pids():
        if pid in excluded:
            continue
        pid = str(pid)
        if pid.startswith(attr):
            candidates.add(pid)
    return candidates


remove_pattern = re.compile("[{}]".format(r''.join([r'\{}'.format(c) for c in '${}@#!-'])))


def hasheable_cmdline(cmdline):
    # join all the tokens ...
    cmdline = ''.join(cmdline)
    # and replace bash sensitive symbols
    cmdline = remove_pattern.sub('', cmdline)

    return cmdline


def exp_cmdline(attr):
    "Expand all matching running command line"
    candidates = set([])
    excluded = (os.getpid(), )
    for pid in psutil.pids():
        if pid in excluded:
            continue
        proc = psutil.Process(pid)
        cmdline = proc.cmdline()
        # create an alternative represetatoin of cmdline
        # compatible with being a single string
        alt_cmd = hasheable_cmdline(cmdline)
        if attr in alt_cmd:  # .startswith(attr):
            candidates.add(alt_cmd)
    return candidates


def find_process_by_cmdline(alt_cmd):
    candidates = set([])
    for pid in psutil.pids():
        proc = psutil.Process(pid)
        cmdline = proc.cmdline()
        # create an alternative represetatoin of cmdline
        # compatible with being a single string
        cmdline = hasheable_cmdline(cmdline)
        if cmdline.startswith(alt_cmd):
            candidates.add(proc)

    return candidates


# -------------------------------------------------------------------
# CompleterController
# -------------------------------------------------------------------
# TODO: add more specific argument expansors


class CompletableController(Controller):

    default_argument_expander = {
        # 'file': exp_file,        # expand names from file system
        'pid': exp_pid,          # expand pid from running process in os
        'cmdline': exp_cmdline,  # expand cmdline from running process in os
    }
    "'static' functions that would be called for completion by default"

    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        self._command_argument_expander = dict()
        "per commnad functions that override default_argument_expander"

    def _add_expander(self, command, attr, func):
        exp = self._command_argument_expander.setdefault(command, {})
        exp[attr] = func

    def guess_values(self, command, info, args):
        """Try to guess argument values based on argument definition."""
        # argument = info[0][-1].split('-')[-1]
        argument = info[1].get('dest')

        func = self._command_argument_expander.get(command, {}).get(argument)
        if not func:
            func = self.default_argument_expander.get(argument, None)

        if func:
            return _call(func, self=self, attr=args[-1])

    def _get_completion_prefix(self, info, args):
        # get the last token used by bash completion
        # get the prefix that must be removed from responses
        # to match what bash expect for completion
        last = args[-1]
        if last in ('=', ':'):
            incomplete, last = list(args), ''
        else:
            incomplete = list(args[:-1])

        prefix = list()
        attrs = info[0]
        while incomplete:
            token = incomplete.pop()
            if token in attrs:
                break
            prefix.append(token)
        prefix.reverse()
        prefix = ''.join(prefix)
        return prefix, f'{prefix}{last}'

    def _get_current_command(self, args):
        """Get the current command in cmdline"""
        exposed = self._get_exposed_commands()
        incompleted = list(args)
        while incompleted:
            token = incompleted.pop()
            if token in exposed:
                return token
        return ''

    # Extra for rendering templates
    def fqname(self):
        """Get the Full Qualified Name of the controller
        based on parents controllers.
        """
        def iterator():
            for c in self.app.handler.list('controller'):
                m = c.Meta
                child = m.label
                parent = getattr(m, 'stacked_on', None)
                yield parent, child

        parent = dict()
        for p, c in iterator():
            parent[c] = p

        me = self.Meta.label
        fqname = list()
        while me and me != 'base':  # convenience value
            fqname.insert(0, me)
            me = parent.get(me, None)

        return '.'.join(fqname)

    def render(self, data, **kw):
        """Get the template from calling context."""

        controller = self.fqname()
        func = get_calling_function(level=2).__func__.__name__
        renderer = getattr(self.Meta, 'renderer', 'jinja2')
        template = f'{controller}.{func}.{renderer}'
        return self.app.render(data, template)


def fix_command_line(cmdline):
    # remove wrapped (")
    cmd = cmdline.strip('"')
    # # join BASH splitting in uri and assignations
    # cmd = cmd.replace(' : ', ':')
    # cmd = cmd.replace(' = ', '=')

    return cmd


class CompleterController(Controller):
    """Bash completed controller for cement.
    To use just include this code in your main cement App

    from bash_completer import CompleterController

    class MyApp(App):

        class Meta:
            label = 'atlas'

            handlers = [
                    Base,
                    CompleterController,
                    ...,
        ]

    and in a your main application folder
    create and execute the script

    # install_bash_completer.rc
    # execute source install_bash_completer.rc
    _myapp_complete() {
        # set your app name
        local myapp=$(basename "$PWD")

        COMPREPLY=()
        local words=( "${COMP_WORDS[@]}" )
        local word="${COMP_WORDS[COMP_CWORD]}"
        words=("${words[@]:1}")
        local completions="$($myapp completer --cmplt=\""${words[*]}"\")"
        COMPREPLY=($(compgen -W "$completions" -- "$word"))
     }

    complete -F _myapp_complete atlas
    """
    class Meta:
        label = 'completer'
        stacked_on = 'base'
        stacked_type = 'nested'
        description = 'auto-completer: hidden command'
        arguments = [
            (['--cmplt'], dict(help='command list so far')),
            (['--cword'], dict(help='word that is being completed', type=int)),
            (['--cpos'], dict(help='cursor position in the line', type=int)),

        ]
        hide = True

    def _default(self):
        """
        Returns completion candidates for bash complete command.
        It would complete:
        - nested controllers
        - controller commands
        - controller arguments names
        - controller arguments values based on argument definition
        """

        self._build_controller_tree()
        cmdline = fix_command_line(self.app.pargs.cmplt)
        cword = self.app.pargs.cword
        cpos = self.app.pargs.cpos

        # we use cpos to be able to complete in the middle of a sentence

        # Get all cmdline tokens
        tokens = [cmd for cmd in cmdline.split(' ')]
        # Get tokens until current cursor position
        # capture trailing space as well
        under_construction = [cmd for cmd in cmdline[:cpos].split(' ')]
        under_construction[0] = 'base'  # remove program name :)
        # notmatch = [cmd for cmd in cmdline[cpos:].split(' ')][:-1]
        last = tokens[cword]
        # if not word:
            # under_construction = under_construction[:-1]

        used_arguments = list()
        # get already completed controllers
        controller_names = list()
        arguments = list()
        # get all used controllers and the final part that is building
        # under last controller scope
        for i in range(len(under_construction) - 1, -1, -1):
            name = under_construction[i]
            fqname = self.root.get(name)
            if fqname and set(fqname.split('.')).issubset(under_construction):
                controller_names.append(name)
                if not arguments:
                    arguments = under_construction[i + 1:]

        controller_names = controller_names or ['base']
        controllers = [self.parent[name][1]() for name in controller_names]
        candidates = list()
        if len(arguments) <= 1:
            for c in controllers:
                # just show the exposed commands that match with pattern
                candidates.extend([cmd for cmd in c._get_exposed_commands() if
                                   cmd.startswith(last)])
                # and nested controllers
                parent = c.Meta.label
                for name, (p, _) in self.parent.items():
                    if parent == p:
                        if name.startswith(last):
                            candidates.append(name)

                break  # only do with last controller near cursor

        elif len(arguments) > 1:
            # is a subcommand trying to complete options
            command = arguments[0]
            # last = arguments[-1]
            # candidates.clear()
            used_attr = set()
            for c in controllers:
                for meta in [cmd['arguments'] for cmd in
                             c._collect_commands()
                             if cmd['exposed'] and cmd['label'] == command]:

                    # check for param value completion
                    # of param name completion
                    # if there is a matched attr, then complete param
                    # else show matching param names
                    incomplete = set()

                    # find the closer to cursor parameter
                    best_idx, best_info = 0, None
                    for info in meta:
                        attrs, specs = info
                        if not specs.get('dest'):  # is a key, not a positional args
                            continue
                        # check if flag as been already used in cmdline
                        if set(attrs).intersection(arguments):
                            used_attr.update(attrs)

                        for attr in attrs:
                            if attr.startswith(last):
                                incomplete.add(attr)
                            try:
                                idx = arguments.index(attr, best_idx)
                                best_idx, best_info = idx, info
                            except ValueError:
                                pass
                    # best points to the closer to end attr that is formed or 0
                    if last.startswith('-') or not best_info:
                        # try to complete attr names, excluding already used
                        incomplete.difference_update(used_attr)
                        candidates.extend(incomplete)
                    else:
                        # try to complete attr values
                        candidates = c.guess_values(command, best_info, under_construction) or []

                    # TODO: actually we can return here ...
                break  # just use the 1st active controller
        else:
            # there is nothing to do here
            pass

        # candidates = ['1']
        # print(*candidates)
        foo = 1
        for token in candidates:
            print(token, flush=True)

    def _build_controller_tree(self):
        """Build the controller tree"""
        self.root = dict()       # not used by now
        self.reverse = dict()    # not used by now
        self.controller = dict()
        self.parent = dict()

        def iterator():
            for c in self.app.handler.list('controller'):
                m = c.Meta
                if m == self.Meta:
                    continue  # skip self completer from processing

                # child = '' if m.label == 'base' else m.label
                child = m.label
                # if getattr(m, 'stacked_type', None) == 'nested':
                    # parent = getattr(m, 'stacked_on', None)
                # else:
                    # parent = None
                parent = getattr(m, 'stacked_on', None)
                yield parent, child, c

        for parent, child, c in iterator():
            self.parent[child] = parent, c

        for child, (parent, c) in self.parent.items():
            path = [child, ]
            while parent:
                path.append(parent)
                parent, _ = self.parent[parent]

            # path.remove('base')
            path = '.'.join(reversed(path))
            self.root[child] = path
            self.controller[path] = c
            self.reverse[path] = child

        foo = 1
