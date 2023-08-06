import re
import types
import asyncio
from functools import wraps
from aiopb.aiopb import Hub

# TODO: move UAgent to gutools or aiopb
from gutools.tools import _call

# hub = get_hub()
exposed = dict()
keys_functions = dict()
members = dict()
def expose(**context):
    def decorator(f):
        @wraps(f)
        def wrap(*args, **kw):
            message = f(*args, **kw)
            if message is not None:
                key = f.__context__.get('response')
                if key is None:
                    key = '{}/{}'.format(keys_functions[f], 'response')
                hub.publish(key, message)
            return message

        assert f.__name__[0] != '_', "Exposing private member ({}) is not allowed".format(f.__name__)
        f.__context__ = context
        key = '/uagent/{}'.format(f.__qualname__.lower().replace('.', '/'))
        exposed[key] = f
        keys_functions[f] = key
        return wrap
    return decorator

def domestic(condition='True', start=0, restart=5, **env):
    """Decorator for domestic method of a UAgent class.

    Domestic are implemented by asyncio module.
    """
    def decorator(f):
        @wraps(f)
        def wrap(*args, **kw):
            if Domestic.stop_restart:
                self_1 = args[0]
                for candidate in list(Domestic.stop_restart.keys()):
                    if candidate.__func__ == wrap:
                        if candidate.__self__ == self_1:
                            Domestic.stop_restart.pop(candidate)
                            return
                        else:
                            foo = 1

            start, condition, restart, env = wrap.__domestic__
            kw2 = dict(env)
            kw2.update(kw)

            if eval(condition, {'self': args[0],}, kw2):
                f(*args, **kw2)

            if restart > 0:
                loop = asyncio.get_event_loop()
                loop.call_later(restart, wrap, *args,)

        wrap.__domestic__ = (start, compile(condition, '<string>', 'eval'), restart, env)
        wrap.__domestic__backup__ = wrap.__domestic__
        return wrap
    return decorator

def update_domestic(wrap, **env):
    func = wrap.__func__
    existing = list(func.__domestic__)
    for i, key in enumerate(['start', 'condition', 'restart']):
        value = env.pop(key, None)
        if value is not None:
            if key == 'condition':
                value = compile(value, '<string>', 'eval')
            existing[i] = value

    existing[-1].update(env)
    func.__domestic__ = tuple(existing)

def restore_domestic(wrap, **env):
    func = wrap.__func__
    func.__domestic__ = func.__domestic__backup__

class Domestic(object):
    """Support for domestic methods.
    Any derived class may decorate a function member with

    @domestic(condition='True', start=0, restart=5, **env)

    and the asyncio loop will call when params match.
    """
    stop_restart = dict()

    def __init__(self):
        # add to schedule all domestic taks
        loop = asyncio.get_event_loop()
        for name in dir(self):
            func = getattr(self, name)
            if isinstance(func, types.MethodType):
                params = getattr(func, '__domestic__', None)
                if params:
                    loop.call_later(params[0] or 0, func, )

    def __del__(self):
        self.stop_domestics()

    def stop_domestics(self):
        for name in dir(self):
            func = getattr(self, name)
            if isinstance(func, types.MethodType):
                params = getattr(func, '__domestic__', None)
                if params:
                    self._stop_domestic(func)

    def _stop_domestic(self, func):
        self.stop_restart[func] = self


class UAgent(object):
    """Allow to handle (key, messages) requests.

    Subscribe to '/uagent/(class|uid)' channels in order to receive requests
    from anywhere inside the same realm.

    Any @expose function will be accessible if key match the funcion name
    The keys must have the format:
          uagent/method
          uagent/member/method

    agent instances or members are cached for next calls with same key.

    _call() will try to match arguments from message to function
    before make the call and strategy used will cache when possible.

    Finally, if `__reply_key__` is provided in the message (dict subclase),
    the response will be published into this channel.
    """

    def __init__(self, uid=None, app=None):
        super().__init__()
        kname = self.__class__.__name__.lower()
        self.uid = uid or kname
        assert self.uid
        self.pattern = '/uagent/({}|{})/(?P<func>.*)$'.format(kname, self.uid)
        # e.g. uagent/dbevents/foo_func
        self.app = app
        self.app.hub.subscribe(self.pattern, self.handle)

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        if exception_type is None:
            self.__detach__()

    def __detach__(self):
        hub = self.app.hub
        hub and hub.detach(self)

    def __del__(self):
        self.__detach__()

    def handle(self, key, message):
        # TODO: review if
        func, _self = exposed.get(key), members.get(self, dict()).get(key, self)
        if not func:
            m = re.match(self.pattern, key, re.I|re.DOTALL)
            if m:
                func, _self = self, None
                for locator in m.groups()[0].split('/'):
                    if locator[0] == '_':
                        return  # don't allow private elements
                    func, _self = getattr(func, locator), func
                if func:
                    exposed[key] = func # save in cache for next call
                    members.setdefault(self, dict())[key] = _self

        response = func and _call(func, message, self=_self)
        if isinstance(message, dict):
            reply_key = message.get('__reply_key__')
            if reply_key:
                self.app.hub.publish(reply_key, response)
        return response


def test_call_exposed_methods():

    agent = FooAgent()
    r1 = agent.mysum(1, 2)
    for message in [(1, 2), dict(a=1, b=2)]:
        r = agent.handle('/uagent/fooagent/mysum', message)
        assert r == r1

def test_subrogate_call_to_members():

    agent = FooAgent()
    r1 = agent.mysum(1, 2)
    for message in [(1, 2), dict(a=1, b=2)]:
        r = agent.handle('uagent/fooagent/calc/sum2', message)
        assert r == r1


if __name__ == '__main__':
    class Calc:
        def sum2(self, a, b):
            return a + b

    class FooAgent(UAgent):
        def __init__(self):
            super(FooAgent, self).__init__()
            self.calc = Calc()

        @expose(response='foo/bar')
        def mysum(self, a, b):
            ""
            return a + b

    test_call_exposed_methods()
    test_subrogate_call_to_members()

    foo = 1
