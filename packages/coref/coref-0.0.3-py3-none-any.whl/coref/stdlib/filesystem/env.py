import platform
import uuid
import os
import psutil
import shutil
import getpass
import time
from pathlib import Path
from coref.mod import nsValues, nsList

home_total, home_used, home_free = shutil.disk_usage(str(Path.home()))

_set = nsValues(
    {
        '/sys/env/id': str(uuid.uuid4()),
        '/sys/env/platform/architecture': platform.architecture()[0],
        '/sys/env/platform/machine': platform.machine(),
        '/sys/env/platform/node': platform.node(),
        '/sys/env/platform/platform': platform.platform(),
        '/sys/env/platform/python': platform.python_version().split('.'),
        '/sys/env/platform/system': platform.system(),
        '/sys/env/platform/uname': platform.uname(),
        '/sys/env/uid': os.getuid(),
        '/sys/env/user': getpass.getuser(),
        '/sys/env/home': str(Path.home()),
        '/sys/env/cwd': os.getcwd(),
        '/sys/env/home.disk.size': home_total,
        '/sys/env/home.disk.used': home_used,
        '/sys/env/home.disk.free': home_free,
        '/sys/env/home.disk.free.percent': (home_free/home_total)*100,
        '/sys/env/bootTimestamp': time.time(),
        '/sys/env/pid': os.getpid(),
    }
)

_mkdir = [
    '/sys/env',
    '/sys/env/variables',
    '/sys/env/platform',
    '/sys/env/proc'
]
