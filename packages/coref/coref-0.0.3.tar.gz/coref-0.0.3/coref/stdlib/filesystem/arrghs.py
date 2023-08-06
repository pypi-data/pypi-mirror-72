from coref.arrghs import nsArgs
from coref.mod import nsValues, nsList


_set = nsValues(
    {
        '/etc/args/default/conf': [],
        '/etc/args/default/bootstrap': [],
        '/etc/args/default/userlib': [],
        '/etc/args/default/conf': [],
        '/etc/args/default/listen': [],
        '/etc/args/default/rpc': [],
        '/etc/args/default/group': [],
        '/etc/argv': [],
        '/etc/rpc': {},
        '/etc/groups': [],
        '/etc/flags/console': True,
        '/etc/flags/log': False,
        '/etc/flags/stdout': True,
        '/etc/flags/daemonize': False,
        '/etc/flags/color': True,
        '/etc/flags/pid': False,
        '/etc/flags/direct': True,
        '/etc/flags/cookie': False,
    }
)

_mkdir = [
    '/etc/args',
    '/etc/args/default',
    '/etc/flags',
    '/help',
    '/help/cmd',
]

_init = {
    3: {
        'arrghs': {
            'start': nsArgs,
        }
    },
}
