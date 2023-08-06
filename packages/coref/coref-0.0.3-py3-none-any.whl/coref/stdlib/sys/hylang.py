from coref.hylang import nsHYInit, nsHyEval, nsHyPipeline

def _hylangInit(ns):
    nsHYInit(ns)
    return True

_lib = {
    '/bin/hy': nsHyEval,
    '/bin/hy|': nsHyPipeline,
}

_init = {
    1: {
        'hylang': {
            'start': _hylangInit,
        }
    },
}

_mkdir = [
    '/pbin',
    '/psbin',
    '/etc/hy.startup',
]
