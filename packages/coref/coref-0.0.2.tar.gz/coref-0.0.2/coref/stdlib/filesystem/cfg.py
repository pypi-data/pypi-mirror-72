import uuid
import os
import time
from coref.internal.path import check_the_path
from coref.cfg import nsCfgFSLoad
from coref.ns import *



def nsCfgStart(ns):
    for c in nsGet(ns, "/config/cfg.files").value:
        nsCfgFSLoad(ns, c)
    return True


def nsCfgStop(ns, *args, **kw):
    return True

_lib = {

}

_init = {
    901: {
        'cfg': {
            'start': nsCfgStart,
            'stop': nsCfgStop
        }
    }
}
