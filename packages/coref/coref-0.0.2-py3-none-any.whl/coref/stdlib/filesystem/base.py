from coref.mod import nsValues, nsList

_set = nsValues(
    {
        '/etc/library': [],
        '/config/user.library': [],
        '/etc/answer': 42,
        '/config/var.redefine': True,
        '/etc/daemonize': False,
        '/etc/flags/truename': False,
        '/sys/hylang.enabled': False,
        '/config/cfg.files': [],
        '/etc/author': 'Unknown',
        '/etc/author.email': 'noreturn@example.com',
    }
)

_mkdir = [
    '/bin',
    '/sbin',
    '/home',
    '/tmp',
    '/etc',
    '/config',
    '/sys',
    '/usr',
    '/usr/local',
    '/usr/local/bin',
    '/proc',
    '/dev',
    '/templates',
    '/etc/corens',
    '/etc/init.d',
    '/etc/init.app',
]
