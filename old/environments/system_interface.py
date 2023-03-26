import subprocess
from typing import Optional
import threading
from computaco.abstractions.abilities import HandlesTextInputOutput
from computaco.abstractions.environment import Environment
from computaco.abstractions.types import Text


class SystemInterface(Environment, HandlesTextInputOutput):
    def __init__(self, cwd, project_path, agents=[], cmd="bash"):
        super().__init__(project_path, agents)
        self._logger.info(f"SystemInterface {self.name} created.")
        self.cwd = cwd
        self.process = None
        self.cmd = cmd
        self.output_buffer = ""
        self.output_lock = threading.Lock()

    def __enter__(self):
        self.process = subprocess.Popen(
            self.cmd,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=self.cwd,
            text=True,
            bufsize=0,
        )

        self.output_thread = threading.Thread(target=self._read_output)
        self.output_thread.start()

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.process:
            self.process.terminate()
            self.process.wait()
            self.process = None

        if self.output_thread:
            self.output_thread.join()
            self.output_thread = None

    def input_text(self, text: Text, *args, sender="Info", remember=True, **kwargs):
        if self.process is None:
            raise RuntimeError("SystemInterface process not running")

        self.process.stdin.write(text)
        self.process.stdin.flush()

    def _read_output(self):
        while self.process is not None:
            output = self.process.stdout.readline()
            if output:
                with self.output_lock:
                    self._notify_agents(output.strip())
                    self.output_buffer += output
            else:
                break

    def _notify_agents(self, text: Text):
        for agent in self.agents:
            agent.input(text)

    def output_text(self, *args, remember=True, **kwargs) -> Optional[Text]:
        with self.output_lock:
            output = self.output_buffer
            self.output_buffer = ""
            return output.strip() if output else None
