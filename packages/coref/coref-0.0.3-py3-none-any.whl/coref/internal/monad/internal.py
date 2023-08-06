from oslash.maybe import Just, Nothing

Value = Just
NONE=Nothing()
TRUE=Just(True)
FALSE=Just(False)

def isNothing(x):
    return x is None or x == NONE or isinstance(x, Nothing)
