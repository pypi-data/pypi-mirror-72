from oslash import Just
from coref.mod import nsValues, nsList
from coref.init import nsInitRegister
from coref.app import nsAppStart, nsInitAppRegister


_lib = nsValues(
    {
        '/bin/initRegister': nsInitRegister,
        '/bin/main': nsAppStart,
        '/bin/initAppRegister': nsInitAppRegister,
    }
)
