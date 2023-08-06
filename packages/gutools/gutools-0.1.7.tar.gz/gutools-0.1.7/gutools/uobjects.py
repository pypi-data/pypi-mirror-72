import re
from gutools.tools import flatten, BASIC_TYPES, walk, rebuild
from gutools.colors import *
# --------------------------------------------------------------------
# UObjects
# --------------------------------------------------------------------


class UObject(object):

    converter_to_U = dict()
    converter_from_U = dict()

    @classmethod
    def register_converter(cls, uklass, klass, params):
        """params is a dict
        params[(attr, uatrt)] = (to_U_func, from_U_func)
        """
        # keep the same params objects instead creating new ones
        cls.converter_to_U[klass] = (uklass, params)
        cls.converter_from_U[uklass] = (klass, params)

    @classmethod
    def to_uobject(cls, item, **post):
        if item is None:
            return item
        uklass, info = cls.converter_to_U[item.__class__]
        uobject = uklass()
        for uattr, attr, to_U_func, from_U_func in info:
            if not isinstance(attr, str):
                attr = attr(item)
            value = getattr(item, attr, None)

            if not isinstance(uattr, str):
                uattr = uattr(uobject)
            setattr(uobject, uattr, to_U_func(value))

        for uattr, func in post.items():
            if hasattr(uobject, uattr):
                setattr(uobject, uattr, func(getattr(uobject, uattr)))

        return uobject

    @classmethod
    def from_uobject(cls, item, **post):
        if item is None:
            return item
        klass, info = cls.converter_from_U[item.__class__]
        obj = klass()

        for uattr, attr, to_U_func, from_U_func in info:
            if not isinstance(uattr, str):
                uattr = uattr(item)
            value = getattr(item, uattr)

            if not isinstance(atrr, str):
                atrr = atrr(obj)
            setattr(obj, atrr, func(value))

            if not isinstance(uattr, str):
                uattr = uattr(uobject)
            setattr(uobject, uattr, from_U_func(value))

        for atrr, func in post.items():
            setattr(obj, atrr, func(getattr(obj, atrr)))

        return obj

    @classmethod
    def change_to_uobject(cls, item, changes, **post):
        # TODO: move to register_converter pattern
        aliases = {
            'lmtPrice': 'price',
            'auxPrice': 'price',
            # 'trailStopPrice': 'price',
        }

        # same as to_uobject
        uobject = cls.to_uobject(item, **post)

        _, info = cls.converter_to_U[item.__class__]
        for attr, uattr in aliases.items():
            change = changes.pop(attr, None)
            if change is not None:
                for _, (uattr2, converter) in info.items():
                    if uattr == uattr2:
                        change = [converter(v) for v in change]
                        changes[uattr] = change
                        break

        return uobject, changes

    __args__ = tuple([])
    __kwargs__ = {}
    __slots__ = __args__ + tuple(__kwargs__.keys())
    __alias__ = {}

    def __init__(self, *args, **kwargs):
        # translate alias to slots members
        for k in set(self.__alias__).intersection(kwargs):
            kwargs.setdefault(self.__alias__[k], kwargs[k])

        if len(args) == 1 and hasattr(args[0], 'aslist'):  # isinstance(args[0], UObject):
            args = args[0].aslist()
            # remove all overriden kwargs
            idx = [k for k in kwargs if k in self.__args__]
            idx = [self.__args__.index(k) for k in idx]
            idx.sort(reverse=True)
            for i in idx:
                args.pop(i)

        kw2 = dict(self.__kwargs__)
        kw = list(self.__args__)

        # set the named args
        for k, v in kwargs.items():
            if k in kw:
                setattr(self, k, v)
                kw.remove(k)
                kw2.pop(k, None)
            elif k in kw2:
                setattr(self, k, v)
                kw2.pop(k, None)
            else:
                foo = 1

        # set the unnamed args
        kw.extend(kw2.keys())
        for i in range(min(len(kw), len(args))):
            k = kw.pop(0)
            setattr(self, k, args[i])
            kw2.pop(k, None)

        # set default values
        for k in kw:
            kw2.setdefault(k, None)
        for k, v in kw2.items():
            setattr(self, k, v)

        self.__pos_init__()

    def __pos_init__(self):
        """Try to replace an attribute when value is 'callable'"""
        for k in self.__slots__:
            try:
                setattr(self, k, getattr(self, k)())
            except TypeError:
                pass

    def astuple(self):
        return tuple(self.aslist())

    def aslist(self):
        return [getattr(self, k) for k in self.__slots__]

    def asdict(self, skip_nones=False, **kw):
        for k in self.__slots__:
            v = getattr(self, k)
            if skip_nones and v is None:
                continue
            kw.setdefault(k, v)
        for k in set(kw).difference(self.__slots__):
            kw.pop(k, None)

        # return dict([(k, getattr(self, k)) for k in self.__slots__])
        return kw

    def argsval(self, mask=r'arg\d'):
        regexp = re.compile(mask)
        keys = [k for k in self.__slots__ if regexp.match(k)]
        keys.sort()
        return [getattr(self, k) for k in keys]

    def __str__(self):
        # args = list(self.__args__)
        # args.extend(set(self.__kwargs__).difference(args))
        data = ['{}={}'.format(k, getattr(self, k)) for k in self.__slots__ if getattr(self, k) is not None]
        return '<{}: {}>'.format(self.__class__.__name__, ', '.join(data))

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        if isinstance(other, UObject):
            return self.astuple() == other.astuple()
        return False

    def __getitem__(self, key):
        key = self.__alias__.get(key, key)
        return getattr(self, key)

    def __setitem__(self, key, value):
        key = self.__alias__.get(key, key)
        return setattr(self, key, value)

    def update(self, **kw):
        for k in set(self.__slots__).intersection(kw):
            self.setattr(k, kw[k])


