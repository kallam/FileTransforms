from typing import Any, Callable


class ColumnMod:

    def __init__(self, prefix=None, suffix=None, func: Callable[[Any], Any] = None):
        self.prefix = prefix
        self.suffix = suffix
        self.func = func

    def apply(self, v):
        value = self.func(v) if self.func is not None else v
        return f'{self.prefix if self.prefix else ""}{value}{self.suffix if self.suffix else ""}'
