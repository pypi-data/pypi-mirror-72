from coref.gevent import *

_lib = {
    '/bin/spawn': nsSpawn,
    '/bin/daemon': nsDaemon,
    '/bin/loop': nsLoopUser,
    '/sbin/loop': nsLoopSys,
    '/sbin/killall': nsKillAll,
    '/bin/schedule': nsSchedulerIntervalJob,
    '/bin/scheduleN': nsSchedulerIntervalJob,
    '/bin/scheduleINT': nsSchedulerIntervalJob,
    '/bin/sps': nsSchedulerPS,
    '/bin/ps': nsGeventPS,
}

_set = nsValues (
    {
        '/sys/greenlets': [],
        '/sys/greenlets.user': [],
        '/sys/greenlets.kill': False,
        '/dev/time': 0
    }
)

_init = {
    2: {
        'gevent': {
            'start': nsGevent,
        }
    },
}

_mkdir = [
    '/proc',
]
