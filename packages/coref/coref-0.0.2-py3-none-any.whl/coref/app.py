import sys
import signal
import atexit
from coref.internal.util import partial
from coref.init import nsInitRun
from coref import *


def nsAppInit(ns):
    atexit.register(nsAppStop, ns)

def nsAppStart(ns):
    init = ns.dir("/etc/init.app")
    for i in init.sort():
        ctx = ns.dir(f"/etc/init.app/{i}")
        for k in ctx.sort():
            path = f"/etc/init.app/{i}/{k}"
            if nsInitRun(ns, path, 'start') is False:
                break
    return

def nsAppStop(ns):
    init = ns.dir("/etc/init.app")
    for i in init.sort().reverse():
        ctx = ns.dir(f"/etc/init.app/{i}")
        for k in ctx.sort().reverse():
            path = f"/etc/init.app/{i}/{k}"
            if nsInitRun(ns, path, 'stop') is False:
                break
    return

def nsInitAppRegister(ns, fun, **kw):
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
    ns.V(f"/etc/init.app/{level}/{name}/{action}", _fun)
    return True
