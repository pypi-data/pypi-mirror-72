import time
from coref import *
from apscheduler.schedulers.gevent import GeventScheduler


def nsGeventTick(ns):
    ns.V("/dev/time", time.time())

def nsSchedulerIntervalJob(ns, seconds, name, fun, *args, **kw):
    if len(args) > 0 and args[0] is ns:
        _fun = fun
    else:
        _fun = partial(fun, ns)
    scheduler = nsGet(ns, "/sys/scheduler").value
    return scheduler.add_job(_fun, 'interval', seconds=seconds, name=name, args=args, kwargs=kw, max_instances=nsGet(ns, "/etc/maxScheduleJobs", 10).value, replace_existing=True)

def nsSchedulerPS(ns):
    return nsGet(ns, "/sys/scheduler").get_jobs()

def nsGeventPS(ns):
    return nsGet(ns, "/sys/greenlets")[1:] +  nsGet(ns, "/sys/greenlets.user")

def nsGevent(ns, *args, **kw):
    ns.V("/sys/scheduler", GeventScheduler())
    s = nsGet(ns, "/sys/scheduler").value
    nsSchedulerIntervalJob(ns, 60, "/dev/time", nsGeventTick)
    g = s.start()
    nsProcAlloc(ns, "scheduler", g, scheduler=s)
    glist = nsGet(ns, "/sys/greenlets").value
    glist.append(g)
    return True

def nsProcAlloc(ns, name, g, **kw):
    path = "/proc/{}".format(name)
    nsMkdir(ns, path)
    for k in kw:
        nsSet(ns, "{}/{}".format(path, k), kw[k])
    nsSet(ns, "{}/proc".format(path), g)
    nsSet(ns, "{}/stamp".format(path), time.time())
    return ns

def nsSpawn(ns, name, fun, *args, **kw):
    if len(args) > 0 and args[0] is ns:
        _fun = fun
    else:
        _fun = partial(fun, ns)
    g = gevent.Greenlet.spawn(_fun, *args, **kw)
    g.name = name
    nsProcAlloc(ns, name, g)
    glist = nsGet(ns, "/sys/greenlets.user").value
    glist.append(g)
    g.start()
    return ns

def nsDaemon(ns, name, fun, *args, **kw):
    if (len(args) > 0 and args[0] is ns) or kw.get("_raw", False) is True:
        _fun = fun
    else:
        _fun = partial(fun, ns)
    if "_raw" in kw:
        del kw["_raw"]
    g = gevent.Greenlet.spawn(_fun, *args, **kw)
    g.name = name
    nsProcAlloc(ns, name, g)
    glist = nsGet(ns, "/sys/greenlets")
    glist.append(g)
    g.start()
    return ns

def _ns_greenlet_loop(ns, *path):
    glist = []
    for p in path:
        glist += nsGet(ns, p).value
    try:
        gevent.joinall(glist)
    except:
        nsKillAll(ns)
        pass

def nsLoopUser(ns):
    return _ns_greenlet_loop(ns, "/sys/greenlets.user")

def nsLoopSys(ns):
    return _ns_greenlet_loop(ns, "/sys/greenlets", "/sys/greenlets.user")


def nsKillAll(ns):
    if nsGet(ns, "/sys/greenlets.kill") is True:
        return ns
    nsGet(ns, "/sys/scheduler").value.shutdown(wait=True)
    gevent.killall(nsGet(ns, "/sys/greenlets").value[1:])
    gevent.killall(nsGet(ns, "/sys/greenlets.user").value)
    nsSet(ns, "/sys/greenlets.kill", True)
    return ns
