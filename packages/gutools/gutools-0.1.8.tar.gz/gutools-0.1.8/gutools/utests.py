"""Parse CSV alike data from different sources including:

- markdown tables (e.g. from documentation)


Future:
- csv
- excel

"""
import asyncio
import inspect
import sys
import time
import re
import pandas as pd
from datetime import timedelta as timedelta
from datetime import datetime

from io import StringIO
# import uuid
import random
import yaml

import parse  # https://github.com/r1chardj0n3s/parse

from gutools.tools import get_calling_function

_regx_eval = re.compile(r"(\<(.*)\>)")

_regx_param = re.compile(r"""
(?P<idx>[\*\s]+)?
(?P<format>
\{?
    (?P<param>[_a-z][^:\*\}]*)
    (:(?P<fmt>[^\*\}]*))?
\}?
)
(?P<idx2>[\*\s]+)?

""", re.VERBOSE | re.IGNORECASE)

m = _regx_param.match('*{seq:d}*')
print(m.groupdict())
m = _regx_param.match('{seq:d}')
print(m.groupdict())
m = _regx_param.match('*seq*')
print(m.groupdict())
m = _regx_param.match('seq')
print(m.groupdict())
m = _regx_param.match('{bid1}')
print(m.groupdict())
m = _regx_param.match('{_foo}')
print(m.groupdict())
m = _regx_param.match('{0}')
assert not m


default_converters = {'seq': int, 'p0': float, 'p1': float, 'date': datetime.fromisoformat,
              'type': float, 'amount': float, 'price': float,
              'lid': int, 'exp': float, 'fill': float,
              'uf': int, 'cf': int, 'cd': int, 'bid': int, }

# --------------------------------------------------------
# Markdown tables extractor
# --------------------------------------------------------

def apply_converters(row, conv, nan_error=False):
    for i, c in conv:
        try:
            row[i] = c(row[i])
        except:
            if nan_error:
                row[i] = pd.np.NaN

    # always convert NaN strings to np.nan
    for i, x in enumerate(row):
        if x in ('NaN', ):
            row[i] = pd.np.NaN
    return row


def parse_fields(row, header, env, nan_error=False):
    # 1 step: parse all rows known format and update context
    idx_pos = None
    for i, fmt in enumerate(header):
        try:
            d = _regx_param.match(fmt).groupdict()
            info = parse.parse(d['format'], row[i])
            if info:
                env.update(info.named)
                # we asume there's only 1 named params or at least, the result is the last one
                for key, value in info.named.items():
                    row[i] = value
            elif d['idx']:
                return None  # is an index and we can not parse value

        except Exception as why:
            if nan_error:
                row[i] = pd.np.NaN

    for i, t_value in enumerate(row):
        if isinstance(t_value, str):
            m = _regx_eval.match(t_value)
            if m:
                exp = m.group(2)
                try:
                    row[i] = eval(exp, env)
                except Exception as why:
                    foo = 1
    return row

def prepare_converters(columns, converters):
    conv = list()
    for i, field in enumerate(columns):
        c = converters.get(field)
        if c:
            conv.append((i, c))
    return conv

def parse_df_header(header):
    if isinstance(header, str):
        header = [scalar.strip() for scalar in header.strip().strip('|').split('|')]

    idx0 = idx1 = None
    header0 = list(header)

    for i, col in enumerate(header0):
        m = _regx_param.match(col)
        if m:
            d = m.groupdict()
            header0[i] = d['param']
            if d['idx']:
                idx0, idx1 = col, d['param']
        else:
            header0[i] = col

    header1 = list(header0)
    if idx1:
        header1.remove(idx1)

    return idx0, idx1, header0, header1

def set_df_index(df, header):
    idx0, idx1, _, _ = parse_df_header(header)
    if idx1:
        df.rename({idx0: idx1}, axis='columns', inplace=True)
        df.set_index(idx1, inplace=True)


