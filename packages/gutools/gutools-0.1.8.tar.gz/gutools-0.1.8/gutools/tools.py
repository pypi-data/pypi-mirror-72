# -*- coding: utf-8 -*-
"""This module contains basic methods and definitions that would be used
by other `gutools` modules.
"""

import sys
import os
import string
import asyncio
import hashlib
import uuid
import random
import inspect
import types
import fnmatch
import re
import yaml
import time
import json
import stat
import math
import traceback
import dateutil.parser as parser
from dateutil.relativedelta import relativedelta
import itertools

from datetime import datetime
from codenamize import codenamize
from urllib import parse
from io import StringIO
from functools import partial
from collections import OrderedDict
from collections.abc import Iterable
from weakref import WeakKeyDictionary, WeakValueDictionary, WeakSet
from gutools.colors import *
from pprint import pformat

# -------------------------------------------------------
#  asyncio nested loops
# -------------------------------------------------------
# import nest_asyncio
# nest_asyncio.apply()

# -----------------------------------------------------------
# random strings, values and containers
# -----------------------------------------------------------


def random_name(size=10, mixed_case=False, first_letter=True):
    if mixed_case:
        domain = string.digits + string.ascii_lowercase + string.ascii_uppercase + '_'
    else:
        domain = string.digits + string.ascii_lowercase + '_'

    result = ''.join(random.choice(domain) for _ in range(size))
    if first_letter:
        result = random.choice(domain[10:]) + result[1:]
    return result


def random_value(size=10, options=[str, bytes, int, float, bool]):
    t = random.choice(options)

    # try to expand type 't'
    if t == str:
        domain = string.digits + string.ascii_letters + '_'
        return ''.join(random.choice(domain) for _ in range(size))
    if t == bytes:
        result = ''.join([chr(random.randint(0, 255)) for _ in range(size)])
        return bytes(result, 'utf-8')
    if t == int:
        return random.randint(-size, +size)
    if t == float:
        return (random.random() - 0.5) * size * 2
    if t == bool:
        return random.choice([True, False])

    if t == 'date':  # preserve some fields
        return datetime.now().replace(
            month=random.randint(1, 12),
            day=random.randint(1, 28),
            hour=random.randint(0, 23),
            minute=random.randint(0, 59),
        )
    # otherwise return the option
    return t


def random_dict(length=20, size=10, options=[str, bytes, int, float, bool]):
    result = dict()
    for _ in range(length):
        key = random_name()
        value = random_value(size=size, options=options)
    return result


def random_specific_dict(**pattern):
    result = dict()
    for name, klass in pattern.items():
        if isinstance(klass, (list, tuple, set)):
            result[name] = random_value(options=klass)
        else:
            result[name] = random_value(options=[klass])
    return result


# -----------------------------------------------------------
# Misc converters handling
# -----------------------------------------------------------
def to_camel(exp):
    if isinstance(exp, (tuple, list, )):
        return exp.__class__([to_camel(k) for k in exp])
    if isinstance(exp, str):
        return ' '.join([t[0].upper() + t[1:] for t in exp.split()])


def Str(item):
    "Extended String converter"
    if isinstance(item, bytes):
        return item.decode('UTF-8')
    return str(item)


def Float(item):
    "Extended Float converter"
    return float(item or 0)


def Int(item):
    "Extended Float converter"
    return int(item or 0)


def Date(item):
    return parser.parse(item)


# -----------------------------------------------------------
# Base Item class
# -----------------------------------------------------------

class Item():
    """Just a container to Store data"""

    __hash_exclude__ = []

    def __getkeys__(self):
        keys = []
        for klass in self.__class__.__mro__:
            keys.extend(getattr(klass, '__slots__', []))
        return keys

    def __getstate__(self):
        state = dict([(k, getattr(self, k, None)) for k in self.__getkeys__()])
        #state['<klass>'] = self.__class__.__name__
        return state

    def __setstate__(self, state):
        #klass = state.pop('<klass>')
        #assert klass == self.__class__.__name__
        for k, v in state.items():
            setattr(self, k, v)

    def __str__(self):
        keys = self.__getkeys__()
        fields = ', '.join([f"{key}: {getattr(self, key, None)}" for key in keys])
        return f'{self.__class__.__name__}: {fields}'

    def aslist(self):
        keys = self.__getkeys__()
        return [f"{getattr(self, key, None)}" for key in keys]

    def soft(self, **kw):
        for k, v in kw.items():
            if getattr(self, k, None) is None:
                setattr(self, k, v)

    def hash(self):
        state = self.__getstate__()
        for k in self.__hash_exclude__:
            state.pop(k)
        m = hashlib.md5(bytes(str(state), 'utf-8'))
        return m.hexdigest()

    def clone(self, **kw):
        """Clone the object allowing an update"""
        new = self.__class__()  # default constructor must be defined
        for k in self.__getkeys__():
            setattr(new, k, kw.get(k, getattr(self, k)))
        return new



# -----------------------------------------------------------
# Containers
# -----------------------------------------------------------
TYPES = []
for k in types.__all__:
    klass = getattr(types, k)
    try:
        if isinstance(TYPES, klass):
            pass
        TYPES.append(klass)
    except Exception as why:
        pass
TYPES = tuple(TYPES)

BASIC_TYPES = tuple([type(None), int, float, str, bytes, ])
DATETIME_TYPES = tuple([datetime, relativedelta])
CONTAINERS_TYPES = tuple([dict, list, tuple])

BASIC_TYPES_EXT = tuple(list(BASIC_TYPES) + list(CONTAINERS_TYPES) + list(DATETIME_TYPES) + [Item])
ITERATOR_TYPES = tuple([type({}.keys()), type({}.values()), type({}.items())] + list(CONTAINERS_TYPES))
GENERATOR_TYPES = tuple([types.GeneratorType, ])
ITERATOR_TYPES_EXT = tuple(list(ITERATOR_TYPES) + list(GENERATOR_TYPES))
CALLEABLE_TYPES = tuple([types.MethodType, types.FunctionType, types.LambdaType])

# -----------------------------------------------------------
# URI handling
# -----------------------------------------------------------
reg_uri = re.compile(
    r"""
    (
    (?P<fscheme>
       (?P<direction>[<|>])?(?P<scheme>[^:/]*))
    ://
    (?P<fservice>
       (
            (?P<auth>
               (?P<user>[^:@/]*?)
               (:(?P<password>[^@/]*?))?
            )
        @)?
       (?P<host>[^@:/?]*)
    )
    (:(?P<port>\d+))?
    )?

    (?P<path>/[^?]*)?
    (\?(?P<query>[^#]*))?
    (\#(?P<fragment>.*))?
    """,
    re.VERBOSE | re.I | re.DOTALL)


def parse_uri(uri, bind=None, **kw):
    """Extended version for parsing uris:

    Return includes:

    - *query_*: dict with all query parameters splited

    If `bind` is passed, *localhost* will be replace by argument.

    """
    m = reg_uri.match(uri)
    if m:
        for k, v in m.groupdict().items():
            if k not in kw or v is not None:
                kw[k] = v
        if bind:
            kw['host'] = kw['host'].replace('localhost', bind)
        if kw['port']:
            kw['port'] = int(kw['port'])
            kw['address'] = tuple([kw['host'], kw['port']])
        if kw['query']:
            kw['query_'] = dict(parse.parse_qsl(kw['query']))

    return kw


def build_uri(fscheme='', direction='', scheme='',
              host='', port='', path='',
              query='', fragment='', **kw):
    """Generate a URI based on individual parameters"""
    uri = ''
    if fscheme:
        uri += fscheme
    else:
        if not direction:
            uri += scheme
        else:
            uri += f'{direction}{scheme}'
    if uri:
        uri += '://'

    host = host or f'{uuid.getnode():x}'
    uri += host

    if port:
        uri += f':{port}'
    if path:
        uri += f'{path}'
    if query:
        uri += f'?{query}'
    if fragment:
        uri += f'#{fragment}'

    return uri


