import time
import uuid
import re
import sys
from fnmatch import fnmatch
from coref.internal.dp import DP
from coref.internal.path import *
from coref.internal.util import *
from coref.internal.v import Vstor
from typing import Generic, Callable, Iterator, TypeVar, Iterable, Sized, Any
from coref.internal.monad.internal import NONE, isNothing
from .Dict import Dict
from .L import L
from oslash import Monad, Just, Nothing
from oslash import Left, Right

class Namespace(Dict):
    def __init__(self, derive: Callable[[Callable], Any]=None, **kw) -> None:
        self.isNamespace = True
        if derive is None:
            self._value = DP()
        elif isinstance(derive, dict) is True:
            self._value = DP(derive)
        elif isinstance(derive, Monad) is True and ( hasattr(derive, 'value') is True and isinstance(derive.value, dict) is True ):
            self._value = DP(derive.value)
        elif callable(derive) is True:
            self._value = derive()
        else:
            self._value = DP()
        for k in kw:
            v = kw[k]
            if isinstance(v, Monad) is True:
                self._value.raw()[k] = v.value
            else:
                self._value.raw()[k] = v
        if '__dir__' not in self._value.keys():
            _new = {
                '__dir__': True,
                '__stamp__': time.time(),
                '__name__': '/',
                '__id__': str(uuid.uuid4())
            }
            self._value.raw().update(_new)
        self.stor = Vstor()
        self.V("/sys/vstor", self.stor)

    def update(self, *cfg, **kw):
        for k in kw:
            if k[0] != "/":
                _k = f"/home/{k}"
            else:
                _k = k
            self._value.set(_k, kw[k])
        for c in cfg:
            if callable(c) is True:
                c(self)
                continue
            self._value.update(c)
        return self


    def _derive(self, _d, *attrs):
        for a in attrs:
            if hasattr(self, a) is True:
                setattr(_d, a, getattr(self, a))

    def _clone(self, _orig, _dst, *attrs):
        for a in attrs:
            if hasattr(_orig, a) is True and hasattr(_dst, a) is False:
                setattr(_dst, a, getattr(_orig, a))

    def append(self, other: 'Dict') -> 'Dict':
        if self.null():
            return other
        _d = self.empty()
        self._derive(_d, "parent", "stor")
        _d.raw().raw().update(self.value.raw())
        if isinstance(other.value, DP) is True:
            _d.raw().raw().update(other.value.raw())
        else:
            _d.raw().raw().update(other.value)
        self._clone(other, _d, "parent", "stor")
        return (_d)

    def raw(self):
        return self._value

    def Name(self):
        return Just(self._value.raw()['__name__'])

    def isDir(self):
        return Just(self._value.raw()['__dir__'])

    def Mkdir(self, *path) -> tuple:
        _p = []
        _res = []
        for p in path:
            _p += expandPath(p)
        for i in unique(_p):
            _res.append(self.mkdir(i))
        return tuple(_res)

    def mkdir(self, path: str) -> 'Namespace':
        _nns = Namespace(self._value.mkdir(path))
        if hasattr(self, "parent") is True:
            _nns.parent = self.parent
        else:
            _nns.parent = self
        self._clone(self, _nns, "stor")
        return _nns

    def Cd(self, *path) -> tuple:
        _res = []
        for i in unique(path):
            _res.append(self.cd(i))
        return tuple(_res)
    def cd(self, path: str) -> 'Namespace':
        if self.stor.here(f"{path}/afile") is True:
            return NONE
        ns = self._value
        try:
            print('YYYY', type(self._value.get(path).value))
            res =  Namespace(self._value.get(path).value)
        except KeyError:
            res =  self.mkdir(path)
        if hasattr(self, "parent") is True:
            res.parent = self.parent
        else:
            res.parent = self
        self._clone(self, res, "stor")
        return res

    def C(self):
        if hasattr(self, "parent"):
            self.parent.raw().set(self.Name().value, self._value)

    def V(self, path: str, value: Monad=NONE) -> Any:
        import os.path

        if path[0] != "/":
            path = f"/home/{path}"

        if value is NONE or value is None or value is Nothing():
            if self.stor.here(path) is True:
                res = self.stor.get(path)
                if res is None:
                    return NONE
                else:
                    return Just(res)
            return self._value.get(path)
        else:
            if isinstance(value, Monad) is True:
                data = value.value
            else:
                data = value
            if self.stor.here(path) is True:
                self.stor.set(path, data)
            else:
                self._value.set(path, value)
            return value
        return NONE

    def f(self, name: str, *args, **kw) -> Any:
        def _fun(*args, **kw):
            return NONE
        path = self._value.get("/etc/path", ["/bin", "/home"])
        if name[0] == "/":
            fun = self._value.get(name, _fun)
            if args or kw:
                return partial(fun.value, *args, **kw)
            return fun.value
        else:
            for p in path.value:
                fname = f"{p}/{name}"
                fun = self._value.get(fname, None)
                if fun is not None:
                    if args or kw:
                        return partial(fun.value, *args, **kw)
                    return fun.value
        return _fun

    def F(self, path, *args, **kw):
        _fun = self.f(path)
        try:
            _start = time.perf_counter()
            res = _fun(*args, **kw)
            _end = time.perf_counter()
            ftrace = self.V('/sys/traceback/ftrace')
            if isNothing(ftrace) is not None:
                ft = self.V('/config/ftrace').value
                _rec = ft(stamp=time.time(), fun=path, time=_end-_start, args=args, kw=kw)
                ftrace.value.append(_rec)
            return Right(res)
        except:
            _t, _val, _tb = sys.exc_info()
            exc = self.V('/config/exception').value
            if isNothing(exc) is not True:
                res = exc(type=_t, value=_val, traceback=_tb)
            else:
                res = {}
                res['type'] = _t
                res['value'] = _val
                res['traceback'] = _tb
            tb = self.V('/sys/traceback/tb')
            if isNothing(tb) is not True:
                tb.value.append(res)
                self.V('/sys/traceback/exists', True)
            print(res)
            return Left(res)

    def ls(self, path: str, patt: str="*", **kw) -> 'L':
        _out = []
        v = self._value.get(path, None)
        if v is None or v is NONE:
            return NONE
        if isinstance(v, Monad):
            v = v.value
        if isinstance(v, dict) is True and v.get('__dir__', False) is True:
            for k in v:
                if re.match(r"\_\_(.*)", k) is not None:
                    continue
                if fnmatch(k, patt) is not True:
                    continue
                _v = v[k]
                if isinstance(_v, dict) is True and _v.get('__dir__', False) is True and kw.get('dir', True) is True:
                    _nns = Namespace(_v)
                    self._clone(self, _nns, "stor")
                    _out.append(_nns)
                else:
                    if kw.get("type", None) is not None and isinstance(kw.get("type"), tuple) is True:
                        if isinstance(_v, kw.get("type")) is True:
                            _out.append(Just(_v))
                    else:
                        _out.append(Just(_v))
        else:
            return NONE
        res = L(_out)
        res.name = path
        return L(_out)
    def dir(self, path):
        _out = []
        v = self._value.get(path, None)
        if isNothing(v):
            return NONE
        if isinstance(v, Monad):
            v = v.value
        if isinstance(v, dict) is True and v.get('__dir__', False) is True:
            for k in v:
                if re.match(r"\_\_(.*)", k) is not None:
                    continue
                _out.append(k)
        return L(_out)
def C(*ns):
    for n in ns:
        if isinstance(n, Namespace) is True:
            n.C()

def f(ns, path, *args, **kw):
    return ns.f(path, *args, **kw)

def F(ns, path, *args, **kw):
    return ns.F(path, *args, **kw)

def rF(ns, path, *args, **kw):
    return ns.F(path, *args, **kw).value

def V(ns, path, value=NONE):
    return ns.V(path, value)

def lf(ns):
    return ns.f("/bin/f")

def lF(ns):
    return ns.f("/bin/F")

def lV(ns):
    return ns.f("/bin/V")