def Markdown_extractor(content, converters=default_converters, env=None, nan_error=False, what=['table']):
    """Extact elements from MD formated content."""
    last = None
    context = dict()
    header_fmt = header0 = header1 = None
    env = env if env is not None else dict()

    stream = StringIO(content)

    while not stream.closed:
        rows = table_reader(stream)
        data = list()
        for header_fmt in rows:
            idx0, idx1, header0, header1 = parse_df_header(header_fmt)
            break
        else:
            break  # not header found, stop reading

        for row in rows:
            row = parse_fields(row, header_fmt, env)
            row and data.append(row)

        df = pd.DataFrame(data, columns=header0)
        if idx1:
            df.set_index(idx1, inplace=True)
        yield df

def table_reader(stream):
    """Parse a table in MD format.
    Returns header and all rows, then exit.
    The stream is moved forward to next MD content.
    """
    header = None
    for line in stream.readlines():
        row = [scalar.strip() for scalar in line.strip().strip('|').split('|')]

        # check if is a header start
        c = ''.join(row)
        if not header:
            if c:
                if not c.strip('-').strip(':'):
                    header = last
                    yield header
        else:
            if line.strip():
                yield row
            else:
                break
        last = row

def df_asdict(df):
    name = df.index.name
    for idx, serie in df.iterrows():
        d = dict(zip(serie.index, serie.values))
        d[name] = idx
        yield d

def list_asdict(lines, header):
    for row in lines:
        d = dict(zip(header, row))
        yield d

def twin_iter(a, b):
    keys = list(a.keys())
    keys.sort()
    for k in keys:
        yield k, a[k], b[k]

class Match(object):
    def __init__(self, df, content, env):
        self.df = df
        # self.df.reset_index()   # to add index into context values
        self.content = content
        self.env = env

    def match(self):
        for step in ['capture', 'eval']:
            stream = StringIO(self.content)
            lines = table_reader(stream)

            for header in lines:
                idx0, idx1, header0, header1 = parse_df_header(header)
                break
            env = self.env

            # iterate df rows and template rows one by one
            for i, (e_row, t_row) in enumerate(
                    zip(df_asdict(self.df), list_asdict(lines, header0))):

                a, b = list(e_row.keys()), list(t_row.keys())
                a.sort()
                b.sort()
                assert a == b

                # pass 1: cast to same type and capture
                env.update(e_row)

                pending = list()
                for key, e_value, t_value in twin_iter(e_row, t_row):
                    # - ignore <> expressions
                    m = _regx_eval.match(t_value)
                    if m:
                        pending.append((key, m.group(2)))
                        continue

                    # - try to capture variable from e_row
                    m = _regx_param.match(t_value)
                    if m:
                        d = m.groupdict()
                        env[d['param']] = t_row[key] = e_row[key]
                        continue

                    # - try to cast value to same class. NaN is convertted as well
                    # e_value = e_row[key]
                    try:
                        t_row[key] = e_value.__class__(t_value)
                        continue
                    except Exception as why:
                        print(why)
                        foo = 1

                if step in ('eval', ):
                    # pass 2: expand <vars>
                    for key, exp in pending:
                        try:
                            t_row[key] = eval(exp, env)
                        except Exception as why:
                            foo = 1

                    # compare
                    if t_row != e_row:
                        diff = list()
                        diff.append(f"{'key':9} {'Expected':>8} --- {'Observed':<8}")
                        for key, e_value, t_value in twin_iter(e_row, t_row):
                            if e_value != t_value:
                                if isinstance(e_value, float) and not pd.np.isnan(e_value):
                                    diff.append(f"- {key:6}: {e_value:>8} != {t_value:<8}")

                        diff = '\n'.join(diff)
                        error = f"""*** ERROR ***
    {self.df}

    row: {i}
    {diff}
                        """
                        print(error)
                        return False
        return True



