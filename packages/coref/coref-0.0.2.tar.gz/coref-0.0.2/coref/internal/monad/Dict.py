from copy import deepcopy
from typing import Generic, Callable, Iterator, TypeVar, Iterable, Sized, Any

from coref.internal.util import *
from .L import L
from oslash.abc import Applicative
from oslash.abc import Functor
from oslash.abc import Monoid
from oslash.abc import Monad

class Dict(Monad, Monoid, Applicative, Functor, Sized, Iterable):
    def __init__(self, derive: Callable[[Callable], Any]=None, **kw) -> None:
        if derive is None:
            self._value = {}
        elif isinstance(derive, dict) is True:
            self._value = deepcopy(derive)
        elif isinstance(derive, Monad) is True and ( hasattr(derive, 'value') is True and isinstance(derive.value, dict) is True ):
            self._value = deepcopy(derive.value)
        elif callable(derive) is True:
            self._value = derive()
        else:
            self._value = {}
        self._value.update(kw)

    def _get_value(self):
        return self._value

    @classmethod
    def empty(self) -> 'Dict':
        return self()

    def append(self, other: 'Dict') -> 'Dict':
        if self.null():
            return other
        _d = self.empty()
        _d._value.update(self.value)
        _d._value.update(other.value)
        return (_d)

    def update(self, other: Any=None, **kw) -> 'Dict':
        self._value.update(kw)
        if isinstance(other, dict) is True:
            self._value.update(other)
        elif isinstance(other, Dict) is True:
            self._value.update(other.value)
        elif isIterable(other) is True:
            for x in other:
                self.update(x)
        else:
            return self
        return self

    def __len__(self):
        return len(self.value.keys())

    def __iter__(self) -> Iterator:
        if self.null():
            return
        for k,v in self._value.items():
            yield (k,v)

    def bind(self, fn: Callable[[Any], 'Dict']) -> 'Dict':
        return Dict({k: fn(v) for k, v in self.value.items()})

    def apply(self, something: 'Dict') -> 'Dict':
        _res = {}
        for k, v in self:
            if callable(v) is not True:
                continue
            for k1, v1 in something:
                try:
                    _res[k1] = v(v1)
                except TypeError:
                    _res[k1] = partial(v, self)(v1)
        return Dict(_res)

    def map(self, mapper: Callable[[Any], Any]) -> 'Dict':
        value = deepcopy(self._get_value())
        try:
            result = mapper(value)
        except TypeError:
            result = partial(mapper, value)
        return Dict(result)

    def null(self) -> bool:
        return len(self._value.keys()) == 0

    def __eq__(self, other: 'Dict') -> bool:
        return self.value == other.value

    @classmethod
    def from_iterable(cls, iterable: Iterable) -> 'Dict':
        iterator = iter(iterable)
        _d = {}
        for k, v in iterator:
            _d[k] = v
        return Dict.empty().append(Dict(_d))

    def __setitem__(self, key, value):
        _key = key
        if isinstance(key, Monad) is True:
            _key = key.value
        return self._get_value().__setitem__(key, value)

    def __getitem__(self, key, default=None):
        _key = key
        if isinstance(key, Monad) is True:
            _key = key.value
        try:
            return self._get_value().__getitem__(key)
        except KeyError:
            return default
    def __delitem__(self, key):
        _key = key
        if isinstance(key, Monad) is True:
            _key = key.value
        return self._get_value().__delitem__(_key)

    def keys(self):
        return L(list(self._value.keys()))

    def __str__(self):
        return str(self._get_value())
    def __repr__(self):
        return repr(self._get_value())

Values = Dict
