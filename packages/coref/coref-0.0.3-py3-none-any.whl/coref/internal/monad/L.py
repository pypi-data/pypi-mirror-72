from copy import deepcopy
from typing import Generic, Callable, Iterator, TypeVar, Iterable, Sized, Any

from coref.internal.util import partial
from coref.internal.monad.internal import isNothing
from oslash.abc import Applicative
from oslash.abc import Functor
from oslash.abc import Monoid
from oslash.abc import Monad

class L(Monad, Monoid, Applicative, Functor, Sized, Iterable):
    def __init__(self, derive: Callable[[Callable], Any]=None) -> None:
        self.name = ""
        if derive is None:
            self._value = []
        elif isinstance(derive, list) is True:
            self._value = deepcopy(derive)
        elif isinstance(derive, Monad) is True and ( hasattr(derive, 'value') is True and isinstance(derive.value, list) is True ):
            self._value = deepcopy(derive.value)
        elif callable(derive) is True:
            self._value = derive()
        else:
            self._value = []

    def _get_value(self):
        return self._value

    def raw(self):
        return self._value

    @property
    def value(self):
        return self.raw()

    @classmethod
    def empty(cls) -> 'L':
        return cls()

    def __len__(self):
        return len(self._value)

    def null(self) -> bool:
        return len(self) == 0

    def __iter__(self) -> Iterator:
        if self.null():
            return
        for v in self._value:
            yield (v)

    def __eq__(self, other: 'L') -> bool:
        return self.value == other.value

    def head(self) -> Any:
        if self.null() is True:
            return NONE
        return self._value[0]

    def tail(self) -> 'L':
        if self.null() is True:
            return NONE
        return L(self._value[1:])

    def cons(self, element: Any) -> 'L':
        if self.null() is True:
            return L([element])
        return L([element]+self._value)

    def end(self, element: Any) -> 'L':
        if self.null() is True:
            return L([element])
        return L(self._value+[element])

    def unit(self, value: Any) -> 'L':
        return self.empty().cons(value)

    pure = unit


    def apply(self, something: 'L') -> 'L':
        try:
            xs = [f(x) for f in self for x in something]
        except TypeError:
            xs = [partial(f, x) for f in self for x in something]
        return L.from_iterable(xs)

    def append(self, other: 'L') -> 'L':
        if self.null():
            return other
        return (self.tail().append(other)).cons(self.head())

    def bind(self, fn: Callable[[Any], 'L']) -> 'L':
        return L(self.map(fn))

    def map(self, mapper: Callable[[Any], Any]) -> 'L':
        try:
            ret = L.from_iterable([mapper(x) for x in self])
        except TypeError:
            ret = L.from_iterable([partial(mapper, x) for x in self])
        return ret

    @classmethod
    def from_iterable(cls, iterable: Iterable) -> 'L':
        _new = cls()
        for e in iterable:
            _new = _new.end(e)
        return _new

    def sort(self):
        return L(sorted(self))

    def reverse(self):
        return L(list(reversed(self.value)))

    def __str__(self) -> str:
        return "[%s]" % ", ".join([str(x) for x in self])

    def __repr__(self) -> str:
        return "L(%s) "%self.name+str(self)

    def __eq__(self, other) -> bool:
        if isNothing(other) is True:
            return False
        if self.null() or other.null():
            return True if self.null() and other.null() else False
        return self.head() == other.head() and self.tail() == other.tail()
