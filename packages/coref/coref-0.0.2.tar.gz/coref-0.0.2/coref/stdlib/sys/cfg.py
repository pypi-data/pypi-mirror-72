from fs.opener import open_fs
from fs.errors import CreateFailed
from coref.cfg import nsCfgGrammar, nsCfgLoad, nsCfgFSLoad, nsCfgAppendFs, nsCfgYamlLoad
from coref.mod import nsValues, nsList
from coref.ns import nsGet
from coref.internal.monad.internal import isNothing

def _systemCfgInit(ns):
    nsCfgGrammar(ns)
    return True


def _systemFSInit(ns):
    for c in nsGet(ns, "/config/cfg.path").value:
        nsCfgAppendFs(ns, c)
    return True

_lib = {
    '/bin/C': nsCfgLoad,
    '/bin/Cfg': nsCfgFSLoad,
    '/bin/FSCfg': nsCfgAppendFs,
    '/bin/yaml': nsCfgYamlLoad,
}

_set = nsValues (
    {
        "/config/cfg.path": ['osfs://.','osfs://tests'],
        "/config/cfg.fs": {},
        "/config/cfg.files": [],
        "/config/cmd.path": "/usr/local/bin"
    }
)

_init = {
    2: {
        'bund': {
            'start': _systemCfgInit,
        }
    },
    900: {
        'bund': {
            'start': _systemFSInit
        }
    }
}
