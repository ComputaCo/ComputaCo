from __future__ import annotations
from datetime import datetime
from enum import Enum

from typing import Literal, Union
import json
import os

import attr

from computaco.abstractions.types import Audio, Image, Video
from computaco.agents.agent import Agent
from computaco.tools.tool import Environment, Tool


@attr.s
class Conversation(Tool):
    class MessageTypes(Enum):
        text = str
        image = Image
        audio = Audio
        video = Video

    class Message:
        sender: Agent
        timestamp: datetime
        content: any

    messages: list[Message] = []
    T_INPUT = any
    T_OUTPUT = any

    def _fn(self, agent: Agent, input: T_INPUT) -> T_OUTPUT:
        message = self.Message(sender=agent, timestamp=datetime.now(), content=input)
        self.messages.append(message)
        return message.content

    def to_markdown(self):
        markdown = ""
        for message in self.messages:
            markdown += f"**{message.sender.name} ({message.timestamp.strftime('%Y-%m-%d %H:%M:%S')}):** {message.content}\n"
        return markdown

    def save(self, format: Literal["markdown", "json", "text"]):
        if format == "markdown":
            content = self.to_markdown()
            file_ext = "md"
        elif format == "json":
            content = json.dumps(
                [
                    {
                        "sender": msg.sender.name,
                        "timestamp": msg.timestamp.isoformat(),
                        "content": msg.content,
                    }
                    for msg in self.messages
                ]
            )
            file_ext = "json"
        elif format == "text":
            content = "\n".join(
                f"{msg.sender.name} ({msg.timestamp.strftime('%Y-%m-%d %H:%M:%S')}): {msg.content}"
                for msg in self.messages
            )
            file_ext = "txt"

        file_name = f"conversation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{file_ext}"
        with open(file_name, "w") as f:
            f.write(content)

    @classmethod
    def load(
        cls, env: Environment, file_path: str, format: Literal["markdown", "json", "text"]
    ) -> Conversation:
        if format == "json":
            with open(file_path, "r") as f:
                data = json.load(f)

            conversation = cls(env=env)
            for msg_data in data:
                sender = Agent(msg_data["sender"], "", [])
                timestamp = datetime.fromisoformat(msg_data["timestamp"])
                content = msg_data["content"]
                message = conversation.Message(
                    sender=sender, timestamp=timestamp, content=content
                )
                conversation.messages.append(message)
            return conversation
        else:
            raise NotImplementedError(
                "Loading from markdown and text formats is not supported yet."
            )