def expand_uri(uri):
    if isinstance(uri, str):
        uri = parse_uri(uri)
    uri['path'] = expandpath(uri['path'])

    return build_uri(**uri)


def combine_uris(root, child, extend={'path': True}, build=True):
    if isinstance(root, str):
        root = parse_uri(root)
    else:
        root = dict(root)
    if isinstance(child, str):
        child = parse_uri(child)

    for key, value in child.items():
        if extend.get(key):
            value = f"{root.get(key) or ''}{value}"
        if value:
            root[key] = value

    if build:
        root = build_uri(**root)
    return root


def replace_uri(uri, klass=None, **fields):
    kw = parse_uri(uri)
    if klass:
        fields['fscheme'] = snake_case(klass.__name__, separator="-")
    kw.update(fields)
    return build_uri(**kw)


def get_self_uri(item, **defaults):
    """Try to create a fingerprint of item using all basic
    types that represent the item at this point.
    """
    fingerprint = {k: v for (k, v) in flatdict(item.__dict__).items()
                   if isinstance(v, BASIC_TYPES_EXT)}

    klass = snake_case(item.__class__.__name__, separator='-')
    fingerprint['__class__'] = klass
    fingerprint = '|'.join([str(i) for i in fingerprint.items()])
    path = f"/{codenamize(fingerprint, join='_', hash_algo='sha1')}"

    defaults.setdefault('scheme', klass.lower())
    defaults.setdefault('host', f'{uuid.getnode():x}')
    defaults.setdefault('path', path)

    uri = build_uri(**defaults)
    return uri


# --------------------------------------------------------------------
# iterators helpers
# --------------------------------------------------------------------
def round_robin(*iterators):
    """Chain all iterators extracting an element alternatvily
    from the 1st generator, the 2dn from the 2nd generator and so on.

    The generator list is cycled and a generator is removed when exahusted.

    """
    def foo_gen(container):
        for item in container:
            yield item

    stack = []
    for gen in iterators:
        if isinstance(gen, CALLEABLE_TYPES):
            gen = gen()
        if isinstance(gen, ITERATOR_TYPES):
            gen = foo_gen(gen)

        stack.append(gen)

    while stack:
        gen = stack.pop(0)
        for item in gen:
            yield item
            stack.append(gen)
            break
    foo = 1


def snake_case(name, separator='_'):
    s2 = f"\\1{separator}\\2"
    s1 = re.sub('(.)([A-Z][a-z]+)', s2, name)
    return re.sub('([a-z0-9])([A-Z])', s2, s1).lower()

# containers


def dset(d, key, value, *args, **kw):
    if key not in d:
        if args or kw:
            value = value(*args, **kw)
        d[key] = value
    return d[key]


# next_lid = random.randint(-10**5, 10**5)
next_lid = random.randint(0, 10**5)


def new_uid():
    global next_lid
    next_lid += 1
    return next_lid  # TODO: remove, just debuging
    # return uidfrom(next_lid)


def flatten(iterator, klass=None):
    if not isinstance(iterator, Iterable):
        yield iterator
        return
    # from https://stackoverflow.com/questions/2158395/flatten-an-irregular-list-of-lists
    for item in iterator:
        if isinstance(item, Iterable) and not isinstance(item, (str, bytes)):
            yield from flatten(item)
        elif klass is None or isinstance(item, klass):
            yield item


def deep_search(item, patterns, result=None):
    """Explore deeply elements hierchachy searching items from
    certain classes.
    """
    if result is None:
        result = dict()

    remain = [item]

    # TODO: avoid circular references
    used = set()
    while remain:
        item = remain.pop(0)
        idx = id(item)
        if idx in used:
            # print('remain[{}] : {} : <{}> : {}'.format(len(remain), klass, holder, idx))
            continue
        used.add(idx)

        klass = item.__class__.__name__
        holder, idx = patterns.get(klass, (None, None))

        # print('remain[{}] : {} : <{}> : {}'.format(len(remain), klass, holder, idx))
        if idx:
            # found an item of interest.
            holder = holder or klass
            key = getattr(item, idx)
            if key is not None:
                result.setdefault(holder, dict())[key] = item
                # print('>> [{}][{}] = {}'.format(holder, key, klass))
                foo = 1

        if isinstance(item, dict):
            # remain.extend(item.keys())
            remain.extend(item.values())
        elif isinstance(item, (list, tuple, set)):
            remain.extend(item)
        elif hasattr(item, '__dict__'):
            remain.append(item.__dict__)
        elif hasattr(item, '__slots__'):
            remain.append(dict([(k, getattr(item, k, None)) for k in item.__slots__]))
        else:
            foo = 1  # discard item, we don't know how to go deeper

    return result

# --------------------------------------------------------------------
# containers helpers
# --------------------------------------------------------------------


def walk(container, root=tuple(), includes={}, excludes={}, keys_included=[], keys_excluded=[]):
    """Walk recursive for an arbitrary container """
    keys_included = [re.compile(reg) if isinstance(reg, str) else reg for reg in keys_included]
    keys_excluded = [re.compile(reg) if isinstance(reg, str) else reg for reg in keys_excluded]

    def ignore(*path):
        foo = 1
        foo = list()
        for k in deep_chain(path):
            foo.append(str(k))
        path = f"/{'/'.join(foo)}"
        foo = 1
        # ---------------------------------------
        # check key filters
        # ---------------------------------------
        for reg in keys_excluded:
            if reg.match(path):
                return True  # ignore this key

        ign = True
        for reg in keys_included:
            if not reg.match(path):
                ign = False  # accept this key
                break
        else:
            ign = False
        return ign

    def buid_key(*keys):
        "creare a key using the right factory"

        # if factory in (tuple, ):
            # keys = list(flatten(keys))
            # return factory(keys)
        # elif factory in (str, ):
            # return '/'.join([factory(k) for k in keys])
        # else:
            # raise RuntimeError('Unknown factory type')
        results = list(keys[0])
        results.extend(keys[1:])
        return tuple(results)

    if ignore(root):
        return

    if isinstance(container, dict):
        func = container.items
        # yield '{}/'.format(root, ), '<{}>'.format(container.__class__.__name__)
        yield buid_key(root, ), '<{}>'.format(container.__class__.__name__)
    elif isinstance(container, (list, tuple)):
        def func(): return enumerate(container)
        yield buid_key(root, ), '<{}>'.format(container.__class__.__name__)
    else:
        # TODO: apply includes/excludes
        yield root, container  # container is a single item or object
        return

    # EXCLUDES
    recursive, match, same_klass = 0, 0, 0
    to_exclude = set()
    valid_items = dict()
    for key, item in func():
        if ignore(root, key):
            continue

        valid_items[key] = item
        # ---------------------------------------
        # continue
        # ---------------------------------------
        for klass, info in excludes.items():
            if not isinstance(item, klass):
                continue
            same_klass += 1
            for attr, filters in info.items():
                value = getattr(item, attr)
                if isinstance(value, CONTAINERS_TYPES):
                    recursive += 1
                    continue
                results = [f(value) for f in filters]
                if any(match):
                    match += 1
                    to_exclude.add(key)
                match += any(results)

    if recursive == 0 and match == 1 and same_klass == 1:
        # discard the whole container because there is 1 single element
        # that match the excludes and the rest of element are related with
        # different klasses (e.g. a tuple containing related information)
        return

    # TODO: coding 'includes' filters

    # RECURSIVE exploring
    for key, item in valid_items.items():
        if key in to_exclude:
            continue
        new_key = buid_key(root, key)

        if isinstance(item, CONTAINERS_TYPES):
            yield from walk(item, new_key, includes, excludes, keys_included, keys_excluded)
        # elif item.__class__ is not type.__class__ and hasattr(item, '__getstate__'):
            #state = item.__getstate__()
            # if state.get('<klass>', None):
                # yield from walk(state, new_key, includes, excludes, keys_included, keys_excluded)
            # else:
                # yield new_key, item
        else:
            yield new_key, item


