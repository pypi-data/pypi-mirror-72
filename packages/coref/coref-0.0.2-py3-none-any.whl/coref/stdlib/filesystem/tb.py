import os
from collections import namedtuple
from coref.internal.rb import RingBuffer
from coref.mod import nsValues, nsList

_EXCEPTION = namedtuple('Exception', ['type', 'value', 'traceback'])
_F_TRACE = namedtuple('Trace', ['stamp', 'fun', 'time', 'args', 'kw'])
_F_TRACE_CAP = 100
_TB_CAP = 100


_set = nsValues(
    {
        '/sys/traceback/exists': False,
        '/sys/traceback/tb': RingBuffer(capacity=_TB_CAP, dtype=_EXCEPTION),
        '/sys/traceback/ftrace': RingBuffer(capacity=_F_TRACE_CAP, dtype=_F_TRACE),
        '/etc/traceCapacity': _F_TRACE_CAP,
        '/etc/tracebackCapacity': _TB_CAP,
        '/config/exception': _EXCEPTION,
        '/config/ftrace': _F_TRACE,
    }
)

_mkdir = [
    '/sys/traceback'
]
