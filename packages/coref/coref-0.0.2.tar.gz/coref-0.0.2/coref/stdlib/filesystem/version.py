from coref.mod import nsValues, nsList
from coref.version import *

_set = nsValues(
    {
        '/etc/coref/version': VERSION,
        '/etc/coref/release': RELEASE,
        '/etc/coref/url': URL,
        '/etc/coref/author': AUTHOR,
        '/etc/coref/email': AUTHOR_EMAIL,
        '/etc/coref/license': LICENSE,
        '/etc/coref/license.txt': LICENSE_txt,
        '/etc/coref/README.md': READ_me,
        '/etc/version': '0.0',
        '/etc/release': '0.0.1',
    }
)

_mkdir = [
    '/etc/coref',
]
