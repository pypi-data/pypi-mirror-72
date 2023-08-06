import sys
from coref import *
from coref.mod import nsImport
from coref.init import nsInit
from coref.app import nsAppInit


def nsNS(argv=sys.argv[1:], *cfg, **kw):
    ns = Namespace(kw)
    nsSet(ns, "/etc/ARGV", argv)
    for c in cfg:
        if isinstance(c, dict) is True:
            ns.update(c)
        elif isinstance(c, Dict) is True:
            ns += c
        elif callable(c) is True:
            c(ns)
        elif hasattr(c, 'isNamespace') is True:
            ns.update(c)
        else:
            pass
    nsImport(ns, 'coref.stdlib')
    more_libs = ns.V("/etc/libraries")
    if more_libs is not NONE:
        nsImport(ns, more_libs.value)
    more_libs = ns.V("/etc/user.library")
    if more_libs is not NONE:
        nsImport(ns, more_libs.value)
    nsInit(ns)
    nsAppInit(ns)
    return ns


def nsSet(ns, key, val):
    if nsGet(ns, "/config/var.redefine", True) == TRUE:
        return ns.V(key, val)
    return NONE

def nsGet(ns, path, default=NONE):
    if path[-1] == '/':
        path = path[:-1]
    v = ns.V(path)
    if v == NONE or v == Nothing() or v is None:
        if isinstance(default, Monad):
            return default
        return Just(default)
    return v

def nsLn(ns, _from, _to):
    v = ns.V(_from)
    if nsNothing(v):
        return v
    return ns.V(_to, v)

def nsDir(ns, path):
    return ns.cd(path)

def nsLs(ns, path):
    return ns.ls(path)

def nsMkdir(ns, path):
    return ns.mkdir(path)

def nsMemory(ns):
    return sys.getsizeof(ns)
