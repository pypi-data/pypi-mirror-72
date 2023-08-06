import pytest

import random
import operator
from time import time, sleep
from select import select

from gutools.tools import get_calling_function, flatten
from gutools.utests import speed_meter
from lswarm.stm import Layer, Reactor, DebugReactor, STATE_INIT, STATE_READY, STATE_END, \
    QUITE_STATE, EVENT_QUIT, EVENT_TERM, MERGE_ADD, MERGE_REPLACE_EXISTING

from lswarm.stm import _TestBrowserProtcol

class _TestReactor(Reactor):
    def __init__(self, events=None):
        super().__init__()
        self._fake_events = events  # iterator
        self._queue = list()

    def stop(self):
        print("Stoping reactor")
        super().stop()

    # def next_event(self):
        # try:
            # while True:
                # if self._queue:
                    # return self._queue.pop(0)
                # elif self._fake_events:
                    # return self._fake_events.__next__()
                # sleep(0.1)
        # except StopIteration:
            # self.running = False
            # return EVENT_TERM, None

    def next_event(self):
        """Blocks waiting for an I/O event or timer.
        Try to compensate delays by substracting time.time() and sub operations."""
        def close_sock(fd):
            self._protocols[fd].eof_received()
            self.close_channel(self._transports[fd])

        while True:
            if self._queue:
                return self._queue.pop(0)
            elif self._fake_events:
                try:
                    return self._fake_events.__next__()
                except StopIteration:
                    self.running = False
                    return EVENT_TERM, None

            # there is not events to process. look for timers and I/O
            if self._timers:
                when, restart, key = timer = self._timers[0]
                seconds = when - self.time
                if seconds > 0:
                    rx, _, ex = select(self._transports, [], self._transports, seconds)
                    for fd in rx:
                        try:
                            raw = fd.recv(0xFFFF)
                            if raw:
                                self._protocols[fd].data_received(raw)
                            else:
                                close_sock(fd)
                        except Exception as why:
                            close_sock(fd)
                            pass

                    for fd in ex: # TODO: remove if never is invoked
                        close_sock(fd)
                        foo = 1
                else:
                    self.publish(key, None)
                    # --------------------------
                    # rearm timer
                    self._timers.pop(0)
                    if restart <= 0:
                        continue  # is a timeout timer, don't restart it
                    when += restart
                    timer[0] = when
                    #  insert in right position
                    i = 0
                    while i < len(self._timers):
                        if self._timers[i][0] > when:
                            self._timers.insert(i, timer)
                            break
                        i += 1
                    else:
                        self._timers.append(timer)
            else:
                # duplicate code for faster execution
                rx, _, _ = select(self._transports, [], [], 1)
                for fd in rx:
                    try:
                        raw = fd.recv(0xFFFF)
                        if raw:
                            self._protocols[fd].data_received(raw)
                        else:
                            close_sock(fd)
                    except Exception as why:
                        close_sock(fd)
                        pass
            foo = 1
        foo = 1

def populate1(container, population, n):
    while n:
        ctx = container
        for x in population:
            key = str(random.randint(0, x))
            ctx = ctx.setdefault(key, dict())

        key = str(random.randint(0, population[-1]))
        ctx = ctx.setdefault(key, list())
        ctx.append(n)
        n -= 1

def populate2(container, population, n):
    while n:
        key = tuple([str(random.randint(0, x)) for x in population])
        container[key] = n
        n -= 1

