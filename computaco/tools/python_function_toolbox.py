from __future__ import annotations

from typing import Callable, List
import inspect

import attr

from computaco.agents.agent import Agent
from computaco.tools.tool import Tool


@attr.s
class PythonFunctionToolbox(Tool):
    fns: List[Callable] = attr.ib(default=[])

    T_INPUT = str
    T_OUTPUT = str

    _locals = attr.ib(default={})
    _globals = attr.ib(
        default={
            "__name__": "__main__",
            "__doc__": None,
            "__package__": None,
            "__loader__": __loader__,
            "__spec__": None,
            "__annotations__": {},
            "__builtins__": __builtins__,
        }
    )

    def print_signature(fn: Callable) -> str:
        signature = inspect.signature(fn)
        return f"{fn.__name__}{signature}"

    def _fn(
        self, agent: Agent, input: PythonFunctionToolbox.T_INPUT
    ) -> PythonFunctionToolbox.T_OUTPUT:
        # makes sure input is actually calling one of the allowed functions
        input = input.strip()
        if not any(input.startswith(fn) for fn in self.fns):
            return None
        return eval(input, {**locals, "agent": agent}, globals)
