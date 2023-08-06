import asyncio
import sys
import inspect
import traceback
import time
import random
from gutools.tools import _call
from gutools.colors import *
from gutools.uobjects import UObject

available_context = dict()

def context(**context):
    def decorator(f):
        @wraps(f)
        def wrap(*args, **kw):
            message = f(*args, **kw)
            return message

        f.__context__ = context
        key = f.__qualname__.lower()
        available_context[key] = f
        return wrap
    return decorator

class UProcedure(UObject):
    """A single method that runs (forever usually)
    that user can set a policy behavior on
    exceptions or external events """
    __args__ = ('method', )
    __kwargs__ = {'exceptions': dict, 'events': dict,}
    __slots__ = __args__ + tuple(set(__kwargs__).difference(__args__))

class UApplication(object):
    """Supervise some procedures as a whole entity
    handling exceptions and events that
    happens within them.

    UApplication define a Policy for handling
    non-expected exceptions.

    When an exception is raised, App tries to find a handler for the exception
    and will take actions based on handler returned value.

    """
    ABORT = 0
    RESTART = 1
    CONTINUE = 2

    def __init__(self, context=None, fixtures=None, procedures=None,
                  policy=1, exceptions=None, restart_delay=5,
                  hub=None, tl=None, config=None, session=None,
                  realm='/default'):

        self.context = context or dict()
        self.fixtures = fixtures or dict()
        self.procedures = procedures or list()
        self.policy = policy
        self.exceptions = exceptions or dict()
        self.restart_delay = restart_delay
        self.hub = hub
        self.tl = tl
        self.realm = realm
        self.config = config or dict()
        self.session = session or dict()
        self.agents = dict()
        self.running = False
        self._loop = None

    async def run(self, *procedures):
        """
        TODO: Implement additional policies
        - CONTINUE
        - RESTART + REMOVE failling procedure
        """
        self.running = True
        loop = self._loop
        assert isinstance(loop, asyncio.base_events.BaseEventLoop)

        # assert on using the same loop
        assert loop == self.hub._loop
        # assert loop == self.tl._loop

        self.procedures.extend(procedures)

        def collect_awaitables():
            # prepare fixtures
            context = self._expand_needed_fixtures()
            context.update(self.context)

            # collect and fire procedures
            awaitables = list()
            for proc in self.procedures:
                if not inspect.iscoroutinefunction(proc):
                    raise RuntimeError(f"{proc} is not an coroutine function (async def xxx()")

                aw = _call(proc, **context)
                awaitables.append(aw)
            return awaitables

        # create the related tasks
        ct = loop.create_task
        awaitables = [ct(c) for c in collect_awaitables()]
        done = []
        while awaitables:
            try:
                # get the global policy, that may change by specific exception
                policy = self.policy

                # fire procedures waiting to end or any exception
                done, pending = await asyncio.wait(awaitables, loop=loop,
                                                   return_when=asyncio.FIRST_COMPLETED)
            except Exception as why:
                print(f"{RED}{why}{RESET}")
                frame = inspect.trace()[-1]
                # traceback.print_exc()
                # traceback.print_exc(file=sys.stdout)
                # print(f"{RESET}")

                # Find a handler for the exception
                # (per-exception policy)
                for ex, p in self.exceptions.items():
                    if isinstance(why, ex):
                        if not isinstance(p, int):
                            policy = p(why)
                        break
            # acts according policy
            if policy in (self.ABORT, ):
                break
            elif policy in (self.RESTART, ):
                # TODO: change loop to make it reentrant
                print(f"{YELLOW}Restarting finished tasks in {self.restart_delay} sec{RESET}")
                await asyncio.sleep(self.restart_delay)
                for i, coro in enumerate(collect_awaitables()):
                    if awaitables[i] in done:
                        # replace the finished task by a new one
                        awaitables[i] = ct(coro)

            elif policy in (self.CONTINUE, ):
                raise NotImplementedError("CONTINUE policy is not yet Implemented")

    async def start(self):
        self._loop = asyncio.get_running_loop()  # must be already running
        # self._loop = asyncio.get_event_loop()
        assert self._loop.is_running()
        await self.hub.start(self._loop)
        # self.tl.start(self._loop)  # TODO:

    async def stop(self):
        await self.hub.stop()
        # self.tl.stop()

    def pause(self):
        pass

    def resume(self):
        pass

    def add_agent(self, factory, **kw):
        args = self._expand_args(factory, **kw)
        agent = _call(factory, **args)
        self.agents[agent.uid] = agent
        return agent

    def _expand_needed_fixtures(self):
        "Expand the arguments needed by awaitables from fixtured factories"
        exp = dict()
        for func in self.procedures:
            exp.update(self._expand_args(func))
        return exp

    def _expand_args(self, func, **kw):
        kw2 = dict(self.fixtures)
        kw2.update(kw)

        exp = dict()
        info = inspect.getfullargspec(func)
        for arg in info.args:
            if arg in kw2:
                fix = kw2[arg]
                if hasattr(fix, '__call__'):
                    fix = _call(fix, **self.context)
                exp[arg] = fix

        return exp


def test_uobject_factories():
    p1 = UProcedure()
    p1.events['foo'] = 1

    p2 = UProcedure()
    p2.exceptions['bar'] = 1

    p3 = UProcedure()

    assert 'foo' in p1.events
    assert 'foo' not in p2.events
    assert 'foo' not in p3.events

    assert 'bar' not in p1.exceptions
    assert 'bar' in p2.exceptions
    assert 'bar' not in p3.exceptions


def test_uapplication():

    async def foo(i):
        print(f"> Enter foo({i})")
        await asyncio.sleep(2)
        print(f"< Exit foo({i})")

    async def bar(i):
        print(f"> Enter bar({i})")
        await asyncio.sleep(3)
        _ = 1 / 0.0
        print(f"< Exit bar({i})")

    async def buz(i):
        print(f"> Enter buz({i})")
        await asyncio.sleep(1)
        if random.random() < 0.25:
            open('/non-existin-directory', 'r')
        print(f"< Exit buz({i})")

    def exception_handler(exc):
        if random.random() > 0.8:
            return UApplication.ABORT
        if random.random() > 0.5:
            # return UApplication.CONTINUE
            return UApplication.RESTART
        return UApplication.RESTART

    app = UApplication(policy=UApplication.RESTART)
    app.procedures = [foo, bar, buz]
    app.exceptions[ZeroDivisionError] = app.RESTART
    app.exceptions[FileNotFoundError] = exception_handler

    app.run()

    foo = 1

if __name__ == '__main__':
    test_uobject_factories()
    test_uapplication()


    foo = 1
