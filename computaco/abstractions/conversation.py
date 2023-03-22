from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Message:
    name: str
    text: str

    timestamp: datetime = field(default_factory=datetime.now)

    def __repr__(self):
        return f"{self.name}: {self.text}"


@dataclass
class Conversation:
    _messages: list[Message] = field(default_factory=list)

    def to_json(self):
        return [
            {
                "text": message.text,
                "role": message.name,
            }
            for message in self._messages
        ]

    def to_string(self, include_timestamps: bool = False):
        return "\n".join(
            [
                (
                    f"{message.name} at {message.timestamp.strftime('%b %d, %Y %I:%M:%S %p')}: {message.text}"
                    f"{message.name}: {message.text}"
                )
                for message in self._messages
            ]
        )

    def __repr__(self):
        return self.to_string()

    def __len__(self):
        return len(self._messages)

    def __getitem__(self, index):
        return self._messages[index]

    def __setitem__(self, index, value):
        self._messages[index] = value

    def __delitem__(self, index):
        del self._messages[index]

    def __iter__(self):
        return iter(self._messages)

    def __reversed__(self):
        return reversed(self._messages)

    def __contains__(self, item):
        return item in self._messages

    def append(self, value):
        self._messages.append(value)

    def insert(self, index, value):
        self._messages.insert(index, value)

    def clear(self):
        self._messages.clear()
