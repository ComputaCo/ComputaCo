from datetime import datetime
import json
from dataclasses import dataclass
from pathlib import Path

from git import Repo
import git


class Project:

    name: str
    path: Path
    repo: Repo = None
    summary: str = ""

    conversations = {}  # {task: <conversations>}
    files = {}  # {group: <files>}

    def __init__(self, path):
        self.path = Path(path)
        # open git repository if it exists
        try:
            self.repo = Repo(self.path)
        # create git repository if it doesn't exist
        except git.InvalidGitRepositoryError:
            self.repo = Repo.init(self.path)
        # create .computacode directory if it doesn't exist
        if not (self.path / ".computacode").exists():
            (self.path / ".computacode").mkdir()
            self.checkpoint()
        if (self.path / ".computacode" / "project.json").exists():
            with open(self.path / ".computacode" / "project.json") as f:
                self.__dict__.update(json.load(f))

    @property
    def all_files(self):
        return [file for group in self.files.values() for file in group]

    def checkpoint(self, message=None):
        # save snapshot of self to json
        with open(self.path / ".computacode" / "project.json", "w") as f:
            json.dump(self.__dict__, f, indent=4)
        # git add all changes
        self.repo.index.add(["."])
        # git commit all changes
        if message is None:
            # message: "checkpoint-<branch>-<num_heads>-<YYYY>-<MM>-<DD>-<HH>-<MM>-<SS.ffffff>"
            message = (
                f"checkpoint-{self.repo.active_branch.name}-"
                f"{len(self.repo.heads)}-{datetime.now().strftime('%Y-%m-%d-%H-%M-%S.%f')}"
            )
        self.repo.index.commit(message)

    def __repr__(self):
        return self.name

    @property
    def datapath(self):
        return self.path / ".computaco"