class _TestLayer(Layer):

    def _setup__testlayer(self):
        states = {
            STATE_END: [[], ['bye'], []],
        }

        transitions = {
            STATE_READY: {
                'each:5,1': [
                    ['READY', [], ['timer']],
                ],
                'each:5,21': [
                    [STATE_READY, [], ['bye']],
                ],
            },
        }
        return states, transitions, MERGE_ADD

    def start(self, **kw):
        print("Hello World!!")
        self.t0 = time()
        self._func_calls = dict()
        self._log_function()

    def term(self, key, **kw):
        elapsed = time() - self.t0
        print(f"Term {key}: {elapsed}")
        super().term(key, **kw)

    def timer(self, **kw):
        "Empty timer to be overrided"

    def _log_function(self):
        func = get_calling_function(level=2)
        name = func.__func__.__name__
        self._func_calls.setdefault(name, 0)
        self._func_calls[name] += 1

    def _check_log(self, expected):
        """Check if observerd calls match expected ones.
        Expected values can be integer and iterables.
        Ranges may be defined with strings like '7-8'
        """
        for name, _ve in expected.items():
            ve = set()
            for v in flatten(list([_ve])):
                # allow ranges
                v = str(v).split('-')
                v.append(v[0])
                ve.update(range(int(v[0]), int(v[1]) + 1))

            vr = self._func_calls.get(name, None)
            if vr not in ve:
                self.reactor.stop()
                raise RuntimeError(f"Fuction {name} is expected to be called {ve} time, but where {vr}")


class Foo(_TestLayer):
    def __init__(self, states=None, transitions=None, context=None):
        super().__init__(states, transitions, context)

        self.b = 0

    def _setup_test_foo_1(self):
        states = {
            STATE_INIT: [[], [], ['hello']],
            STATE_READY: [[], ['ready'], []],
            STATE_END: [[], ['stop'], []],
        }
        transitions = {
        }
        return states, transitions, MERGE_ADD

    def _setup_test_foo_2(self):
        states = {
        }
        transitions = {
            STATE_READY: {
                EVENT_TERM: [
                    [STATE_READY, ['b <= 5'], ['not_yet']],
                    [STATE_READY, ['b > 5'], ['from_init_to_end', 'term']],
                ],
            },
        }
        return states, transitions, MERGE_REPLACE_EXISTING

    def timer(self, **kw):
        self.context['b'] += 1
        print(f">> timer: b={self.context['b']}")

    def hello(self, **kw):
        print(">> Hello!")
        self._log_function()

    def ready(self, **kw):
        print(">> Ready")
        self._log_function()

    def stop(self, **kw):
        print(">> Stop !!")
        self._log_function()

    def not_yet(self, key, **kw):
        print(f'>> Received: {key}, but not_yet()')
        self._log_function()

    def from_init_to_end(self, key, **kw):
        print(f'>> Received: {key}, OK shutdown now')
        self._log_function()

    def term(self, **kw):
        expected = {
            'from_init_to_end': 1,
            'hello': 1,
            'not_yet': 2,
            'ready': 12,
            'start': 1
        }
        self._check_log(expected)
        super().term(**kw)

class iRPNCalc(Layer):
    operations = {
        '+': operator.add,
        '-': operator.sub,
        '*': operator.mul,
        '/': operator.truediv,
        'neg': operator.neg,
    }

    def __init__(self, states, transitions):
        self.stack = []
        super().__init__(states=states, transitions=transitions)
        foo = 1

    def start(self, data, **kw):
        print("Hello World!!")

    def push(self, data, **kw):
        self.stack.append(data)

    def exec1(self, data, **kw):
        a = self.stack.pop()
        r = self.operations[data](a)
        self.stack.append(r)

    def exec2(self, data, **kw):
        b = self.stack.pop()
        a = self.stack.pop()
        try:
            r = self.operations[data](a, b)
            self.stack.append(r)
        except ZeroDivisionError:
            pass


class RPNCalc1(iRPNCalc):
    def __init__(self):
        # Simplier RPN, less states
        states = {
            STATE_INIT: [[], ['start'], []],
            'READY': QUITE_STATE,
            'PUSH': [[], ['push'], []],
            'EXEC1': [[], ['exec1'], []],
            'EXEC2': [[], ['exec2'], []],
            STATE_END: [[], ['bye'], []],
        }

        transitions = {
            'INIT': {
                None: [
                    ['READY', [], []],
                ],
            },
            'READY': {
                'input': [
                    ['PUSH', ['isinstance(data, int)'], []],
                    ['EXEC2', ["data in ('+', '-', '*', '/')", 'len(stack) >= 2'], []],
                    ['EXEC1', ["data in ('neg', )", 'len(stack) >= 1'], []],
                ],
                EVENT_TERM: [
                    [STATE_END, [], []],
                ],
            },
            'PUSH': {
                None: [
                    ['READY', [], []],
                ],
            },
            'EXEC1': {
                None: [
                    ['READY', [], []],
                ],
            },
            'EXEC2': {
                None: [
                    ['READY', [], []],
                ],
            },
        }
        super().__init__(states, transitions)

