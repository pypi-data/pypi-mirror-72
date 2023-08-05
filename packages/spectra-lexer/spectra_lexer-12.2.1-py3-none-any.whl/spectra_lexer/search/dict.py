""" Module for key-search dictionaries from generic to specialized. """

from bisect import bisect_left
from itertools import islice
from operator import methodcaller
import re
from typing import Callable, Dict, Iterable, List, Tuple, TypeVar

SKT = TypeVar("SKT")  # Similarity-transformed key (simkey) type.
KT = TypeVar("KT")    # Raw key type.
VT = TypeVar("VT")    # Value type.


class SimilarKeyDict(Dict[KT, VT]):
    """
    A special hybrid dictionary implementation using a sorted key list along with the usual hash map. This allows
    lookups for keys that are "similar" to a given key in O(log n) time as well as exact O(1) hash lookups, at the
    cost of extra memory to store transformed keys and increased time for individual item insertion and deletion.
    It is most useful for large dictionaries that are mutated rarely after initialization, and which have a need
    to compare and sort their keys by some measure other than their natural sorting order (if they have one).

    The "similarity function" returns a measure of how close two keys are to one another. This function should take a
    single key as input, and the return values should compare equal for keys that are deemed to be "similar". Even if
    they are not equal, keys with return values that are close will be close together in the list and may appear
    together in a search where equality is not required (subclasses must implement these searches). All implemented
    functionality other than similar key search is equivalent to that of a regular dictionary.

    Due to the dual nature of the data structure, there are additional restrictions on the data types allowed to be
    keys. As with a regular dict, keys must be of a type that is hashable, but they also must be totally orderable
    (i.e. it is possible to rank all the keys from least to greatest using comparisons) in order for sorting to work.
    A frozenset, for instance, would not work despite being hashable because it has no well-defined sorting order.
    The output type of the similarity function (if it is different) must be totally orderable as well.

    Inside the list, keys are stored in sorted order as tuples of (simkey, rawkey), which means they are ordered first
    by the value computed by the similarity function, and if those are equal, then by their natural value.

    The average-case time complexity for common operations are as follows:

    +-------------------+-------------------+------+
    |     Operation     | SimilarSearchDict | dict |
    +-------------------+-------------------+------+
    | Initialize        | O(n log n)        | O(n) |
    | Lookup (exact)    | O(1)              | O(1) |
    | Lookup (inexact)  | O(log n)          | O(n) |
    | Insert Item       | O(n)              | O(1) |
    | Delete Item       | O(n)              | O(1) |
    | Iteration         | O(n)              | O(n) |
    +-------------------+-------------------+------+
    """

    def __init__(self, *args, simfn:Callable[[KT], SKT]=None, mapfn:Callable[[Iterable[KT]], map]=None, **kwargs):
        """ Initialize the dict and list to empty and set up the similarity and map functions.
            If other arguments were given, treat them as containing initial items to add as with dict.update(). """
        super().__init__()
        if simfn is None:
            simfn = self._default_simfn
        if mapfn is None:
            mapfn = self._default_mapfn
        self._list = []      # Sorted list of tuples: the similarity function output paired with the original key.
        self._simfn = simfn  # Similarity function, mapping raw keys that share some property to the same "simkey".
        self._mapfn = mapfn  # Optional implementation of the similarity function mapped across many keys.
        if args or kwargs:
            self._update_empty(*args, **kwargs)

    @staticmethod
    def _default_simfn(k:KT) -> SKT:
        """ The default similarity function returns keys unchanged. """
        return k

    def _default_mapfn(self, keys:Iterable[KT]) -> map:
        """ The default similarity map function is a straight call to map(). This is usually good enough. """
        return map(self._simfn, keys)

    def __reduce__(self) -> tuple:
        """ Dict subclasses call __setitem__ to unpickle, which will happen before the key list exists in our case.
            We must sidestep this and unpickle everything using __setstate__.  """
        return self.__class__, (), (dict(self), self._simfn, self._mapfn)

    def __setstate__(self, state:tuple) -> None:
        """ Unpickle everything with a call to __init__. This makes the key list redundant. """
        d, simfn, mapfn = state
        self.__init__(d, simfn=simfn, mapfn=mapfn)

    def clear(self) -> None:
        super().clear()
        self._list.clear()

    def __setitem__(self, k:KT, v:VT) -> None:
        """ Set an item in the dict. If the key didn't exist before, find where it goes in the list and insert it. """
        if k not in self:
            idx = self._index_exact(k)
            self._list.insert(idx, (self._simfn(k), k))
        super().__setitem__(k, v)

    def __delitem__(self, k:KT) -> None:
        """ Just call pop() and throw away the return value. This will not affect sort order. """
        self.pop(k)

    def pop(self, k:KT, *default:VT) -> VT:
        """ Remove an item from the dict and list and return its value, or <default> if not found. """
        if k in self:
            idx = self._index_exact(k)
            del self._list[idx]
        if not default:
            return super().pop(k)
        return super().pop(k, *default)

    def popitem(self) -> Tuple[KT,VT]:
        """ Remove the last (key, value) pair as found in the list and return it. The dict must not be empty. """
        if not self:
            raise KeyError()
        sk, k = self._list[-1]
        return k, self.pop(k)

    def setdefault(self, k:KT, default:VT=None) -> VT:
        """ Get an item from the dictionary. If it isn't there, set it to <default> and return it. """
        if k in self:
            return self[k]
        self[k] = default
        return default

    def update(self, *args, **kwargs) -> None:
        """ Update the dict and list using items from the given arguments. Because this is typically used
            to fill dictionaries with large amounts of items, a fast path is included if this one is empty. """
        if not self:
            self._update_empty(*args, **kwargs)
        else:
            for (k, v) in dict(*args, **kwargs).items():
                self[k] = v

    def _update_empty(self, *args, **kwargs) -> None:
        """ Fill the dict from empty and remake the list using items from the given arguments. """
        assert not self
        super().update(*args, **kwargs)
        self._list = sorted(zip(self._mapfn(self), self))

    def copy(self) -> "SimilarKeyDict":
        """ Make a shallow copy of the dict. The list will simply be reconstructed in the new copy. """
        cls = type(self)
        return cls(self, simfn=self._simfn, mapfn=self._mapfn)

    @classmethod
    def fromkeys(cls, seq:Iterable[KT], value:VT=None, **kwargs) -> "SimilarKeyDict":
        """ Make a new dict from a collection of keys, setting the value of each to <value>.
            simfn can still be set by including it as a keyword argument after <value>. """
        return cls(dict.fromkeys(seq, value), **kwargs)

    def _index_left(self, simkey:SKT) -> int:
        """ Find the leftmost list index of <simkey> (or the place it *would* be) using bisection search. """
        # Out of all tuples with an equal first value, the 1-tuple with this value compares less than any 2-tuple.
        return bisect_left(self._list, (simkey,))

    def _index_exact(self, k:KT) -> int:
        """ Find the exact list index of the key <k> using bisection search (if it exists). """
        return bisect_left(self._list, (self._simfn(k), k))

    def get_similar_keys(self, k:KT, count:int=None) -> List[KT]:
        """ Return a list of at most <count> keys that compare equal to <k> under the similarity function. """
        _list = self._list
        simkey = self._simfn(k)
        idx_start = self._index_left(simkey)
        idx_end = len(_list)
        if count is not None:
            idx_end = min(idx_end, idx_start + count)
        keys = []
        for idx in range(idx_start, idx_end):
            (sk, rk) = _list[idx]
            if sk != simkey:
                break
            keys.append(rk)
        return keys

    def get_nearby_keys(self, k:KT, count:int) -> List[KT]:
        """ Return a list of at most <count> keys that are near to <k> under the similarity function.
            All keys will be approximately centered around <k> unless we're too close to one edge of the list. """
        _list = self._list
        idx_left = self._index_exact(k) - count // 2
        if idx_left <= 0:
            items = _list[:count]
        else:
            idx_right = idx_left + count
            if idx_right >= len(_list):
                items = _list[-count:]
            else:
                items = _list[idx_left:idx_right]
        return [i[1] for i in items]