def I(a):
    return a


def E(item, name):
    return getattr(item, name)

# TODO: hash uid to permId and viceversa. Need map persistence


def iterasdict(iterator):
    r = list()
    for item in iterator:
        if item is None:
            r.append(item)
        else:
            r.append(item.asdict())
    return r


def kget(container, *keys):
    """Get a value from a container trying multiples keys in order."""
    for key in keys:
        if key in container:
            return container[key]


def vget(container, value, *keys):
    """TBD"""
    for name, item in container.items():
        for key in keys:
            if getattr(item, key, None) == value:
                return name, item
    return None, None


# --------------------------------------------------------------------
# UUnit
# --------------------------------------------------------------------
class UUnit(UObject):
    __args__ = ('value', )
    __kwargs__ = {'unit': '', }
    __slots__ = __args__ + tuple(set(__kwargs__).difference(__args__))

    conversion = {}

    def __long__(self):
        return self.value

    def __float__(self):
        return self.value

    def __str__(self):
        return f"{self.value} {self.unit}"

    def __repr__(self):
        return str(self)

    def __bool__(self):
        return bool(self.value)

    def __eq__(self, other):
        if isinstance(other, UUnit):
            return self.aslist() == other.aslist()
        return self.value == other

    def __add__(self, other):
        """
        Defines the '+' operator.
        """
        assert isinstance(other, UUnit)
        if other.unit != self.unit:
            fact = UUnit.conversion.get
            f = fact((other.unit, self.unit)) or 1.0 / fact((self.unit, other.unit))
            if not f:
                raise RuntimeError(f"Unable to convert '{other.unit}' to '{self.unit}'")

        else:
            f = 1.0

        return UUnit(self.value + f * other.value, self.unit)

    def __iadd__(self, other):
        """
        Similar to __add__
        """
        if type(other) == int or type(other) == float:
            x = (other * Ccy.currencies[self.unit])
        else:
            x = (other.value / Ccy.currencies[other.unit] * Ccy.currencies[self.unit])
        self.value += x
        return self

    def __radd__(self, other):
        res = self + other
        if self.unit != "EUR":
            res.changeTo("EUR")
        return res