def iter_df(df, converters=default_converters, nan_error=False):
    conv = list()

    # prepare converters
    if df.index.name:
        fields = [df.index.name] + list(df.columns)
        conv = prepare_converters(fields, converters)
    else:
        fields = list(df.columns)
        conv = prepare_converters(fields, converters)

    for idx, row in df.iterrows():
        row = [idx] + list(row)
        row = apply_converters(row, conv, nan_error)
        yield row



# --------------------------------------------------------
# Check internal table structures in the middle of algorithm
# --------------------------------------------------------

async def inject_events(df, hub, key, klass, converters=default_converters, rate=10,
                        pub_keys=['{key}', '/test{key}', ]):
    """Inject events from a df into Hub using a key
    converting rows values prior building a klass.

    Allow
    """
    ctx = locals()
    pub_keys = [k.format(**ctx) for k in pub_keys]

    s = 1 / (rate * len(pub_keys))
    s = 1 / rate

    for row in iter_df(df, converters):
        record = klass(*row)
        # print(record)

        for i, k in enumerate(pub_keys):
            if i > 0:
                priority = 15
            else:
                priority = 1
                await asyncio.sleep(s)

            join = asyncio.Event()
            hub.publish(k, record, priority=priority, join=join)
            await join.wait()
            foo = 1
    foo = 1


async def inject_events_using_date(df, hub, key, klass, date='date', converters=None, speed=1):
    """Inject events from a df into Hub using a key
    converting rows values prior building a klass
    """

    now = None
    for row in iter_df(df, converters):
        record = klass(*row)
        when = getattr(record, date)

        if now:
            dt = when - now
            delay = dt.seconds / speed
            await asyncio.sleep(delay)

        now = when
        hub.publish(key, record)


async def await_until(condition, timeout=10, sampling=10, extra=0):
    # func = get_calling_function()
    frame = sys._getframe(1)
    context = dict(frame.f_locals)

    t0 = time.time()
    s = 1 / sampling
    while time.time() - t0 < timeout:
        try:
            r = eval(condition, context)
            if r:
                break
        except:
            pass
        await asyncio.sleep(s)
    else:
        raise TimeoutError("wait_until() failled")

    await asyncio.sleep(extra)



def parse_df_states(states, converters=default_converters):
    """Parse a dict of internal states in Markdown to check internal status
    during the algorithm evolution.
    """
    df_states = dict()
    for seq, state in states.items():
        for df in Markdown_extractor(state, converters):
            df_states[seq] = df
    return df_states



class InternalStatusMonitor(object):
    def __init__(self, hub, key, expected_status, obj, df_attr='df', seq_attr='seq', env=None):
        self.hub = hub
        self.key = f'/test{key}'
        self.expected_status = expected_status
        self.obj = obj  # where is the df to be checked
        self.df_attr = df_attr
        self.seq_attr = seq_attr

        self.env = env or dict()
        self.result = None

        self.hub.subscribe(self.key, self.check_df_status)

    async def check_df_status(self, key, data):
        if self.result:
            return  # don't process any check when an error is happend

        value = getattr(data, self.seq_attr)
        expected = self.expected_status.get(value)
        if expected is not None:
            observed = getattr(self.obj, self.df_attr)

            m = Match(observed, expected, self.env)
            r = m.match()
            if not r:
                self.result = RuntimeError(f"*** ERROR: internal status differ in {self.seq_attr}: {value}, data: {data}")
                print(observed)
                print(expected)
                raise self.result
            else:
                print(f"OK: internal status {value} match")
                foo = 1  # ok
        foo = 1


async def execute_supervision_test(states, events, record_klass, key, instance, converters=default_converters, env=None):

    app = instance.app
    hub = app.hub
    await app.start()

    # df_states = parse_df_states(states, converters)

    t0 = time.time()
    supervisor = InternalStatusMonitor(hub, key, states, instance, env=env)

    for df in Markdown_extractor(events, env=env):
        # remove rows with no sequence (NaN)
        # df = df[df.index > '']
        # await inject_events(df, hub, key, klass, converters, rate=4)
        # await inject_events_using_date(df, hub, key, klass, 'date', converters, speed=10)
        await inject_events(df, hub, key, record_klass, rate=1000)

    # await await_until('hub._queue.empty()', extra=0.25)
    elapsed = time.time() - t0
    print(f"Elapsed: {elapsed}")
    if supervisor.result:
        raise supervisor.result

    await app.stop()

    foo = 1

