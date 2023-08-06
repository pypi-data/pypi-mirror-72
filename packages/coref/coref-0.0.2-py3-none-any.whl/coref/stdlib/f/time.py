from oslash import Just
from coref.mod import nsValues, nsList
import time

def _timeStamp(ns):
    return time.time()

_lib = nsValues(
    {
        '/bin/time': _timeStamp
    }
)
