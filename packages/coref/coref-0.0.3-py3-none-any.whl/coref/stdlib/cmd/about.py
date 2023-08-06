from oslash import Just
from coref.mod import nsValues, nsList
from coref.help import nsHelp


def nsDisplayReadme(ns):
    nsHelp(ns, "/etc/coref/README.md")
    return True

_set = nsValues(
    {
        '/help/cmd/about': """
This command displays general documentation about core.F .
"""
    }
)

_lib = nsValues(
    {
        '/usr/local/bin/about': nsDisplayReadme
    }
)