class InjectorTest(object):
    def __init__(self, app, events, expected, env=None):
        self.app = app
        self.events = events
        self.expected = expected
        self.env = env

        # runtime
        self.result = None
        self.test_key = None
        self.checked = None

    async def run(self, timers=True):
        """
        timers = True : timers are silenced but defined in events
        """
        app = self.app
        hub = app.hub

        self.test_key = f'/test/run/{random.randint(0, 10**6)}'
        hub.subscribe(f'{self.test_key}/.*', self._check_status)

        await app.start()

        if not timers:  # avoid install timers but mine
            hub._task_timers.cancel()

        pub_keys = ['{key}', f'{self.test_key}/{{stage}}{{key}}']

        t0 = time.time()
        for events in Markdown_extractor(self.events, env=self.env):
            await self.inject_events(events, pub_keys, rate=1000)

        elapsed = time.time() - t0
        print(f"Elapsed: {elapsed}")
        if self.result:
            raise self.result

        await app.stop()
        foo = 1

    async def inject_events(self, events, pub_keys, rate=10):
        hub = self.app.hub
        ctx = locals()
        s = 1 / rate
        env = self.env

        self.checked = asyncio.Event(loop=hub._loop)
        join = asyncio.Event(loop=hub._loop)

        for seq, stage, key, message, date in iter_df(events):
            await asyncio.sleep(s)
            try:
                m = _regx_eval.match(message)
                if m:
                    message = eval(m.group(2), env)
                else:
                    message = yaml.load(message)
            except Exception as why:
                foo = 1

            for i, k in enumerate(pub_keys):
                k = k.format(**locals())
                self.checked.clear()
                join.clear()
                hub.publish(k, message, join=join)
                await join.wait()  # wait event has been processed

            await self.checked.wait()  # wait check has been done
            foo = 1

        foo = 1

    async def _check_status(self, key, data):
        try:
            if self.result:
                return  # don't process any check when an error is happend

            env = self.env
            stage = key.split(self.test_key)[1].split('/')[1]

            expected = self.expected.get(stage) or {}
            for exp, status in expected.items():
                try:
                    observed = eval(exp, env)
                except Exception as why:
                    foo = 1

                m = Match(observed, status, env)
                r = m.match()

                if not r:
                    self.result = RuntimeError(f"*** ERROR: internal status differ in {self.seq_attr}: {value}, data: {data}")
                    print(observed)
                    print(status)
                    raise self.result
            else:
                print(f"Internal status '{stage}' Ok")
                foo = 1  # ok
        finally:
            self.checked.set()


    # ------------------------------------------------------
    # helpers
    # ------------------------------------------------------
    def _no_timers_subscribe(self, pattern, callback, duplicate=False, single=False):
        uri_ = parse_uri(pattern)
        if uri_['scheme'] in ('timer', ):
            return
        self.org_subscribe(pattern, callback, duplicate, single)




# -----------------------------------------------------
#  timeit
# -----------------------------------------------------
import timeit
import os
from datetime import datetime
def speed_meter(N=None, label=None, csv_file='~/speed_meter.csv', **test,):
    """Do a performance test, and write stats to a file for comparisson"""
    
    label = label or '{stmt}'.format(**test)
    elapsed = timeit.repeat(**test)
    elapsed.sort()
    n = test.get('repeat', 5) // 3 + 1  # take 1/3 of the best results
    elapsed = sum(elapsed[:n]) / n
    if N:
        speed = N / elapsed
    else:
        speed = None

    test['label'] = label
    test['speed'] = speed
    test['elapsed'] = elapsed
    test['now'] = now = datetime.now()
    test['now_txt'] = now_txt = now.strftime('%Y-%m-%dT%H:%M:%S')

    _debug_ = set(sys.executable.split(os.path.sep)).\
        intersection(set(['wingdb']))
    _debug_ = len(_debug_) > 0

    test['username']= os.getenv('USERNAME')
    path = csv_file.format(**test)
    path = os.path.expanduser(path)
    path = os.path.expandvars(path)
    with open(path, mode='a') as f:
        line = f'{now_txt:}, {N}, {elapsed:1.5f}, {speed:e}, {label}, {_debug_}\n'
        f.write(line)
    return test


