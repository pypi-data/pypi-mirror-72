from gevent import monkey
monkey.patch_all()
import gevent

import sys
from oslash import Monad, Just, Nothing
from coref.internal.monad import *
from coref.internal.monad.internal import *
from coref.ns import *
from coref.mod import *
from coref.cfg import nsCfgLoad, nsCfgFSLoad
from coref.arrghs import nsArgs, nsCmd
from coref.help import nsHelp
from coref.internal.util import partial

def NS(argv=sys.argv[1:], *cfg, **kw):
    ns = nsNS(argv, *cfg, **kw)
    nsCmd(ns)
    return (ns, ns.V("/bin/f").value, ns.V("/bin/F").value)
