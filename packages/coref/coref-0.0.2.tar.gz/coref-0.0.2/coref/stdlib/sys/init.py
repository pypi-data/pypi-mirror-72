def _systemInit(ns):
    print("system init")
    return True

def _systemStop(ns):
    print("system stop")
    return True

def _systemInit999(ns):
    print("system init 999")
    return True

def _systemStop999(ns):
    print("system stop 999")
    return True

_init = {
    0: {
        'init': {
            'start': _systemInit,
            'stop': _systemStop,
        }
    },
    999: {
        'init': {
            'start': _systemInit999,
            'stop': _systemStop999
        }
    }
}
