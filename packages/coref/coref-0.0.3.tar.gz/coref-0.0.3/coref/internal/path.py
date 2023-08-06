import stat
import os.path

def expandPath(x):
    p = os.path.normpath(x)
    _p = p.split("/")
    _p = [i for i in _p if i]
    out = []
    for e in reversed(range(len(_p))):
        _d = "/"+"/".join(_p[:(e+1)])
        out.append(_d)
    return out

def check_the_path(ns, path):
    if not os.path.exists(path) and not os.path.isdir(path):
        return False
    _stat = os.stat(path)
    if _stat.st_uid != ns.V("/sys/env/uid").value:
        return False
    if stat.S_IMODE(os.lstat(path).st_mode) != 448:
        return False
    return True
