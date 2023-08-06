import sys
import signal
import atexit
from coref.internal.util import partial
from coref import *

def nsInitRun(ns, path, name, action=None):
    _fun = ns.V(f"{path}/{name}")
    if isNothing(_fun) is True:
        return False
    print ("init()", f"{path}/{name}")
    if action is None:
        if callable(_fun.value) is not True:
            return False
        if _fun.value() is not True:
            return False
    else:
        return action(ns, _fun)
    return True

def nsInit(ns):
    atexit.register(nsStop, ns)
    signal.signal(signal.SIGTERM, nsForceExit)
    init = ns.dir("/etc/init.d")
    for i in init.sort():
        ctx = ns.dir(f"/etc/init.d/{i}")
        for k in ctx.sort():
            path = f"/etc/init.d/{i}/{k}"
            if nsInitRun(ns, path, 'start') is False:
                break
    return

def nsForceExit(signo, frame):
    sys.exit(0)

def nsStop(ns):
    init = ns.dir("/etc/init.d")
    for i in init.sort().reverse():
        ctx = ns.dir(f"/etc/init.d/{i}")
        for k in ctx.sort().reverse():
            path = f"/etc/init.d/{i}/{k}"
            if nsInitRun(ns, path, 'stop') is False:
                break
    return

def nsInitRegister(ns, fun, **kw):
    if isinstance(fun, Monad) is True:
        _fun = fun.value
    else:
        _fun = fun
    if callable(fun) is not True:
        return False
    name = kw.get('name', _fun.__name__)
    level = kw.get('level', 999)
    action = kw.get('action', 'start')
    _fun = partial(_fun, ns)
    ns.V(f"/etc/init.d/{level}/{name}/{action}", _fun)
    return True
