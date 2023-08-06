from coref import *
import fnmatch
from hy import read_str, eval

def nsImportPfun(ns, env, *vpath):
    for p in vpath:
        env.update(nsLs(ns, p).value)
    return env


def nsHYmkenv(ns, **kw):
    env = globals()
    env["nsGet"] = nsGet
    env["nsSet"] = nsSet
    env["f"] = nsGet(ns, "/bin/f").value
    env["F"] = nsGet(ns, "/bin/rF").value
    env["V"] = nsGet(ns, "/bin/V").value
    env["stamp"] = nsGet(ns, "/bin/time").value
    env["ns"] = ns
    return env

def nsHYInit(ns):
    nsHyEval(ns, '(nsSet ns "/sys/hylang.enabled" True)')
    nsHyEval(ns, '(nsSet ns "/sys/hylang.enabled.stamp" ((f "/bin/time")))')
    return True

def nsHyEval(ns, expression):
    env = nsHYmkenv(ns)
    env = nsImportPfun(ns, env, "/psbin", "/pbin")
    _expr = read_str(str(expression))
    _res = eval(_expr, env)
    return _res

def nsHyPipeline(ns, expression):
    _exp = u"""(->
    {})""".format(expression)
    return nsHyEval(ns, _exp)