class RPNCalc2(iRPNCalc):
    def __init__(self):
        # Simplier RPN, less states
        states = {
            STATE_INIT: [[], ['start'], [], []],
            'READY': QUITE_STATE,
            STATE_END: [[], ['bye'], [], []],
        }

        transitions = {
            'INIT': {
                None: [
                    ['READY', [], []],
                ],
            },
            'READY': {
                'input': [
                    ['READY', ['isinstance(data, int)'], ['push']],
                    ['READY', ["data in ('+', '-', '*', '/')", 'len(stack) >= 2'], ['exec2']],
                    ['READY', ["data in ('neg', )", 'len(stack) >= 1'], ['exec1']],
                ],
                EVENT_TERM: [
                    [STATE_END, [], []],
                ],
            },
            STATE_END: {
            },
        }
        super().__init__(states, transitions)



class Clock(_TestLayer):

    def _setup_test_clock(self):
        states = {
        }
        transitions = {
            STATE_READY: {
                # set an additional timer
                'each:3,2': [
                    [STATE_READY, [], ['timer']],
                ],
            },
        }
        return states, transitions, MERGE_ADD

    def timer(self, key, **kw):
        elapsed = time() - self.t0
        print(f" > Timer {key}: {elapsed}")
        restart, offset = [int(x) for x in key[5:].split(',')]

        cycles = (elapsed - offset) / restart
        assert cycles - int(cycles) < 0.01


class Parent(_TestLayer):

    def _setup_test_parent(self):
        states = {
            'FOO': [[], ['bar'], []],
        }
        transitions = {
        }
        return states, transitions, MERGE_ADD

    def bar(self, **kw):
        pass

class Crawler(_TestLayer):
    """Dummy Web Crawler for testing dynamic channels creation and
    protocols.

    - a timer creates a new channel from time to time.
    - a timer use a free channel to make a request.
    - a timeout will term the reactor.

    """
    def __init__(self, states=None, transitions=None, context=None):
        super().__init__(states, transitions, context)
        self.channels = list()  # free channels
        self.working = list()  # in-use channels
        self.downloaded = 0

    def _setup_test_crawler(self):
        states = {
            'GET': [[], ['get_page'], []],
            'SAVE': [[], ['save_page'], []],
        }
        transitions = {
            STATE_READY: {
                'each:3,2': [
                    [STATE_READY, ['len(channels) <= 3'], ['new_channel']],
                ],
                'each:1,1': [
                    ['GET', ['len(working) <= 3 and downloaded < 10'], []],  # just to use a state
                ],
                'each:2,1': [
                    ['SAVE', ['len(working) > 3'], []],  # just to use a state
                ],
                'each:5,21': [
                    [STATE_READY, ['downloaded >= 10'], ['bye']],
                ],
            },
            'GET': {
                None: [
                    [STATE_READY, [], []],  # going back to READY
                ],
            },
            'SAVE': {
                None: [
                    [STATE_READY, [], []],  # going back to READY
                ],
            },
        }
        return states, transitions, MERGE_REPLACE_EXISTING

    def new_channel(self, **kw):
        print('  > new_channel')
        self._log_function()
        self.channels.append(False)

    def get_page(self, **kw):
        "Simulate a download page request"
        for i, working in enumerate(self.channels):
            if not working:
                self._log_function()
                print('  > get_page')
                self.channels[i] = True
                self.working.append(i)
                break

    def save_page(self, **kw):
        "Simulate that page has been downloaded and saved to disk"

        for worker, channel in reversed(list(enumerate(self.working))):
            if random.randint(0, 100) < 25:
                self._log_function()
                self.context['downloaded'] += 1
                print(f"  > save_page: {self.context['downloaded']}")
                self.channels[channel] = False
                self.working.pop(worker)

    def term(self, **kw):
        expected = {
            'get_page': '12-13',
            'new_channel': 4,
            'save_page': '10-13',
            'start': 1
        }
        self._check_log(expected)
        super().term(**kw)