# --------------------------------------------------------------------
# Smart Answer and Query.
# --------------------------------------------------------------------
class Query(dict):
    """A query to be attended"""

    def soft(self, *args, **defaults):
        """Soft update dict values when keys doesn't exist"""
        if args:
            q = args[0]
        else:
            q = dict()
        q.update(defaults)
        for k, v in q.items():
            if self.get(k) is None:
                self[k] = v
            # self.setdefault(k, v)


class SmartContainer(dict):
    _key_attribute = dict()
    _includes = dict()
    _excludes = dict()

    def _get_key_attribute(self, item):
        keys = self._key_attribute.get(item.__class__)
        if keys:
            for attr in keys.split('.'):
                item = getattr(item, attr, None)
                if item is None:
                    return
            return item
        else:
            return len(self)

    @classmethod
    def register_key(cls, klass, attr):
        cls._key_attribute[klass] = attr

    @classmethod
    def includes(cls, klass, attr, filter_):
        ex = cls._excludes.setdefault(klass, dict()).setdefault(attr, list())
        ex.append(filter_)

    @classmethod
    def excludes(cls, klass, attr, filter_):
        ex = cls._excludes.setdefault(klass, dict()).setdefault(attr, list())
        ex.append(filter_)

    def add(self, item):
        if isinstance(item, tuple):
            if len(item) == 1:
                item = item[0]

        if self._check_filters(item):
            return  # discard insertion

        key = self._get_key_attribute(item)
        self[key] = item
        return item

    def aslist(self):
        keys = list(self.keys())
        keys.sort()
        return [self[k] for k in keys]

    def sortitems(self):
        keys = list(self.keys())
        keys.sort()
        for k in keys:
            yield k, self[k]

    def _check_filters(self, item) -> bool:
        for item in flatten(item):
            ex_info = self._excludes.get(item.__class__, {})
            for attr, filters in ex_info.items():
                value = getattr(item, attr)
                for filter_ in filters:
                    if filter_(value):
                        return True
        return False

    def walk(self):
        yield from walk(self, includes=self._includes, excludes=self._excludes)


class Answer(SmartContainer):
    pass

# --------------------------------------------------------------------
# Converters
# --------------------------------------------------------------------


class UConverter(object):
    """Base class for Converters.
    """

    def __init__(self):
        pass

    def convert(self, container):
        raise RuntimeError('Must be overriden')

    def convert_item(self, item):
        raise RuntimeError('Must be overriden')


def test_walk():

    containers = [
        {},
        [],
        tuple([]),
        {
            'foo': 3,
            'bar': [1, 2, 3],
            'buzz': {
                'a': 'A',
                'b': 'B',
                'c': (9, 8, 7),
            },
        },
    ]

    for container in containers:
        # footprint = [d for d in walk(container)]
        container2 = rebuild(walk(container))

        assert container == container2
        assert id(container) != id(container2) or isinstance(container, tuple)

    foo = 1


def test_alias():
    class UFoo(UObject):
        __args__ = ('a', 'b', 'c', )
        __kwargs__ = {'a': 'uno', }
        __slots__ = __args__ + tuple(set(__kwargs__).difference(__args__))
        __alias__ = {'foo': 'a', }

    foo = UFoo()
    x = foo.foo
    foo.foo = 1
    assert foo.a == foo.foo


def test_unflattern():
    info = [
        [1, 2, 3, 'uno'],
        [4, 5, 6, 'dos'],
        [7, 8, 9, 'tres'],
        [10, 11, 12, 'cuatro'],
    ]

    info2 = unflattern(info, [-1, ])
    info3 = unflattern(info, [-1, 0])

    foo = 1


def test_uunit():

    a = UUnit(1, "EUR")
    b = UUnit(2, "EUR")
    u = UUnit(5, "USD")

    if a:
        foo = 1
    else:
        foo = 2

    assert foo == 1

    z = a + b

    assert z == 3

    UUnit.conversion[('EUR', 'USD')] = 1.13
    x = u + b
    y = b + u

    foo = 1


if __name__ == '__main__':

    test_uunit()
    test_unflattern()
    test_alias()
    test_walk()