def dive(container, key, stop_before=0, default_container=dict):
    keys = list(key)
    if stop_before > 0:
        rkey = keys[-stop_before]
        keys = keys[:-stop_before]

    if not keys:
        key = key[-1]

    while keys:
        key = keys.pop(0)
        if key in container:
            container = container.setdefault(key, default_container())
        else:
            break

    assert len(keys) == 0
    if stop_before > 0:
        return container, rkey
    return container, key


class DELETE_ITEM:
    """Item interpreted as REMOVE element"""


def divepush(container, key, item, merge=True, default_container=dict):
    """Set an element in a nested container array"""
    parent = container
    for key in key:
        parent, container = container, container.setdefault(key, default_container())

    if item is not DELETE_ITEM:
        if key is not None:
            if merge == False:
                parent[key] = item
            elif isinstance(container, BASIC_TYPES):
                parent[key] = item
            elif len(container) == 0:
                parent[key] = item
            elif len(item) == 0:
                foo = 1
            else:
                parent[key] = item
    else:
        parent.pop(key, None)

    return parent


def rebuild(walk_iterator, default_converter=None, default_container=dict,
            key_converters={}, container_converters={}, converters={}, result=None):
    """rebuild a tree structure from walk result"""
    # if factory in (str, ):
        # key_converters = dict([re.compile(k, re.I | re.DOTALL), v] for k, v in key_converters.items())

    merge = False if result is None else True

    def new_container(item):
        """Try to get the container described in the item string:
        <list> : return the list class
        <dict> : return the dict class
        """

        if isinstance(item, str) and len(item) > 2 \
           and item[0] == '<' and item[-1] == '>':
            klass = item[1:-1]  # the klass name
            try:
                klass = eval(klass)
            except Exception:
                klass = default_container  # as default building container for non-dict alike containers
            return klass

    convert = dict()
    for key, item in walk_iterator:
        klass = new_container(item)  # try to guess if is a container
        if klass is not None and not issubclass(klass, dict):
            convert[key] = klass  # for later converting the container
            klass = default_container  # as default building container for non-dict alike containers

            parent, parent_key = dive(result, key, 1)
            assert parent_key == key[-1]
            if isinstance(parent.setdefault(parent_key, default_container()), (tuple, list)):
                parent[parent_key] = {i: v for i, v in enumerate(parent[parent_key])}

        if klass:
            item = klass()

        conv = converters.get(item.__class__, default_converter)
        if conv:
            item = conv(item)

        if not key:
            if result is None:
                result = item
            continue

        assert result is not None, "root element must be found before any other"

        divepush(result, key, item, merge)
    # we need to convert some nodes from botton-up to preserve
    # indexing with keys as str, not integers in case of list/tuples
    convert_keys = list(convert.keys())
    convert_keys.sort(key=len, reverse=True)

    for key in convert_keys:
        klass = convert[key]
        parent_container, parent_key = dive(result, key, 1)
        container = parent_container[parent_key]
        keys = list(container.keys())

        if issubclass(klass, (list, tuple)):
            keys.sort(key=lambda x: int(x))
        else:
            keys.sort()

        values = [container[k] for k in keys]
        item = klass(values)
        # chain converters
        for conv in container_converters.get(klass, []):
            item = conv(key, item)

        parent_container[parent_key] = item

    return result


def unflattern(iterator, keys, container=None):
    """Build a structure info from a iterator, using some keys that
    acts as indexes of the structure.

    The value is taken from item itself.
    """
    container = container or dict()
    for item in iterator:
        parent, children = None, container
        for key in keys:
            if isinstance(item, (list, tuple)):
                item = list(item)
                key = item.pop(key)
            elif isinstance(item, dict):
                item = dict(item)
                key = item.pop(key)
            else:
                key = getattr(item, key)
            parent, children = children, children.setdefault(key, dict())
        parent[key] = item
    return container


def linear_containers(*iterable):
    remain = list(iterable)
    while remain:
        item = remain.pop(0)
        if isinstance(item, (dict, list, tuple, set)):
            remain.extend(item)
        else:
            yield item


def deep_chain(*iterable):
    remain = list(iterable)
    while remain:
        item = remain.pop(0)
        if isinstance(item, BASIC_TYPES):
            yield item
        elif isinstance(item, dict):
            remain.extend(item.keys())
            # remain.extend(item.values())
        elif isinstance(item, (list, tuple, set)):
            remain.extend(item)
        elif hasattr(item, '__dict__'):
            remain.append(item.__dict__)
        elif hasattr(item, '__slots__'):
            remain.append(dict([(k, getattr(item, k, None)) for k in item.__slots__]))
        else:
            foo = 1  # discard item, we don't know how to go deeper


def update_structure(target, source):
    rebuild(walk(source), result=target)


def serializable_container(container, includes={}, excludes={}, keys_included=[], keys_excluded=[], ignore=True):
    def _filter(container):
        for path, v in walk(container, includes=includes, excludes=excludes, keys_included=keys_included, keys_excluded=keys_excluded):
            if v in ('<tuple>', ):
                yield path, '<list>'
            elif v in (None, '<dict>', '<list>'):
                yield path, v
            elif v in ('<Config>', ):
                yield path, '<dict>'
            # must be at the end
            elif isinstance(v, BASIC_TYPES_EXT):
                yield path, v
            # elif isinstance(v, Item):
                # yield path, v
                #func = item.__getstate__().items
                # yield buid_key(root, ), '<{}>'.format(container.__class__.__name__)
            elif ignore:
                # print(f"Ignoring: {path}: {v}")
                continue
            else:
                raise RuntimeError(f"{RED}Don't know how to _filter{YELLOW} {path} = {v}{RESET}")

    result = rebuild(_filter(container))
    return result


def update_container_value(container, value, *keys):
    """Try to change a value in a container tree of nested list and dict
    returning if tree has been changed or not.
    """
    def change(container, key, value):
        modified = False
        if isinstance(container, (list, )):
            assert isinstance(key, int)
            if value:
                if key not in container:
                    container.append(key)
                    modified = True
            else:
                if key in container:
                    container.remove(key)
                    modified = True
        else:
            old = container.get(key)
            if value != old:
                container[key] = value
                modified = True
        return modified

    for key in keys[:-1]:
        if isinstance(container, (list, )):
            key = int(key)
            while len(container) < key:
                container.append(None)
        elif isinstance(container, (dict, )):
            container = container.setdefault(key, dict())
        else:
            raise RuntimeError(f"Don't know how to handle {container.__class__} in container")
    return change(container, keys[-1], value)


def flatdict(container):
    """Convert any structure in a flat dict that can be
    rebuilt later.

    flat = flatdict(container)
    copy = rebuild(flat.items())
    assert flat == copy
    """
    return dict([t for t in walk(container)])


def try_convert(container, klasses=[int]):
    if not isinstance(klasses, list):
        klasses = [klasses]

    for k, v in list(container.items()):
        for f in klasses:
            try:
                container[k] = f(v)
                break
            except Exception as why:
                continue
    return container


def diffdict(current, last):
    """Compare to versions of the same flatdict container, giving:

    - new items
    - changed items
    - deleted items

    """
    current_keys = set(current.keys())
    last_keys = set(last.keys())

    new_items = dict([(k, current[k]) for k in current_keys.difference(last_keys)])
    deleted_items = dict([(k, last[k]) for k in last_keys.difference(current_keys)])

    changed_items = dict()
    for k in current_keys.intersection(last_keys):
        c = current[k]
        l = last[k]
        if c != l:
            changed_items[k] = (c, l)

    return new_items, changed_items, deleted_items


