from pathlib import Path
from computaco.utils.storage import Storage


class Scoped(Storage):
    name: str
    ancestors: list[str] = []

    def __init__(self, name):
        self.ancestors = Scoped.singleton.ancestors.copy()  # copy from previous scope
        self.name = name
        super().__init__()  # this is where self becomes the topmost singleton

    @property
    def path(self):
        return Path(*self.ancestors, self.name)
