import asyncio
from pathlib import Path
import threading

import attr


@attr.define
class Process:

    path: Path = attr.ib()

    _done = False
    _task = None
    _start_lock = attr.ib(factory=threading.Lock, hide=True)
    _stop_lock = attr.ib(factory=threading.Lock, hide=True)

    MAXIMUM_JOIN_TIMEOUT = 120  # seconds to wait for thread to stop

    def __init__(self, path):
        self.path = Path(path)
        if self.path.exists():
            try:
                self.load_work()
            except:
                raise Exception(f"Failed to load previous work on the process: {self}")

    async def start(self):
        with self._start_lock:
            self._done = False
            self._task = asyncio.create_task(self.run())
            try:
                while True:
                    asyncio.sleep(0.1)
            except asyncio.CancelledError:
                pass
            if self.path.exists():
                try:
                    self.save_work()
                except:
                    raise Exception(f"Failed to save work on the process: {self}")
            await self._task

    async def stop(self):
        with self._stop_lock:
            self._done = True
            await self._task

    def run(self):
        raise NotImplementedError()

    def load_work(self):
        raise NotImplementedError()

    def save_work(self):
        raise NotImplementedError()
