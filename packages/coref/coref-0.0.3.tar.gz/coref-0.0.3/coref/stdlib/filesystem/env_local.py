import uuid
import os
import time
from coref.internal.path import check_the_path
from coref.cfg import nsCfgAppendFs
from coref.ns import *

def nsCookie(ns, cookie):
    return Just(cookie) == nsGet(ns, "/security/cookie")

def nsEnvLocal(ns):
    CNS_NAME = nsGet(ns, "/etc/name").value
    CNS_HOME = "{}/.{}".format(ns.V('/sys/env/home').value, ns.V('/etc/name').value)
    ns.V('/sys/env/apphome', CNS_HOME)
    if check_the_path(ns, CNS_HOME) is not True:
        os.mkdir(CNS_HOME)
        os.chmod(CNS_HOME, 0o700)
    cfg_path = nsGet(ns, "/config/cfg.path").value
    cfg_path.append("osfs://{}".format(CNS_HOME))
    if check_the_path(ns, "/etc/{}".format(CNS_NAME)) is True:
        cfg_path.append("osfs:///etc/{}".format(CNS_NAME))
    cfg_path.append("osfs:///etc/coref/{}".format(CNS_NAME))
    nsSet(ns, "/config/cfg.path", cfg_path)
    nsSet(ns, "/sys/env/pidFile", "{}/{}.pid".format(CNS_HOME, CNS_NAME))
    for p in cfg_path:
        nsCfgAppendFs(ns, p)

def nsEnvLocalCleanup(ns):
    CNS_HOME = ns.V('/sys/env/apphome')


def nsSecurityStart(ns, *args, **kw):
    nsSet(ns, "/security/cookie", str(uuid.uuid4()))
    if nsGet(ns, "/etc/flags/cookie").value is False:
        return True
    apphome = nsGet(ns, "/sys/env/apphome").value
    with open("{}/cookie".format(apphome), "w") as f:
        f.write(nsGet(ns, "/security/cookie").value)
    return True


def nsSecurityStop(ns, *args, **kw):
    if nsGet(ns, "/etc/flags/cookie").value is False:
        return True
    apphome = nsGet(ns, "/sys/env/apphome").value
    cookie_path = "{}/cookie".format(apphome)
    if os.path.exists(cookie_path) is True and os.path.isfile(cookie_path) is True:
        os.unlink(cookie_path)
    return

_lib = {
    '/bin/cookie': nsCookie,
}

_init = {
    900: {
        'env_local': {
            'start': nsEnvLocal,
            'stop': nsEnvLocalCleanup
        }
    },
    901: {
        'sec_local': {
            'start': nsSecurityStart,
            'stop': nsSecurityStop
        }
    }
}

_mkdir = [
    '/security'
]