def sort_iterable(iterable, key=0):
    "Specific function for sorting a iterable from a specific key position"
    result = list()
    iterable = list(iterable)
    while iterable:
        l = min([len(k[key]) if hasattr(k[key], '__len__') else 0 for k in iterable])
        subset = list()
        for i, k in reversed(list(enumerate(iterable))):
            if not hasattr(k[key], '__len__') or len(k[key]) == l:
                subset.append(k)
                iterable.pop(i)
        subset.sort(key=str, reverse=False)
        result.extend(subset)
    return result


def merge(base, new, mode='add'):

    def next_key_old(key):
        key = key.split('/')
        key[-1] = int(key[-1]) + 1
        return '/'.join(key)

    def next_key(key):
        key = list(key)
        key[-1] += 1  # must be an integer
        return tuple(key)

    def score(item):
        "function for sorting tables"
        return str(item)

    def _merge(base, new):
        base_ = list(walk(base))
        new_ = list(walk(new))

        base_.sort(key=score, reverse=False)
        new_.sort(key=score, reverse=False)

        last_container = []
        last_parent = None
        last_key = None
        last_idx = 0

        a = b = None

        while base_ or new_:
            if a is None and base_:
                a = base_.pop(0)
            if b is None and new_:
                b = new_.pop(0)

            if a and a[1] in ('<list>', ) or \
               b and b[1] in ('<list>', ):
                for b1 in last_container:
                    last_key = next_key(last_key)
                    yield (last_key, b1)

                last_container = list()
                last_parent = b and b[0]

            if a is None and b is not None:
                yield b
                b = None
                continue
            if b is None and a is not None:
                yield a
                a = None
                continue

            a0 = str(a[0])  # to make comparissons possible
            b0 = str(b[0])
            if b0 < a0:
                yield b
                b = None
            elif b == a:
                yield b
                a = b = None
            elif b0 == a0:
                # share the same key, but values differs
                if mode in ('replace', ):
                    yield b
                elif mode in ('add', ):
                    if isinstance(last_container, list):
                        last_key = a[0]
                        last_container.append(b[1])
                        yield a
                    else:
                        yield b
                a = b = None
            elif b0 > a0:
                yield a
                a = None
            else:
                raise RuntimeError('???')

        foo = 1

    # data = list()
    from pprint import pprint
    for pair in _merge(base, new):
        print("-" * 40)
        print(f"{pair[0]}: {pair[1]}")
        # data.append(pair)
        # result = rebuild(data)
        # pprint(result)
        foo = 1

    result = list(_merge(base, new))

    # key_converters = {'None': None, }

    result = sort_iterable(result)
    result = rebuild(result)

    return result


def uidfrom(lid):
    if not lid:
        return lid

    lid = str(lid)
    lid = bytes(lid, encoding='UTF-8')

    algo = 'md5'
    assert algo in hashlib.algorithms_guaranteed
    h = hashlib.new(algo)
    h.update(lid)
    uid = h.hexdigest()

    return uid


class wset(WeakSet):

    def __str__(self):
        return f"|{pformat(list(self))[1:-1]}|"

    def __repr__(self):
        return self.__str__()


def WKD(iterator):
    "Build a WeakKeyDictionary from object or object iterators"
    if isinstance(iterator, wset):
        return iterator

    if not hasattr(iterator, '__len__'):
        if iterator:
            iterator = [iterator]
        else:
            iterator = []
    return wset({k: True for k in iterator})


class xset(set):
    """Smart Set that explore other xset in parent for
    cascade deletion.
    """
    universe = WeakValueDictionary()

    def __init__(self, iterator=None, register=False):
        super().__init__(iterator)
        if register:
            # register xset container
            self.universe[id(self)] = self

    def difference_update(self, *args):
        """Remove items from ALL registered xset containers"""
        for container in self.universe.values():
            foo = container.intersection(*args)
            if foo:
                foo = foo
            set.difference_update(container, *args)

    def add(self, *args):
        """Replace an instance by other in ALL registered groups.
        When an object class object with the same attribute <key>
        is found, then is replaced by the new one (id() must be different)
        """
        key = 'uri'

        def _replace_in(container, item):
            id1 = id(item)
            key1 = getattr(item, key, None)

            for current in list(container):
                if id(current) == id1:
                    continue
                key2 = getattr(current, key, None)
                if not key2:
                    continue
                if key1 == key2:  # replace object
                    container.remove(current)
                    set.add(container, item)
                    return True
            set.add(container, item)
            return False

        for item in args:
            if _replace_in(self, item):
                for container in self.universe.values():
                    _replace_in(container, item)

        foo = 1

    @staticmethod
    def _explore(node, visited=None):
        """Iterate for xset containeres across parent nested structure"""
        visited = list() if visited is None else visited
        #extr = ('__iter__', '__dict__', 'items')
        extr = ('node.__dict__.values()')
        items = [item for item in node.__dict__.values()
                 if isinstance(item, xset) and item not in visited]

        print(f"= {node}{'='*40}")
        for item in items:
            if isinstance(item, xset):
                print(f" - {item}")
                visited.append(item)
                xset._explore(item, visited)

        return visited


def build_set(iterator=None):
    "Build a Set from object or object iterators"
    if isinstance(iterator, set):
        return iterator

    if not hasattr(iterator, '__len__') \
       or isinstance(iterator, str):
        if iterator:
            iterator = [iterator]
        else:
            iterator = []
    return set(iterator)


def build_xset(iterator=None, register=False, linear=False):
    "Build a xset from object or object iterators"
    if isinstance(iterator, set):
        return iterator

    if not hasattr(iterator, '__len__') \
       or isinstance(iterator, str):
        if iterator:
            iterator = [iterator]
        else:
            iterator = []
    if linear:
        iterator = linear_containers(iterator)
    return xset(iterator, register)

# https://stackoverflow.com/questions/6760685/creating-a-singleton-in-python
def soft_update(target, source):
    for k, v in source.items():
        target.setdefault(k, v)

class Singleton(type):
    _instances = {}
    _callargs = {}

    def __call__(cls, *args, **kwargs):
        if cls in cls._instances:
            if args or kwargs and cls._callargs[cls] != (args, kwargs):
                warn = """
WARNING: Singleton {} called with different args\n
  1st: {}
  now: {}
""".format(cls, cls._callargs[cls], (args, kwargs))
                print(warn)
        else:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
            cls._callargs[cls] = (args, kwargs)
        return cls._instances[cls]


# #Python2
# class MyClass(BaseClass):
    # __metaclass__ = Singleton

# #Python3
# class MyClass(BaseClass, metaclass=Singleton):
    # pass

class Xingleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        __call__ = super(Xingleton, cls).__call__
        __init__ = cls.__init__
        args2 = prepare_call_args(__init__, *args, **kwargs)
        # args2 = args

        existing = cls._instances.get(cls)  # don't use setdefault here
        if existing is None:
            existing = cls._instances[cls] = WeakValueDictionary()

        instance = existing.get(args2)
        if instance is None:
            instance = existing[args2] = __call__(*args2)
        return instance

# ----------------------------------------------------------------------
# instrospective and async calls
# ----------------------------------------------------------------------


