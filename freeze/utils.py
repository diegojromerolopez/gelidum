def isbuiltin(obj: object):
    return (
            obj is None or
            obj is True or
            obj is False or
            isinstance(obj, (int, float, bytes, complex, str))
    )