# -----------------------------------------------------
#  speed ratios
# -----------------------------------------------------
def speed_ratios(cycles=10**5, passes=8, best=4, console=True,
                 print_report=True, assertions=None,
                 **info):

    """
    Performs some speed tests, find the fastest, compute seed ratios and 
    human readable messages.
    
    It can do some assertions as well.
    
    Example:
            result = speed_ratios(
            cycles=1,
            console=False,
            print_report=True,
            assertions=dict(ratios=[['strategy_1', 'strategy_2', '>5']]),
            strategy_1=dict(func=strategy_1, kw=profile),
            strategy_2=dict(func=strategy_2, kw=profile),
        )
        
    """
    elapsed = dict()
    speed = dict()
    ratios = dict()
    values = dict()
    
    reference = 10**3

    import gc
    import random
    import itertools

    # normalized test info
    for label, task in list(info.items()):
        if not isinstance(task, dict):
            info[label] = task = dict(func=task)
        task.setdefault('args', tuple())
        task.setdefault('kw', dict())

    # execute tests passes
    _info = list(info.items())
    gc.disable()
    for p in range(passes):
        random.shuffle(_info)
        for label, task in _info:
            n = task.get('cycles', cycles)
            func = task['func']
            args, kw = task['args'], task['kw']
            t0 = time.time()
            for _ in range(n):
                v = func(*args, **kw)
            e = time.time() - t0
            # normalize speed and elapsed
            s = n / e / reference
            e *= reference / n
            if console:
                print(f"pass: {p:3}, testing: {label:10}({kw}) for {n:7} cycles, normalized speed: {s:1.5} block[{reference}]/seg")

            elapsed.setdefault(label, list()).append(e)
            speed.setdefault(label, list()).append(s)
            values[label] = v

    gc.enable()
    gc.collect()
    for label, e in list(elapsed.items()):
        e.sort()
        e = e[:best]
        elapsed[label] = sum(e) / len(e)

    for label, s in list(speed.items()):
        s.sort()
        s.reverse()
        s = s[:best]
        speed[label] = sum(s) / len(s)

    # compute ratios matrix
    for x, y in itertools.product(info, info):
        ratios.setdefault(x, dict())[y] = elapsed[x] / elapsed[y]

    # compute winners (podium)
    podium = list(elapsed.keys())
    podium.sort(key=elapsed.get)

    # writedown human readable messages
    messages = [f"'{podium[0]}' is {elapsed[key]/elapsed[podium[0]]:1.3} faster than '{key}'" for key in podium[1:]]

    # compare result sizes
    sizes = list()
    for label in podium:
        try:
            sizes.append((label, len(values[label])))
        except:
            sizes.append((label, None))

    result = dict(podium=podium, values=values, elapsed=elapsed, speed=speed,
                  ratios=ratios, messages=messages, sizes=sizes)
    
    if print_report:
        print("-" * 40)
        print('\n'.join(result['messages']))
        
    assertions = assertions or {}
    for test1, test2, condition in assertions.get('ratios', {}):
        r = ratios[test1][test2]
        cond = f"{r}  {condition}"
        c = eval(cond)
        msg = f"ratio[{test1}][{test2}] = {r:1.3} {condition} = {c}"
        if print_report:
            print(msg)
        assert c, msg
        
    return result



# --------------------------------------------------------
# Temporal files
# --------------------------------------------------------