class IntrospCaller(object):
    """base class for instrospective calls and async calls.

    Requires a context where locate:
    - 'converters' dict for mapping arguments call with calleables or data
    - 'call_keys' set to extract the key used to store deferred calls

    Example:

    # context for automatic IntrospCaller
    converters = self.context.setdefault('converters', {})
    converters['reqId'] = self._next_rid
    converters['contract'] = self._get_contract

    self.context.setdefault('call_keys', set()).update(['reqId', ])

    for symbol in ('NQ', 'ES', 'DAX'):
            self.make_call(self.protocol.client.reqContractDetails)

    It will make 3 calls that will use 'reqId' parameter as key

    In order to drop the cache when request is done user must explicit invoke

        self._drop_call(kw)

    where kw contains the same parameter that has been used to make the call

    """

    def __init__(self, context=None):
        self.context = context if context is not None else dict()
        self._make_request_cache = dict()
        self._calls = dict()

    def make_call(self, func, **ctx):
        frame = inspect.currentframe().f_back
        env = dict(frame.f_locals)
        context = {}
        while frame and not context:
            # converters = frame.f_locals.get('kw', {}).get('__context__', {}).get('converters', {})
            for name in ('context', 'ctx', ):
                context = frame.f_locals.get(name, {})
                if context:
                    break
            frame = frame.f_back
        converters = context.get('converters', {})

        # execute cached strategy
        strategy = self._get_strategy(func, env, converters)
        kw = execute_strategy(strategy, env, **converters)
        keys = self._set_call(func, kw)
        return func(**kw), keys

    def _get_strategy(self, func, env, converters):
        strategy = self._make_request_cache.get(func)
        if strategy is not None:
            return strategy

        strategy = strategy_call(func, env, **converters)
        self._make_request_cache[func] = strategy
        return strategy

    def _set_call(self, func, kw):
        # store call parameters for later use
        for key in self.context['call_keys'].intersection(kw):
            value = kw[key]
            self._calls[value] = func, value, kw

            # just 1 iteration, maybe more than one for advanced uses
            return func, value, kw

    def _drop_call(self, kw):
        result = []
        for key in self.context['call_keys'].intersection(kw):
            result.append(self._calls.pop(kw[key], None))
        return result


def strategy_call(func, env, **converters):
    """Try to find matching calling arguments making a
    deep search in `**kw` arguments."""
    func_info = inspect.getfullargspec(func)
    callargs = list(func_info.args)
    defaults = list(func_info.defaults or [])
    annotations = func_info.annotations or {}
    strategy = dict()
    while callargs:
        attr = callargs.pop(0)
        klass = annotations.get(attr)
        # find a object that match attr
        best_name, best_score = None, 0
        for name, value in env.items():
            if name in strategy:
                continue
            # d1 = likelyhood(attr, name)
            # d2 = likelyhood2(attr, name)
            # print("<{}, {}> : {} {}".format(attr, name, d1, d2))
            score = (likelyhood4(attr, name) +
                     (klass in (None, value.__class__))) / 2
            if 0.50 <= score > best_score:
                best_name, best_score = name, score
        if best_name:
            strategy[attr] = ('env', best_name)
            continue
        # otherwise we need to use converters
        # try to find the best converter possible
        # same or similar names, same return values is provided by signature
        best_name, best_score = None, 0
        for name, conv in converters.items():
            conv_info = inspect.getfullargspec(conv)
            ret = conv_info.annotations.get('return')
            if ret in (None, klass):
                score = likelyhood(attr, name)
                if score > best_score:
                    best_name, best_score = name, score
        if best_name:
            strategy[attr] = ('conv', best_name)

    if isinstance(func, types.MethodType):
        bound = func_info.args[0]
        assert bound == 'self'   # is a convenience criteria
        strategy.pop(bound, None)

    # self._make_request_cache[request] = strategy
    return strategy


def execute_strategy(strategy, env, **converters):
    kw2 = dict()
    for attr, (where, best) in strategy.items():
        if where in ('env'):
            value = env.get(best)
        elif where in ('conv'):
            conv = converters[best]
            args, kw = prepare_call(conv, **env)
            value = conv(*args, **kw)
        kw2[attr] = value
    return kw2


def update_context(context, *args, **kw):
    __avoid_nulls__ = kw.pop('__avoid_nulls__', True)

    if __avoid_nulls__:
        for k, v in kw.items():
            if v is not None:
                context[k] = v
    else:
        context.update(kw)

    for item in args:
        if isinstance(item, dict):
            d = item
        elif hasattr(item, 'as_dict'):
            d = item.as_dict()
        elif hasattr(item, '__dict__'):
            d = item.__dict__
        elif hasattr(item, '__getstate__'):
            d = item.__getstate__()
        else:
            d = dict()
            for k in dir(item):
                if k.startswith('_'):
                    continue
                v = getattr(item, k)
                if v.__class__.__name__ == 'type' or isinstance(v, TYPES):  # (types.FunctionType, types.MethodType, types.MethodWrapperType, types.BuiltinFunctionType)):
                    continue
                d[k] = v

        if __avoid_nulls__:
            for k, v in d.items():
                if v is not None:
                    context[k] = v
        else:
            context.update(d)


def prepare_call(func, *args, **kw):
    # collect available variables from stack
    __max_frames_back__ = kw.pop('__max_frames_back__', 1)
    frame = sys._getframe(1)
    frameN = sys._getframe(__max_frames_back__)
    _locals = list()
    while __max_frames_back__ > 0 and frame:
        _locals.append(frame.f_locals)
        __max_frames_back__ -= 1
        frame = frame.f_back
    _locals.reverse()
    kw0 = dict()
    for st in _locals:
        for item in st.values():
            update_context(kw0, item)
        update_context(kw0, st)
    kw0.update(kw)

    # try to match function calling args
    info = inspect.getfullargspec(func)
    kw2 = dict()
    args = list(args)
    callargs = list(info.args)
    defaults = list(info.defaults or [])
    # remove self for MethodType, and __init__
    if isinstance(func, types.MethodType) or \
       func.__name__ in ('__init__', ) or \
       func.__class__.__name__ in ('type', ):  # klass.__call__
        if callargs[0] == 'self':  # is a convenience criteria
            callargs.pop(0)
            kw0.pop('self', None)

    while len(defaults) < len(callargs):
        defaults.insert(0, None)

    while callargs:
        attr = callargs.pop(0)
        value = defaults.pop(0)
        if attr in kw0:
            value = kw0.pop(attr)
            if args:
                if id(value) == id(args[0]):
                    args.pop(0)
        elif args:
            value = args.pop(0)
        kw2[attr] = value

    if not info.varargs:
        if len(args) > 0:
            raise RuntimeError('too many positional args ({}) for calling {}(...)'.format(args, func.__name__))
    if info.varkw:
        kw2.update(kw0)
    # if isinstance(func, types.MethodType):
        # bound = info.args[0]
        # assert bound == 'self'   # is a convenience criteria
        # kw2.pop(bound)
    return args, kw2


def prepare_call_args(func, *args, **kw):
    args2, kw2 = prepare_call(func, *args, **kw)
    kw2.pop('self', None)
    info = inspect.getfullargspec(func)
    args2.extend([k for k in info.args if k in kw2])
    return tuple([kw2[k] for k in args2])


def _call(func, *args, **kw):
    if func is None:
        return

    # 1. try to execute directly
    if len(args) == 1:
        if isinstance(args[0], dict):
            args[0].update(kw)
            args, kw = [], args[0]
        elif isinstance(args[0], (list, tuple)):
            args = args[0]

    try:
        args2, kw2 = prepare_call(func, *args, **kw)
        return func(*args2, **kw2)
    except Exception as why:  # TODO: which is the right exception here? (missing args)
        #  TypeError
        traceback.print_exc()

        print(f"{YELLOW}ERROR: _call({func}) -> {BLUE}{why}{RED}")
        traceback.print_exc(file=sys.stdout)
        # exc_info = sys.exc_info()
        # tb = exc_info[-1]
        # tb.tb_next
        # frame = tb.tb_next.tb_frame

        # print(traceback.print_exception(*exc_info))
        print(f"{RESET}")
        # del exc_info
        foo = 1

    # 2. try to find calling arguments from passed dict as env
    # TODO: include default **converters as well?

    strategy = strategy_call(func, kw)
    kw2 = execute_strategy(strategy, kw)
    try:
        return func(**kw2)
    except Exception as why:  # TODO: which is the right exception here? (missing args)
        foo = 1


