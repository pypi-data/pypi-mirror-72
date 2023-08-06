def unique(x: list) -> list:
    return list(set(x))

def partial(func, *args, **keywords):
    def f(*fargs, **fkeywords):
        newkeywords = keywords.copy()
        newkeywords.update(fkeywords)
        return func(*(args + fargs), **newkeywords)
    f.func = func
    f.args = args
    f.keywords = keywords
    f.__name__ = func.__name__
    return f

def isIterable(x):
    try:
        iter(x)
        return True
    except TypeError:
        return False

def _mergedicts(dict1, dict2):
    for k in set(dict1.keys()).union(dict2.keys()):
        if k in dict1 and k in dict2:
            if isinstance(dict1[k], dict) and isinstance(dict2[k], dict):
                yield (k, dict(_mergedicts(dict1[k], dict2[k])))
            else:
                yield (k, dict2[k])
        elif k in dict1:
            yield (k, dict1[k])
        else:
            yield (k, dict2[k])

def mergedicts(dict1, dict2):
    return dict(_mergedicts(dict1, dict2))
