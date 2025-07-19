class Options:
    __slots__ = ('method', 'path', 'params')

    def __init__(self, method, path, *, params=None):
        self.method = method
        self.path = path
        self.params = params

    @classmethod
    def get(cls, path, *, params=None):
        return cls('GET', path, params=params)