def async_call(func, *args, **kw):
    main = _call(func, *args, **kw)
    assert asyncio.iscoroutine(main)
    asyncio.run(main)

# ---------------------------------------------------------------------
# A Dynamic Programming based Python program for edit distance problem
# ---------------------------------------------------------------------


def editDistDP(name1, name2):
    m, n = len(name1), len(name2)
    # Create a table to store results of subproblems
    dp = [[0 for x in range(n + 1)] for x in range(m + 1)]

    # Fill d[][] in bottom up manner
    for i in range(m + 1):
        for j in range(n + 1):

            # If first string is empty, only option is to
            # insert all characters of second string
            if i == 0:
                dp[i][j] = j    # Min. operations = j

            # If second string is empty, only option is to
            # remove all characters of second string
            elif j == 0:
                dp[i][j] = i    # Min. operations = i

            # If last characters are same, ignore last char
            # and recur for remaining string
            elif name1[i - 1] == name2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]

            # If last character are different, consider all
            # possibilities and find minimum
            else:
                dp[i][j] = 1 + min(dp[i][j - 1],        # Insert
                                   dp[i - 1][j],        # Remove
                                   dp[i - 1][j - 1])    # Replace

    return dp[m][n]


def wlikelyhood(set1, set2, **weights):
    W = 0
    S = 0
    for k, w in weights.items():
        s1, s2 = set1.get(k, []), set2.get(k, [])
        if s1 or s2:
            # only weight average when any set is not empty
            W += w
            s = likelyhood4(s1, s2)
            S += w * s

    return S / (W or 1)


def likelyhood4(set1, set2):
    set1, set2 = list(set1), list(set2)
    N = (len(set1) + len(set2)) or 1
    S = 0

    def check(s1, s2):
        s = 0
        while s1:
            item = s1.pop(0)
            if item in s2:
                s2.remove(item)
                s += 2
            else:
                s -= 1
        return s
    S = check(set1, set2) + check(set2, set1)
    return S / N


def likelyhood3(set1, set2):
    n = min(len(set1), len(set2))
    if n:
        return 1 - editDistDP(set1, set2) / n
    return 0


def likelyhood2(name1, name2):
    n = min(len(name1), len(name2))
    return 1 - editDistDP(name1.lower(), name2.lower()) / n


def likelyhood(name1, name2):
    if len(name1) > len(name2):
        name1, name2 = list(name2.lower()), list(name1.lower())
    else:
        name1, name2 = list(name1.lower()), list(name2.lower())

    n = len(name1)
    score = 0
    while name1:
        a = name1.pop(0)
        if a in name2:
            idx = name2.index(a)
            name2.pop(idx)
        else:
            idx = n
        score += 1 / (1 + idx) ** 2

    return score / n


def get_calling_function(level=1):
    """finds the calling function in many decent cases."""
    # stack = inspect.stack(context)
    # fr = sys._getframe(level)   # inspect.stack()[1][0]
    stack = inspect.stack()
    while level < len(stack):
        fr = stack[level][0]
        co = fr.f_code
        for get in (
            lambda: fr.f_globals[co.co_name],
            lambda: getattr(fr.f_locals['self'], co.co_name),
            lambda: getattr(fr.f_locals['cls'], co.co_name),
            lambda: fr.f_back.f_locals[co.co_name],  # nested
            lambda: fr.f_back.f_locals['func'],  # decorators
            lambda: fr.f_back.f_locals['meth'],
            lambda: fr.f_back.f_locals['f'],
        ):
            try:
                func = get()
            except (KeyError, AttributeError):
                pass
            else:
                if func.__code__ == co:
                    return func
        level += 1
    raise AttributeError("func not found")


def retry(delay=0.1):
    """Retray the same call where the funcion is invokerd but
    a few instant later"""
    frame = inspect.currentframe().f_back
    calling_args = frame.f_code.co_varnames[:frame.f_code.co_argcount]
    calling_args = [frame.f_locals[k] for k in calling_args]
    func = get_calling_function(2)
    if isinstance(func, types.MethodType):
        calling_args.pop(0)

    loop = asyncio.get_event_loop()
    loop.call_later(0.2, func, *calling_args)

    foo = 1


async def add_to_loop(*aws, delay=0.1, loop=None):
    for coro in aws:
        asyncio.ensure_future(coro, loop=loop)
        await asyncio.sleep(delay, loop=loop)

# --------------------------------------------------
# RegExp operations
# --------------------------------------------------


def exp_compile(pattern):

    try:
        exp = re.compile(pattern, re.DOTALL)
         # if regexp has no groups, I assume is a wildcard
        if not exp.groups:
            raise re.error('force wildcard')
    except re.error:
        try:
            exp = fnmatch.translate(pattern)
            exp = re.compile(exp, re.DOTALL)
        except re.error:
            exp = re.compile('.*')

    return exp


def _prepare_test_regext(regexp=None, wildcard=None, test=None):
    test = test or list()

    if isinstance(regexp, (list, tuple, set)):
        test.extend(regexp)
    else:
        test.append(regexp)

    if not isinstance(wildcard, (list, tuple)):
        wildcard = [wildcard]
    for wc in wildcard:
        if wc and isinstance(wc, str):
            wc = fnmatch.translate(wc)
            test.append(wc)

    test = [re.compile(m).search for m in test if m]

    return test  # you can compile a compiled expression


def _find_match(string, test):
    for match in test:
        m = match(string)
        if m:
            return m


def _return_matched_info(m, info):
    if info == 'd':
        return m.groupdict()
    elif info == 'g':
        return m.groups()


def _return_unmatched(info):
    if info == 'd':
        return dict()
    elif info == 'g':
        return list()


def parse_string(string, regexp=None, wildcard=None, info=None):
    test = _prepare_test_regext(regexp, wildcard)
    m = _find_match(string, test)
    if m:
        return _return_matched_info(m, info)
    return _return_unmatched(info)  # to return cpmpatible values in upper stack


def parse_date(date):
    if isinstance(date, str):
        return parser.parse(date)
    return date


def parse_relativedelta(item):
    units = {
        's': 'seconds',
        'm': 'minutes',
        'h': 'hours',
        'd': 'days',
    }

    m = re.match(r"(?P<value>\d+)\w*(?P<unit>.+)$", item.lower(), re.DOTALL)
    d = m.groupdict()
    kw = {units[d['unit']]: float(d['value'])}
    return relativedelta(**kw)

# --------------------------------------------------
# Speed controlquery
# --------------------------------------------------


class SpeedControl(list):
    """Calculate the next pause needed to keep an average
    speed limit between requests to some service.
    """

    def __init__(self, lapse=0, N=1, *args, **kwargs):
        self.lapse = lapse
        if lapse:
            N = N or int(100 / (lapse or 1)) + 1
            N = min(max(N, 10), 100)
        else:
            N = 1
        self.N = N

    @property
    def pause(self):
        "The next pause before make the next request"
        N = len(self)
        t1 = time.time()
        self.append(t1)
        t0 = self.pop(0) if len(self) > self.N else self[0]
        t1p = self.lapse * N + t0
        return t1p - t1

    @property
    def speed(self):
        "Return the current average speed"
        elapsed = self[-1] - self[0]
        if elapsed > 0:
            return len(self) / elapsed
        return 0
        # return float('inf')

    @property
    def round_speed(self):
        # return math.ceil(self.speed * 100) / 100
        return int(self.speed * 100) / 100


