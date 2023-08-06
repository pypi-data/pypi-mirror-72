
from itertools import cycle
from gutools.uobjects import Query
# --------------------------------------------------
# logger
# --------------------------------------------------
from gutools.loggers import logger, \
    trace, exception, debug, info, warn, error
log = logger(__name__)


class FQItem(Query):
    """*A full qualified item*."""

    def __str__(self):
        result = []
        k = self.get('key')
        if k:
            result.append(f"{k}")

        r = self.get('rot')
        if r:
            result.append(f"{r}{self[r]}")

        result.append("[{d}.{w}.{m}.{y}]".format(**self))
        return '.'.join(result)

    def __repr__(self):
        result = []
        k = self.get('key')
        if k:
            result.append(f"{k}")

        r = self.get('rot')
        if r:
            result.append(f"{r}{self[r]}")

        e = self.get('ext')
        if e:
            result.append(e)

        return '.'.join(result)


class Rotator():
    """*Rotator.*
    Example: 
        
        rot = [
        ('d', 0, 6),
        ('w', 0, 52),
        ('m', 1, 12),
        ('y', 10, None),
        ]
        
    - The cascade order is 'd' -> 'w' -> 'm' -> 'y'
    - The ranges are [0, 6] included for d, etc
    - The range for 'y' is upper unbounded.
    
    """

    def __init__(self, ranges):
        self.ranges = ranges

    def next_item(self, fqitem):
        """*Return the next incremental element of given one.*
        
        TODO: used?
        
        """
        fqitem = FQItem(fqitem)  # makes a copy
        rot = self.ranges[0][0]  # forces to be expressed in the LSB
        fqitem['rot'] = rot
        r0, m0, M0 = None, None, None
        for r1, m1, M1 in self.ranges:
            if r0:
                if fqitem[r0] > M0:  # increase next 'unit'
                    fqitem[r0] = m0
                    fqitem[r1] += 1
                else:
                    break
            else:
                fqitem[r1] += 1  # increase less-most-significat 'digit'
            r0, m0, M0 = r1, m1, M1
        return fqitem

    def fqitem(self, item=None, **level):
        """*Merge an item with extra information.*
        - Create a copy, doesn't modify the passed argument.
        """
        item = FQItem() if item is None else FQItem(item)
        item.update(level)
        return item

    def rotations(self, fqitem, **level):
        """*Check all rotation needed.*
        
        Return a list of rorated fqitems place holders where to store
        the information.
        """
        result = []
        fqitem2 = FQItem(fqitem)

        # increase 'digits'
        for r0, m0, M0 in self.ranges:
            fqitem2[r0] += 1
            if M0 and fqitem2[r0] > M0:  # increase next 'unit'
                fqitem2[r0] = m0
            else:
                break

        # count changes
        for r0, _, _ in self.ranges:
            if fqitem[r0] != fqitem2[r0]:
                fqitem2 = FQItem(fqitem2)
                fqitem2['rot'] = r0
                result.append(fqitem2)
            else:
                break

        return result

    def _parse(self, element):
        """*Extract info form element to be classified.
        
        return a dict with almost:
        - 'key': main key for grouping elements.
        - 'rot': the key of the cascade level.
        - 'value': the value of the element in this cascade.
        
        The rest of parsed elements will be used to rebuild the element
        whenever will be necessary.
        """
        raise NotImplementedError()

    def _rebuild(self, item):
        """*Reconstruct an element from parsed data.*"""
        raise NotImplementedError()

    def apply(self, items):
        """*Apply operation to (rotated) elements.*
        """
        raise NotImplementedError()


# class SubRotator(Rotator):

    # def __init__(self, ranges):
        # super().__init__(ranges)
        #self.elements = dict()

    # def load(self, samples):
        # """*Load a bunch of samples.*
        # - parse samples and create a internal structure.
        # """
        #samples = samples or []
        # for element in samples:
            # self.add(element)

    # def add(self, element):
        # self._add(self._parse(element))

    # def _add(self, item):
        # if item:
            #rot = item['rot']
            #self.elements.setdefault(item['key'], dict()) \
                # .setdefault(rot, dict())[item[item[rot]]] = item

    # def _get_element(self, item):
        #rot = item['rot']

        #aux = self.elements.get(item['key'], {}) \
            # .get(rot, {}) \
            # .get(item[item[rot]])
        # if aux:
            # return self.fqitem(aux, item)

    # def select_newest(self, key):
        #elements = self.elements[key]
        # for rot, m, M in self.ranges:
            #elements = elements[rot]
            #keys = list(elements.keys())
            # keys.sort()
            #item = elements[keys[-1]]
            # return item
