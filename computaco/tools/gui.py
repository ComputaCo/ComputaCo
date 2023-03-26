from __future__ import annotations

from dataclasses import dataclass
import attr
import numpy as np

from computaco.agents.agent import Agent
from computaco.tools.tool import Tool


@attr.s
class GUI(Tool):
    @dataclass
    class T_INPUT:
        mouse_movement: tuple[int, int]
        keyboard_state: dict[str, bool] = None  # specify this or text_input
        text_input: str = None  # convenience alternative to keyboard_state

    @dataclass
    class T_OUTPUT:
        screen: np.ndarray
        mouse_position: tuple[int, int]
        keyboard_state: dict[
            str, bool
        ]  # unlike T_INPUT.keyboard_state, this is always set
        text_output: str = None  # convenience alternative to keyboard_state

    def _fn(self, agent: Agent, input: GUI.T_INPUT) -> GUI.T_OUTPUT:
        raise NotImplementedError()  # Imlpement this.
