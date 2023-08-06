import sys
import re
import clint
import os.path
import socket
from fs.opener import open_fs
from fs.errors import CreateFailed
from coref.ns import *
from coref.cfg import nsCfgAppendFs, nsCfgListenParse
from coref.help import nsHelp
from clint.textui import colored

def nsArgs(ns):
    if len(sys.argv) == 0 or sys.argv[0] == '':
        name = 'coref'
    else:
        name = os.path.basename(sys.argv[0])

    path = "/etc/args"
    nsSet(ns, "/etc/name", name)
    argv = nsGet(ns, "/etc/argv").value
    args = nsGet(ns, "/etc/ARGV").value
    _args = nsGet(ns, path).value
    args = clint.arguments.Args(args, True)
    _path = "{}/default".format(path)
    isFlag = False
    prev = None
    while True:
        a = args.pop(0)
        if a is None or isinstance(a, str) is not True:
            break
        if len(a) == 0:
            continue
        if re.match(r'--help', a) is not None:
            if prev is None:
                hpath = "/help/cmd/default"
            else:
                hpath = "/help/cmd/{}".format(prev)
            nsHelp(ns, hpath)
            raise SystemExit
        if re.match(r'\+(.*)', a) is not None and isFlag is False:
            nsSet(ns, "/etc/flags/{}".format(a[1:]), True)
            continue
        if re.match(r'\-(\w+)', a) is not None and isFlag is False:
            nsSet(ns, "/etc/flags/{}".format(a[1:]), False)
            continue
        if re.match(r'--(.*)', a) is not None and isFlag is False:
            isFlag = True
            prev = a[2:].lower()
            continue
        if re.match(r'--(.*)', a) is not None and isFlag is True:
            nsSet(ns, "{}/{}".format(_path, prev), True)
            isFlag = True
            prev = a[2:].lower()
            continue
        if re.match(r'--(.*)', a) is None and isFlag is True:
            prevValue = nsGet(ns, "{}/{}".format(_path, prev)).value
            if prevValue is None:
                nsSet(ns, "{}/{}".format(_path, prev), a)
            elif prevValue is not None and isinstance(prevValue, list) is not True:
                nsSet(ns, "{}/{}".format(_path, prev), [prevValue, a])
            elif prevValue is not None and isinstance(prevValue, list) is True:
                prevValue.append(a)
            else:
                nsSet(ns, "{}/{}".format(_path, prev), a)
            isFlag = False
            continue
        if re.match(r'--(.*)', a) is None and isFlag is False:
            prev = a
            argv.append(a)
            _path = "{}/{}".format(path, a)
            nsMkdir(ns, _path)
            continue
    cfg_files = nsGet(ns, "/config/cfg.files").value
    cfg_files += nsGet(ns, "/etc/args/default/conf").value
    userlib = nsGet(ns, "/config/user.library").value
    userlib += nsGet(ns, "/etc/args/default/userlib").value
    nsArgsParsePopulate(ns, "/etc/args/default/listen", "/etc/listen", nsCfgListenParse)
    nsArgsParsePopulate(ns, "/etc/args/default/rpc", "/etc/rpc", nsCfgListenParse)
    nsArgsPopulate(ns, "/etc/args/default/group", "/etc/groups")
    for b in nsGet(ns, "/etc/args/default/bootstrap").value:
        nsCfgAppendFs(ns, b)
    nsSet(ns, "/etc/name", nsGet(ns, "/etc/args/default/appname", name))
    nsSet(ns, "/etc/hostname", nsGet(ns, "/etc/args/default/hostname", socket.gethostname()))
    nsSet(ns, "/etc/daemonize", nsGet(ns, "/etc/flags/daemonize", False).value)
    nsSet(ns, "/etc/console", nsGet(ns, "/etc/flags/console", False).value)
    nsSet(ns, "/etc/log", nsGet(ns, "/etc/flags/log", False).value)
    colored.DISABLE_COLOR=not nsGet(ns, "/etc/flags/color", False).value
    return ns

def nsArgsPopulate(ns, _from, _to):
    _to_val = nsGet(ns, _to).value
    if _to_val is None:
        nsSet(ns, _to, [])
        _to_val = nsGet(ns, _to)
    _from_val = nsGet(ns, _from)
    if _from_val is None:
        return
    if isinstance(_from_val, list) is not True:
        return
    _to_val += _from_val

def nsArgsParsePopulate(ns, _from, _to, parser):
    _from_data = nsGet(ns, _from).value
    if _from_data is None:
        _from_data = []
        nsSet(ns, _from, _from_data)
    _to_data = nsGet(ns, _to).value
    if _to_data is None:
        _to_data = {}
        nsSet(ns, _to, _to_data)
    for i in _from_data:
        _k, _v = parser(ns, i)
        if _k not in _to_data:
            _to_data[_k] = _v
    return _to_data



def nsCmd(ns):
    argv = nsGet(ns, "/etc/argv", []).value
    root = nsGet(ns, "/config/cmd.path").value
    is_cmd_run = nsGet(ns, "/config/cmd.run")
    if is_cmd_run == TRUE:
        return ns
    for k in argv:
        out = ns.f("{}/{}".format(root, k))()
        nsSet(ns, "/config/cmd.run", True)
    return ns
