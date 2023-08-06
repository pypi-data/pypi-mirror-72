from oslash import Just
from coref.mod import nsValues, nsList
from coref.ns import *
import pyfiglet
from texttable import Texttable

def nsBanner(ns):
    pyfiglet.print_figlet(
            nsGet(ns, "/etc/name").value,
            nsGet(ns, "/etc/bannerFont", "isometric2").value,
            "GREEN:"
        )
    tbl = Texttable(nsGet(ns, "/etc/bannerTableWidth", 120).value)
    tbl.set_deco(Texttable.HEADER)
    tbl.add_rows(
            [
                ["Variable", "Value", "Description"],
                ["/etc/name", nsGet(ns, "/etc/name").value, "Name of the application"],
                ["/etc/hostname", nsGet(ns, "/etc/hostname").value, "Hostname"],
                ["/sys/env/platform/platform", nsGet(ns, "/sys/env/platform/platform").value, "Host platform"],
                ["/sys/env/platform/python", nsGet(ns, "/sys/env/platform/python").value, "Version of the Python"],
                ["/sys/env/platform/system", nsGet(ns, "/sys/env/platform/system").value, "OS Name"],
                ["/sys/env/user", nsGet(ns, "/sys/env/user").value, "Name of the user"],
                ["/sys/env/home", nsGet(ns, "/sys/env/home").value, "Home directory"],
                ["/sys/env/apphome", nsGet(ns, "/sys/env/apphome").value, "Application home"],
                ["/sys/env/pidFile", nsGet(ns, "/sys/env/pidFile").value, "PID file"],
                ["/config/user.library", nsGet(ns, "/config/user.library").value, "Application library"],
                ["/etc/daemonize", nsGet(ns, "/etc/daemonize").value, "Become daemon ?"],
                ["/etc/flags/internalServer",nsGet(ns, "/etc/flags/internalServer", False).value,"Enable internal server"],
                ["/etc/version", str(nsGet(ns, "/etc/version").value), "Application version"],
                ["/etc/release", nsGet(ns, "/etc/release").value, "Application release"],
                ["/etc/author", nsGet(ns, "/etc/author").value, "Author of application"],
                ["/etc/author.email", nsGet(ns, "/etc/author.email").value, "Author's email"],
                ["/etc/coref/version", str(nsGet(ns, "/etc/coref/version").value), "core.F version"],
                ["/etc/coref/release", nsGet(ns, "/etc/coref/release").value, "core.F release"],
                ["/config/RPCCatchCalls", nsGet(ns, "/config/RPCCatchCalls").value, "Trace RPC"],
                ["/etc/answer", nsGet(ns, "/etc/answer").value, "THE ANSWER"],
            ]
    )
    print(tbl.draw())
    return True

_set = nsValues(
    {
        '/help/cmd/banner': """
This command displays the system banner and configuration.
"""
    }
)

_lib = nsValues(
    {
        '/usr/local/bin/banner': nsBanner
    }
)
