from secrets import token_hex

class Command:
    def __init__(self, fn):
        self._fn = fn
        self.which = token_hex()

    def __call__(self, *args, **kwargs):
        return self._fn(*args, **kwargs)