from oslash import Just
from coref.mod import nsValues, nsList
from coref.help import nsHelp


def nsDisplayLicense(ns):
    nsHelp(ns, "/etc/coref/license.txt")
    return True

_set = nsValues(
    {
        '/help/cmd/license': """
This command displays the license under which core.F is distributed.
"""
    }
)

_lib = nsValues(
    {
        '/usr/local/bin/license': nsDisplayLicense
    }
)