class StringSearchDict(SimilarKeyDict):
    """
    A similar-key dictionary with special search methods for strings.
    In order for the standard optimizations involving literal prefixes to work, the similarity function must
    not change the relative order of characters (i.e. changing case is fine, reversing the string is not.)
    """

    # Regex to match ASCII characters without special regex behavior when used at the start of a pattern.
    # Will always return at least the empty string (which is a prefix of everything).
    _LITERAL_PREFIX_RX = re.compile(r'[\w \"#%\',\-:;<=>@`~]*').match

    def prefix_match_keys(self, prefix:str, count:int=None, raw=True) -> List[str]:
        """ Return a list of keys (of either type) where the simkey starts with <prefix>, up to <count>. """
        sk_start = self._simfn(prefix)
        if not sk_start:
            # If the prefix is empty after transformation, it could possibly match anything.
            matches = self._list if count is None else self._list[:count]
        else:
            # All matches will be found in the sort order between the prefix itself (inclusive) and
            # the prefix with one added to the numerical value of its final character (exclusive).
            idx_start = self._index_left(sk_start)
            sk_end = sk_start[:-1] + chr(ord(sk_start[-1]) + 1)
            idx_end = self._index_left(sk_end)
            if count is not None:
                idx_end = min(idx_end, idx_start + count)
            matches = self._list[idx_start:idx_end]
        # For the (simkey, rawkey) tuples, we can use the boolean as an index for the key type we want.
        return [i[raw] for i in matches]

    def regex_match_keys(self, pattern:str, count:int=None, raw=True) -> List[str]:
        """ Return a list of at most <count> keys that match the regex <pattern> from the start.
            Can search and return either the raw keys (default) or sim keys. """
        # First, figure out how much of the pattern string from the start is literal (no regex special characters).
        literal_prefix = self._LITERAL_PREFIX_RX(pattern).group()
        # If all matches must start with a certain literal prefix, we can narrow the range of our search.
        # Only keep the type of key (raw or simkey) that we're interested in searching.
        keys = self.prefix_match_keys(literal_prefix, count=None, raw=raw)
        if not keys:
            return []
        # If the prefix and pattern are equal, we have a complete literal string. Regex is not necessary.
        # Just do a (case-sensitive) prefix match in that case. Otherwise, compile the regular expression.
        if literal_prefix == pattern:
            match_op = methodcaller("startswith", pattern)
        else:
            match_op = re.compile(pattern).match
        # Run the match filter until <count> entries have been produced (if None, search the entire key list).
        return list(islice(filter(match_op, keys), count))