class HashableEvents(Layer):
    """Test class for testing events using any hashable event
    - strings
    - tuples
    - integers/floats
    """
    def _setup_test_hashable_events(self):
        self.channels = list()  # free channels
        self.working = list()  # in-use channels

        states = {
        }
        transitions = {
            STATE_READY: {
                ('hello', 'world'): [
                    [STATE_READY, [], ['hello_world']],
                ],
                1: [
                    [STATE_READY, [], ['uno']],
                ],
            },
        }
        return states, transitions, MERGE_ADD

    def hello_world(self, **kw):
        print('  > hello_world')
        foo = 1

    def uno(self, **kw):
        print('  > uno')
        foo = 1


# -----------------------------------------------------
#  Atlas demo
# -----------------------------------------------------
class GraphExample(_TestLayer):
    def _setup_test_graph(self):
        states = {
            'ASK': [[], ['bar'], []],
            'WAIT': [[], [], []],
        }
        transitions = {
            STATE_READY: {
                'each:5,1': [
                    ['ASK', [], ['bar']],
                ],
            },
            'ASK': {
                None: [
                    ['WAIT', [], []],
                ],
            },
        }
        return states, transitions, MERGE_ADD

    def bar(self, **kw):
        pass


# -----------------------------------------------------
#  tests
# -----------------------------------------------------

#def test_layer():

    #foo = Foo()
    #reactor = _TestReactor()
    #reactor.attach(foo)
    ## reactor.graph()
    #reactor.run()
    #foo = 1

#def test_timeit():
    #population = [100, 100, 10]

    #states1 = dict()
    #populate1(states1, population, n=10000)

    #N = 1000000

    #i = 0
    #key = [str(random.randint(0, x)) for x in population]
    #t0 = time()
    #while i < N:
        #info = states1
        #for k in key:
            #info = info.get(k, {})
        #i += 1
    #t1 = time()

    #states2 = dict()
    #populate2(states2, population, n=10000)
    #key = [str(random.randint(0, x)) for x in population]

    #i = 0
    #key = [str(random.randint(0, x)) for x in population]
    #info = states2
    #t2 = time()
    #while i < N:
        #k = tuple(key)
        #info = states2.get(k, {})
        #i += 1
    #t3 = time()

    #import pandas as pd
    #t4 = time()
    #df_1 = pd.DataFrame()

    #speed1 = N / (t1 - t0)
    #speed2 = N / (t3 - t2)

    #print(f"{speed1}")  # around 28e6 loops/sec
    #print(f"{speed2}")  # around 40e6 loops/sec
    #print(f"{speed2/speed1}")  # aound 1.5 faster
    #print(f"Pandas: {t4-t3}")

#def test_await_vs_normal():
    #N = 10000000

    #def foo1():
        #return

    #async def foo2():
        #return

    #def timeit0(i):
        #t0 = time()
        #while i > 0:
            #foo1()
            #i -= 1
        #t1 = time()
        #return t1 - t0

    #async def timeit2(i):
        #t0 = time()
        #while i > 0:
            #await foo2()
            #i -= 1
        #t1 = time()
        #return t1 - t0

    #e1 = timeit0(N)
    #import asyncio
    #e2 = asyncio.run(timeit2(N))

    #speed1 = N / (e1)
    #speed2 = N / (e2)

    #print(f"{speed1}")  # around 11e6 loops/sec
    #print(f"{speed2}")  # around 5e6 loops/sec
    #print(f"{speed1/speed2}")  # aound x2 faster


#def test_clock():
    #reactor = _TestReactor()
    #clock = Clock()
    #reactor.attach(clock)
    #reactor.run()
    #foo = 1

