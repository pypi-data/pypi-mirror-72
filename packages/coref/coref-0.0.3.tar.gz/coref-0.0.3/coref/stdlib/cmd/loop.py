import os
import os.path
import psutil
import resource
from setproctitle import setproctitle
from coref import *
from oslash import Just
from coref.mod import nsValues, nsList
from coref.ns import *
from coref.gevent import nsLoopSys, nsLoopUser
from coref.init import nsInitRegister

def daemonize(umask=0o027):
    if gevent.fork():
        os._exit(0)
    os.setsid()
    if gevent.fork():
        os._exit(0)
    os.umask(umask)
    os.open(os.devnull, os.O_RDWR)
    gevent.reinit()

def nsDaemonRemovePid(ns):
    pid = nsDaemonLoadPid(ns)
    if pid is not None:
        return
    pidFile = nsGet(ns, "/sys/env/pidFile").value
    if os.path.exists(pidFile) and os.path.isfile(pidFile):
        os.remove(pidFile)

def nsDaemonMkPID(ns):
    if nsDaemonLoadPid(ns) is not None:
        return
    with open(nsGet(ns, "/sys/env/pidFile").value, "w") as f:
        f.write(str(os.getpid()))

def nsDaemonLoadPid(ns):
    try:
        with open(nsGet(ns, "/sys/env/pidFile").value, "r") as f:
            try:
                pid = int(f.read())
            except ValueError:
                return None
    except FileNotFoundError:
        return None
    try:
        me = psutil.Process(pid)
    except psutil.NoSuchProcess:
        return None
    if me.is_running() is True:
        return pid
    return None

def nsDaemonProcTitle(ns, msg=None):
    if msg is None:
        _msg = nsGet(ns, "/etc/processTitle").value
        if _msg is None:
            _msg = "core.F($etc.name) is running on $etc.hostname"
    else:
        _msg = msg
    _msg = nsTxt(ns, _msg)
    setproctitle(_msg)
    return _msg

def nsLoopPrep(ns):
    nsDaemonProcTitle(ns)
    nsSet(ns, "/sys/env/pid", os.getpid())
    nsSet(ns, "/sys/env/me", psutil.Process(os.getpid()))
    nsSet(ns, "/sys/env/pidFile", "{}/{}.pid".format(nsGet(ns, "/sys/env/apphome").value, nsGet(ns, "/etc/name").value))
    working_directory=nsGet(ns, "/sys/env/apphome").value
    try:
       os.chdir(working_directory)
    except:
       pass
    uid = nsGet(ns, "/sys/env/uid").value
    try:
       os.setuid(uid)
    except:
       pass
    resource.setrlimit(resource.RLIMIT_CORE, (0,0))


def nsLoopSysMain(ns):
    nsLoopPrep(ns)
    nsLoopSys(ns)

def nsLoopUserMain(ns):
    nsLoopPrep(ns)
    nsLoopUser(ns)

def nsLoop(ns):
    if nsGet(ns, "/etc/daemonize").value is True:
        daemonize()
        nsDaemonMkPID(ns)
        nsInitRegister(ns, nsDaemonRemovePid, name='removepid', action='stop')
    nsLoopUserMain(ns)
    return True

def nsDaemon(ns):
    if nsGet(ns, "/etc/daemonize").value is True:
        daemonize()
        nsDaemonMkPID(ns)
        nsInitRegister(ns, nsDaemonRemovePid, name='removepid', action='stop')
    nsLoopSysMain(ns)
    return True

def nsDaemonStop(ns):
    pid = nsDaemonLoadPid(ns)
    if pid is not None:
        me = psutil.Process(pid)
        me.terminate()
    nsDaemonRemovePid(ns)


_set = nsValues(
    {
        '/help/cmd/loop': """
This command executes a user-only threads eventloop.
""",
        '/help/cmd/daemon': """
This command executes a user&system threads eventloop.
""",
        '/help/cmd/start': """
This command executes a user&system threads eventloop.
""",
        '/help/cmd/stop': """
This command stops the daemon if one is running.
"""
    }
)

_lib = nsValues(
    {
        '/usr/local/bin/loop': nsLoop,
        '/usr/local/bin/daemon': nsDaemon,
        '/usr/local/bin/start': nsDaemon,
        '/usr/local/bin/stop': nsDaemonStop,
        '/bin/setproctitle': nsDaemonProcTitle,
    }
)