# --------------------------------------------------
# Progress
# --------------------------------------------------
class ProgressControl(list):
    def __init__(self, d0, d1):
        self.d0 = d0
        self.range_ = d1 - d0
        # assert self.range_ > 0

    def progress(self, d):
        return int(10000 * (d - self.d0) / self.range_) / 100

# --------------------------------------------------
# File perations
# --------------------------------------------------


def lsof():
    regexp = re.compile(r'/proc/(?P<pid>\d+)/fd/(?P<fd>\d+)$')
    for root, folder, files in os.walk('/proc'):
        for name in files:
            path = os.path.join(root, name)
            m = regexp.match(path)
            if m:
                d = m.groupdict()
                try:
                    d['path'] = path
                    filename = os.readlink(path)
                    # if file == '/dev/null' or \
                      # re.match(r'pipe:\[\d+\]', file) or \
                      # re.match(r'socket:\[\d+\]', file):
                        #foo = 1
                except OSError as err:
                    if err.errno == 2:
                        file = None
                    else:
                        raise(err)

                yield (filename, d)

                foo = 1


def pid_of(path):
    for _path, result in lsof():
        if path == _path:
            yield result

        foo = 1


def iterate_fds(pid):
    dir = f'/proc/{pid}/fd'
    if not os.access(dir, os.R_OK | os.X_OK):
        return

    for fds in os.listdir(dir):
        for fd in fds:
            full_name = os.path.join(dir, fd)
            try:
                file = os.readlink(full_name)
                if file == '/dev/null' or \
                        re.match(r'pipe:\[\d+\]', file) or \
                        re.match(r'socket:\[\d+\]', file):
                    file = None
            except OSError as err:
                if err.errno == 2:
                    file = None
                else:
                    raise(err)

            yield (fd, file)


def direct_lines(file):
    "Just simple a wrapper to be able to call file.tell()"
    line = file.readline()
    while line:
        yield line
        line = file.readline()


def sorted_lines(file):
    "Just simple a wrapper to be able to call file.tell() and yields lines sorted"
    lines = dict()
    for line in direct_lines(file):
        key = line.split(',')[0]
        lines[key] = line, file.tell()

    # sort lines by 1st key
    keys = list(lines.keys())
    keys.sort()

    for k in keys:
        line, pos = lines.pop(k)
        # move file cursor for extenal progress
        file.seek(pos, os.SEEK_SET)
        yield line


def reversed_lines(file):
    "Generate the lines of file in reverse order."
    part = ''
    for block in reversed_blocks(file):
        for c in reversed(block):
            if c == '\n' and part:
                yield part[::-1]
                part = ''
            part += c
    if part:
        yield part[::-1]


def reversed_blocks(file, blocksize=4096):
    "Generate blocks of file's contents in reverse order."
    file.seek(0, os.SEEK_END)
    here = file.tell()
    while 0 < here:
        delta = min(blocksize, here)
        here -= delta
        file.seek(here, os.SEEK_SET)
        yield file.read(delta)


def fileiter(top, regexp=None, wildcard=None, info=None, relative=False):
    """Iterate over files
    info == 'd'   : returns filename, regexp.groupdict()
    info == 'g'   : returns filename, regexp.groups()
    info == None: : returns filename

    Allow single expressions or iterator as regexp or wildcard params
    """
    test = _prepare_test_regext(regexp, wildcard)
    for root, _, files in os.walk(top):
        for name in files:
            filename = os.path.join(root, name)
            if relative:
                filename = filename.split(top)[-1][1:]

            m = _find_match(filename, test)
            if m:
                m = _return_matched_info(m, info)
                if m:
                    yield filename, m
                else:
                    yield filename
    foo = 1


def copyfile(src, dest, override=False):
    if os.path.exists(dest) and not override:
        return

    folder = os.path.dirname(dest)
    if not os.path.exists(folder):
        os.makedirs(folder)
    with open(src, 'rb') as s:
        with open(dest, 'wb') as d:
            d.write(s.read())

    st = os.stat(src)
    os.chmod(dest, stat.S_IMODE(st.st_mode))


def expandpath(path):
    if path:
        path = os.path.expanduser(path)
        path = os.path.expandvars(path)
        path = os.path.abspath(path)
        while path[-1] == '/':
            path = path[:-1]
    return path



def parse_config_file(path):
    """*Parse a UNIX bash style config file.*
    Example:
    
    #REMOTE="vorange:/media/backup/ vmountain:/mnt/backup/"
    REMOTE="vorange:/media/backup/"
    FOLDERS="/home/agp/Documents/me/"
    SSHKEY=/home/agp/.ssh/id_rsa
    BWLIMIT=100
    PAUSE=3600
    CONSOLE=true
        
    """
    config = dict()
    path = expandpath(path)
    if os.path.exists(path):
        reg = re.compile(r'^(?P<key>\w+)\s*="?(?P<value>.*?)"?$')
        reg2 = re.compile(r'([^\s]+)\s*')
        for line in open(path, 'rt'):
            m = reg.match(line)
            if m:
                key, value = m.groups()
                value2 = [x.group() for x in reg2.finditer(value)]
                if len(value2) > 1:
                    value = value2
                config[key] = value

    return config

def load_config(path):
    raise DeprecationWarning()
    loader = {
        'yaml': yaml.load,
        'json': json.load,
    }
    config = dict()
    if os.path.exists(path):
        ext = os.path.splitext(path)[-1][1:]
        loader = loader.get(ext, loader['yaml'])
        with open(path, 'r') as f:
            config = loader(f) or config
    return config


def file_lookup(pattern, path=None):
    """Search for files in several folders using a strategy lookup.
    - pattern: relative or abspath
    - srcfile: file or directory where to look for last
    """

    root, name = os.path.split(pattern)
    if root:
        pattern = expandpath(pattern)

    path = path or '.'
    if os.path.isabs(pattern):
        candidates, pattern = os.path.split(pattern)
        candidates = [candidates]
    else:
        candidates = ['/etc', os.path.dirname(__file__),
                      '~/.config', '~', '.', path]

    # expand all parents for each candidate
    folders = []
    for path in candidates:
        head = tail = expandpath(path)
        ascend = list()
        while tail:
            ascend.append(head)
            head, tail = os.path.split(head)

        ascend.reverse()
        # add only new ones (is faster here that check twice later)
        for path in ascend:
            if path not in folders:
                folders.append(path)

    conf = dict()
    for root in folders:
        path = os.path.join(root, pattern)
        path = os.path.expanduser(path)
        path = os.path.expandvars(path)
        if not os.path.exists(path):
            # print(f"?  {path}? - no")
            continue
        # print(f"> {path}? - yes")
        yield path


def merge_config(pattern, srcfile=None):
    """Merge config files using the same lookup pattern"""
    conf = dict()
    for path in file_lookup(pattern, srcfile):
        # print(f"loading: {path}")
        c = yaml.load(open(path), Loader=yaml.FullLoader)
        if c is None:
            continue
        # merge with existing values
        # for name in c.get('loggers', {}):
            # print(f" - {name}")
        foo = 1
        for section, values in c.items():
            if isinstance(values, dict):
                org = conf.setdefault(section, dict())
                org.update(values)
            else:
                conf[section] = values
    return conf


def save_config(config, srcfile):
    srcfile = expandpath(srcfile)
    root, path = os.path.split(srcfile)
    os.makedirs(root, exist_ok=True)

    yaml.dump(config, open(srcfile, 'w'), default_flow_style=False)


def basic_type(item):
    if isinstance(item, (bool, int, float, str, bytes, )):
        return True
    return False


def get_serializable_state(config):
    state = dict()
    for k, v in flatdict(config).items():
        if basic_type(item):
            state[k] = v

    return state