#def test_hierarchy():
    #parent = Parent()

    #assert parent.states == {
        #'END': [[], ['bye'], []],
        #'FOO': [[], ['bar'], []],
        #'INIT': [[], [], ['start']],
        #'READY': [[], [], []]
    #}

    #assert parent.transitions == {
        #'END': {},
        #'INIT': {None: [['READY', [], []]]},
        #'READY': {
            #EVENT_QUIT: [['END', [], ['quit']]],
            #EVENT_TERM: [['READY', [], ['term']]],
            #'each:5,1': [['READY', [], ['timer']]],
            #'each:5,21': [['READY', [], ['bye']]]},
    #}

    #foo = 1


#def test_calc():
    #"""Compare two different STM definition styles
    
    #RPNCalc2: loop over same state doing actions on transitions
    #RPNCalc1: has more states and doing actions entering in state
    
    #Is supposed RPNCalc1 stylel should be faster than RPNCalc2 one
    
    #Finally, RPNCalc1 stats are saved on a csv file using speed_meter() helper
    #for comparison when changing STM internal libray.
    #"""

    #def monkey_calc(N):
        #for i in range(N):
            #r = random.randint(0, 8 + len(iRPNCalc.operations))
            #if r <= 9:
                #yield 'input', r
            #else:
                #ops = list(iRPNCalc.operations.keys())
                #yield 'input', list(iRPNCalc.operations)[r - 9]

        #foo = 1

    #N = 500000

    ## Testing RPNCalc1 definition
    #reactor = _TestReactor(monkey_calc(N))
    #calc = RPNCalc1()
    #reactor.attach(calc)
    #reactor.graph()

    #t0 = time()
    #reactor.run()
    #e1 = time() - t0
    #speed1 = N / e1
    #print(f'Speed: {speed1}')

    ## Just using speed_meter() helper for writedown
    ## RPNCalc1 stats
    
    #setup = """# This code must be executed for each iteration
#reactor = _TestReactor(monkey_calc(N))
#calc = RPNCalc1()
#reactor.attach(calc)
#"""
    #env = globals()
    #env.update(locals())

    #test = dict(
        #stmt='reactor.run()',
        #setup=setup,
        #globals=env,
        #number=1,
        #repeat=3,
        #N=N,
        #label='RPN1Calc speed'
    #)

    #r = speed_meter(**test)
    #print(r['speed'])

    ## Testing RPNCalc2 definition
    #reactor = _TestReactor(monkey_calc(N))
    #calc = RPNCalc2()
    #reactor.attach(calc)
    #reactor.graph()

    #t0 = time()
    #reactor.run()
    #e2 = time() - t0

    #speed2 = N / e2
    #print(f'Speed: {speed2}')

    #print(f"RPNCalc2 is {speed2/speed1:.4} times faster than RPNCalc1")
    #foo = 1


#def test_graph_layer():
    #monitor = GraphExample()
    #reactor = _TestReactor()
    #reactor.attach(monitor)
    #reactor.graph(view=False)
    #foo = 1

#def test_create_channel():
    #reactor = Reactor()
    #url = 'http://www.debian.org'

    ## create a protocol and transport without layer (persistent until reactor ends)
    #proto, trx = reactor.create_channel(url, factory=_TestBrowserProtcol)

    #reactor.run()
    #foo = 1

#def test_crawler():
    #reactor = Reactor()
    #crawler = Crawler()
    #reactor.attach(crawler)
    #reactor.run()
    #foo = 1

#def test_hashable_events():
    #def events():
        #yield ('hello', 'world'), None
        #yield 1, None
        #foo = 1

    #reactor = _TestReactor(events())
    #layer = HashableEvents()
    #reactor.attach(layer)
    #reactor.run()
    #foo = 1
    
#def test_decoders():
    #"""Use 2 Layers, one send a stream using random lengths
    #The other must recompone message before sending to reactor.
    #"""
    #foo = 1

if __name__ == '__main__':
    
    test_decoders()
    test_calc()
    
    # test_timeit()
    # test_layer()
    # test_await_vs_normal()
    test_clock()
    # test_hierarchy()
    # test_order_monitor()
    test_create_channel()
    test_crawler()
    # test_hashable_events()
    pass

