import sys
import dill
import fnmatch
import os.path
import uuid
import time
from collections import namedtuple
from vedis import Vedis

class Vstor:
    def __init__(self):
        self.mounts = {}
        self.fs = {}
        self.rec = namedtuple('Mount', ['path', 'patt'])

    def mount(self, name, path, patt=[]):
        if name in self.mounts:
            return (self.mounts[name], self.fs[name])
        self.mounts[name] = self.rec(path=path, patt=patt)
        self.fs[name] = Vedis(path)
        try:
            _ready = dill.loads(self.fs[name]['/__sys/__ready__'])
            if _ready is not True:
                raise KeyError
        except KeyError:
            self.fs[name]['/__sys/__name__'] = dill.dumps(name)
            self.fs[name]['/__sys/__path__'] = dill.dumps(path)
            self.fs[name]['/__sys/__patt__'] = dill.dumps(patt)
            self.fs[name]['/__sys/__ready__'] = dill.dumps(True)
            self.fs[name]['/__sys/__id__'] = dill.dumps(str(uuid.uuid4()))
        self.fs[name]['/__sys/__stamp__'] = dill.dumps(time.time())
        return self.mount(name, path, patt)

    def here(self, path):
        fs, _dir, _name = self.op(path)
        if fs is None:
            return False
        return True

    def read(self, name, path, default=None):
        if name not in self.fs:
            return default
        return dill.loads(self.fs[name][path])

    def op(self, path):
        _dir = os.path.dirname(path)
        _name = os.path.basename(path)
        for n in self.mounts:
            m = self.mounts[n]
            for p in m.patt:
                if fnmatch.fnmatch(path, p) is True:
                    return (self.fs[n], _dir, _name)
        return (None, None, None)

    def _set(self, fs, _dir, _name, value):
        path = f"{_dir}/{_name}"
        dir_s = fs.Set(_dir)
        fs.begin()
        if _name not in dir_s:
            dir_s.add(_name)
        fs[path] = dill.dumps(value)
        fs.commit()
        return value

    def set(self, path, value):
        fs, _dir, _name = self.op(path)
        if fs is None:
            return None
        return self._set(fs, _dir, _name, value)

    def get(self, path):
        fs, _dir, _name = self.op(path)
        if fs is None:
            return None
        if path in fs:
            return dill.loads(fs[path])
        return None
