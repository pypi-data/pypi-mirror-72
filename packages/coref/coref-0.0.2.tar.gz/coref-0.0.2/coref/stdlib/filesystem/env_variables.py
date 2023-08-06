import os
from coref.mod import nsValues, nsList

def nsEnvVars():
    _res = {}
    for e in os.environ:
        _res[f"/sys/env/variables/{e}"] = os.environ[e]
    return _res

_set = nsValues(
    nsEnvVars()
)
