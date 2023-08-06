from oslash import Just
from coref.mod import nsValues, nsList
from coref.help import nsHelp


def nsStatus(ns):
    
    return True

_set = nsValues(
    {
        '/help/cmd/status': """
Displaying status of running daemon process .
"""
    }
)

_lib = nsValues(
    {
        '/usr/local/bin/status': nsStatus
    }
)