# def save_config(config, path):
    #raise DeprecationWarning()

    # saver = {
        # 'yaml': partial(yaml.dump, default_flow_style=False),
        # 'json': json.dump,
    # }
    #ext = os.path.splitext(path)[-1][1:]
    #saver = saver.get(ext, saver['yaml'])
    # with open(path, 'w') as f:
        #config = saver(config, f)


def yaml_decode(raw: str):
    fd = StringIO(raw)
    return yaml.load(fd)


def yaml_encode(item: str):
    fd = StringIO()
    yaml.dump(item, fd, default_flow_style=False)
    return fd.getvalue()


def identity(item):
    "convenience function"
    return item


def test_pid(pid):
    try:
        pid = int(pid)
        os.kill(pid, 0)
    except OSError:
        return False
    else:
        return True


def dropfrom(cont, attr, value, recursive=True):
    for key in list(cont.keys()):
        print(f"key: {key}")
        if key == ('202005', 'diary', '20200521', 'atlas', 'core'):
            foo = 1
        item = cont[key]
        if attr in item:
            if item[attr] == value:
                cont.pop(key)
                return
            continue

        if hasattr(item, 'keys'):
            print(f">> in : {key}")
            dropfrom(item, attr, value, recursive)
            print(f"<< out: {key}")


def change_monitor(paths, timeout=None, delay=1):
    timestamp = dict()
    t0 = time.time()

    while True:
        for path in list(paths):
            t1 = os.stat(path).st_mtime
            t2 = timestamp.setdefault(path, t1)
            if t2 < t1:
                yield path
                timestamp[path] = t1
        else:
            time.sleep(delay)
            t1 = time.time()
            if timeout and t1 - t0 > timeout:
                break


# --------------------------------------------------
# Stats
# --------------------------------------------------
class Chronogram(dict):
    def __init__(self, params=None, *args, **kw):
        super().__init__(*args, **kw)
        self._last_key = None
        self.params = params or dict()
        self.labels = dict()
        self.key_name = 'x'
        self.name = 'A simle plot'
        self.formats = ('png', 'svg')

    def push(self, key, *args, **kw):
        for i, v in enumerate(args):
            kw[f'y{i}'] = v

        if kw != self.get(self._last_key, None):
            self[key] = kw
            self._last_key = key
            for i, k in enumerate(kw.keys()):
                self.params.setdefault(k, {'chart': 'plot'})
            return True
        return False

    def sorted_keys(self):
        keys = list(self.keys())
        keys.sort()
        return keys

    def extract(self, *names, **coverters):
        def ident(v): return v

        names = names or self.params
        for name in names:
            yield name, \
                [coverters.get(name, ident)(self[k][name])
                 for k in self.sorted_keys()], \
                self.params[name]

    def compute(self):
        """
        - [ ] compute df, and outdiders cases

        """
        import pandas as pd

        self.df = df = pd.DataFrame(self).transpose()

        std = df.std()
        mean = df.mean()

        # BBU
        bbu = mean + 1.0 * std
        bbl = mean - 1.0 * std

        # compute outdiders cases
        xbbu = (df - bbu) > 0
        self.outside_u = xbbu.sum() / xbbu.size

        xbbl = (df - bbl) < 0
        self.outside_l = xbbl.sum() / xbbu.size

        assert (self.outside_l < 0.10).all()  # less than 10% of value are outside
        assert (self.outside_u < 0.10).all()  # less than 10% of value are outside

        foo = 1

    def plot(self, **context):
        assert isinstance(self, Chronogram)
        import matplotlib.pyplot as plt
        plt.rcdefaults()
        import numpy as np
        import matplotlib.pyplot as plt

        x = self.sorted_keys()
        params = list(self.params)

        fig, axes = plt.subplots(nrows=len(params), constrained_layout=True, figsize=(20, 15))
        axes = dict([(params[i], ax) for (i, ax) in enumerate(axes)])

        for param, y, ctx in self.extract():
            ax = axes[param]
            chart = ctx.get('chart', context.get(param, {}).get('chart', 'plot'))
            #ax.plot(x, y)
            eval(f"ax.{chart}(x, y)")
            ax.grid()
            ax.set(xlabel=self.key_name, ylabel=self.params.get(param).get('name'),
                   title=self.labels.get(param, param))

        for fmt in self.formats:
            # plt.savefig(f"{self.name}.{time.time()}.{fmt}", dpi=600)
            plt.savefig(f"{self.name}.{fmt}", dpi=600)
        # plt.show()  # TODO: skip if is runing whitout desktop shell


class BoxedChronogram(Chronogram):
    """A basic Chronogram to be plotted.
    - if timeframe is set, numbers are averaged within box
    """

    def __init__(self, timeframe=None, *args, **kw):
        super().__init__(*args, **kw)
        self.timeframe = timeframe
        self._current_sampes = 0

    def push(self, key, *args, **kw):
        if self.timeframe:
            key = key // self.timeframe

        for i, v in enumerate(args):
            kw[f'y{i}'] = v

        if self._last_key != key:
            self._current_sampes = 1
            self[key] = kw
            self.params.update(kw.keys())
        else:
            # get average
            self._current_sampes += 1
            for k, v in kw.items():
                self[key][k] += (v - self[key][k]) / self._current_sampes


# --------------------------------------------------
# Debugger/Testing
# --------------------------------------------------
def void(): pass


class Record(dict):
    """Specific subclass dictorionary that:
    - remember keys order when someone has used before (in order)
    - iterate dict with this order
    """
    ORDER = list()
    USED = list()

    @classmethod
    def set_order(cls, order):
        assert isinstance(order, list)
        cls.ORDER = order

    def __init__(self, *args, **kw):
        self['time'] = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')
        super().__init__(*args, **kw)

    def __setitem__(self, key, value):
        if isinstance(value, type(None)):
            value = str(value)

        if key not in self.USED and key not in self.ORDER:
            self.USED.append(key)

        super().__setitem__(key, value)

    def reset(self):
        for k in set(self.ORDER).intersection(self.keys()):
            self.pop(k)
        for k in self.keys():
            self[k] = ''
        self['time'] = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')

    def items(self):
        keys = list(self.keys())
        for key in self.ORDER:
            if key in self:
                yield key, self[key]
                keys.remove(key)

        for key in self.USED:
            if key in self:
                yield key, self[key]


class Dumper():
    def __init__(self, out):
        self.out = out
        self.flush = getattr(self.out, 'flush', void)
        self.sep = '|'

        self._template_format = {
            r'time': r'{time:>{size}}',
            r'event': r'{event:>25}',
            # r'(name\d+)': r'{\1:{size}}',
            r'(name\d+)': r'{\1:25}',
        }
        self._format = dict()

    def write(self, record):
        record['time'] = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')
        indent = ''
        for line in self.format(record).split('\n'):
            self.out.write(f"{indent}{line}\n")
            indent = ' ... '
        self.flush()

    def format(self, record):
        fields = []
        if 'event' in record:
            record['event'] = "# {event}".format(**record)
        for k, v in record.items():
            fmt = self._get_fmt(k, v)
            fields.append(fmt)

        fields.append('')
        fmt = self.sep.join(fields)
        return fmt.format(**record)

    def _get_fmt(self, key, value):
        fmt = self._format.get(key)
        if not fmt:
            size = str(2 + len(str(value)))
            for pattern, exp in self._template_format.items():
                if re.search(pattern, key):
                    fmt = self._format[key] = re.sub(pattern, exp, key). \
                        replace('{size}', size)  # you can extend replacemente chain
                    break
            else:
                fmt = f"{value:^25}"
                # raise RuntimeError(f"unable fo find a format for {key} : {value}")
        return fmt


# - End -
