from oslash import Just
from coref.mod import nsValues, nsList
from coref.gevent import nsLoopSys, nsLoopUser


_lib = nsValues(
    {
        '/bin/loop': nsLoopUser,
        '/sbin/loop': nsLoopSys,
    }
)
