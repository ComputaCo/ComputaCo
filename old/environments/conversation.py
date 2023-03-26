import json
import logging
from pathlib import Path
import pickle
from threading import Lock
import attr
from datetime import datetime
from computaco.abstractions.converts import Markdown
from computaco.abstractions.types import Audio, Image, Text, Video

import IPython.display
from computaco.abstractions.environment import Environment
import ipywidgets
import imageio
import soundfile as sf

from computaco.utils.logging import make_logger
from computaco.utils import english
from computaco.utils import consts
from computaco.abstractions import abilities
from computaco.agents.agent import Agent


@attr.s(auto_attribs=True)
class Message(Markdown):
    sender: str
    timestamp: datetime = attr.ib(default=datetime.now())

    def save(self, path: Path):
        # make directory if it doesn't exist
        path.mkdir(path, parents=True, exist_ok=True)
        # save pickle
        with path.open(path / "pickle.pkl", "wb") as f:
            pickle.dump(self, f)

    @classmethod
    def load(cls, path: Path):
        with path.open(path / "pickle.pkl", "rb") as f:
            return pickle.load(f)

    @property
    def name(self):
        return f"{self.timestamp.strftime(consts.TIME_FORMAT)}_{self.sender}"

    @property
    def markdown(self) -> str:
        return str(self)

    def __repr__(self):
        return IPython.display.Markdown(self.markdown)

    def __str__(self):
        return f"{self.__class__.__name__}({self.sender})"


class MultipleMessages(Message):
    messages: list[Message] = attr.ib(factory=list)

    def save(self, path: Path):
        for m in self.messages:
            m.save(path / m.name)
        super().save(path)

    def load(self, path: Path):
        super().load(path)
        # not used since the pickle already contains all the messages
        # for m in path.iterdir():
        #     self.messages.append(Message.load(m))

    @property
    def name(self):
        return english.join([m.name for m in self.messages])

    @property
    def markdown(self) -> str:
        return "\n\n".join([m.markdown for m in self.messages])

    def __repr__(self):
        return ipywidgets.VBox([m.__repr__() for m in self.messages])

    def __str__(self):
        return "\n\n".join([str(m) for m in self.messages])


class TextMessage(Message):
    text: str

    def __init__(self, sender, text, timestamp=None):
        super().__init__(sender=sender, timestamp=timestamp)
        self.text = text

    def save(self, path: Path):
        super().save(path)
        with path.open(path / "text.txt", encoding="w") as f:
            f.write(self.text)

    @property
    def markdown(self) -> str:
        return f"**{self.sender}**: {self.text}"

    def __str__(self):
        return f"{self.sender}: {self.text}"


class FileAssetMessage(TextMessage):
    def save(self, path: Path):
        super().save(path)
        fullpath = self._save(path)
        if self.text == "[Image]":
            caption = ""
            self.text = str(fullpath)
        else:
            caption = self.text

        self.markdown = f"![{caption}]({fullpath})"

    def _save(self, path) -> Path:
        """Saves the asset and returns its full path"""
        pass


class ImageMessage(TextMessage):
    image: Image

    def __init__(self, sender, image, text="[Image]", timestamp=None):
        super().__init__(sender=sender, timestamp=timestamp, text=text)
        self.image = image

    def _save(self, path: Path):
        fullpath = path / "image.png"
        imageio.imwrite(fullpath, self.image.numpy())
        return fullpath


class AudioMessage(TextMessage):
    audio: Audio

    def __init__(self, sender, audio, text="[Audio]", timestamp=None):
        super().__init__(sender=sender, timestamp=timestamp, text=text)
        self.audio = audio

    def _save(self, path: Path):
        fullpath = path / "audio.wav"
        sf.write(fullpath, self.audio.numpy(), consts.AUDIO_RATE)
        return fullpath


class VideoMessage(TextMessage):
    video: Video

    def __init__(self, sender, video, text="[Video]", timestamp=None):
        super().__init__(sender=sender, timestamp=timestamp, text=text)
        self.video = video

    def _save(self, path: Path):
        fullpath = path / "video.mp4"
        imageio.mimwrite(fullpath, self.video.numpy(), fps=consts.VIDEO_RATE)
        return fullpath


class Conversation(Environment, abilities.HandlesAnyInput, Markdown):
    speakers: list[Agent]
    bystanders: list[Agent]
    messages: list[Message]

    def __init__(
        self,
        path,
        speakers=[],
        bystanders=[],
        initial_message=None,
        final_message=None,
    ):
        self.speakers = speakers
        self.bystanders = bystanders
        self._evaluators = []
        self._initial_message = initial_message
        self._final_message = final_message
        self.messages = []
        self.initialize()
        super().__init__(path, speakers + bystanders)

    def input(self, message: str | Message | None, *args, remember=True, **kwargs):
        # TODO: support string input
        self._logger.info(f"Message sent: {message}")
        if message is None:
            self._logger.info("Conversation.input called with message=None. Returning.")
            return
        if remember == False:
            self._logger.warn(
                "Conversation.input called with remember=False. Ignoring message and returning."
            )
            return

        self._save_delta(message)
        self.messages.append(message)
        for agent in set(self.agents) + set(self._evaluators):
            agent.input(message)

    @property
    def agents(self):
        return self.speakers + self.bystanders

    def step(self):
        for speaker in self.speakers:
            self.input(speaker.output())

    def converse(self, rounds=5):
        for _ in range(rounds):
            self.step()

    def converse_until_done(
        self,
        is_done_message=None,
        evaluators=None,
        evaluators_and_queries: list[tuple[Agent | list[Agent], str | Message]] = None,
        num_steps=10,
    ):
        assert not (
            evaluators_and_queries is not None
            and (evaluators is not None or is_done_message is not None)
        ), "Conversation.converse_until_done: Cannot specify both evaluators_and_queries and evaluators/is_done_message."
        if evaluators_and_queries is None and (
            evaluators is not None and is_done_message is not None
        ):
            evaluators_and_queries = [(e, is_done_message) for e in evaluators]
        _evaluators_and_queries = []
        for e, query in evaluators_and_queries:
            if isinstance(e, list):
                for ei in e:
                    _evaluators_and_queries.append((ei, query))
            else:
                _evaluators_and_queries.append((e, query))

        self._evaluators = [e[0] for e in evaluators_and_queries]

        for _ in range(num_steps):
            self.step()

            # Check if each agent has made a decision
            for evaluator, query in evaluators_and_queries:
                if tc.decide(evaluator(query, remember=False)):
                    break
        # else:
        #     raise RuntimeError("Conversation.converse_until_done: No decision reached.")
        self._evaluators = []

    def join(self, *agents: list[Agent]):
        self.remove_bystanders(*agents)
        super().join(agents)
        self.input(
            f"{english.join(agent.name for agent in agents)} joined the conversation"
        )

    def leave(self, *agents: list[Agent]):
        self.remove_bystanders(*agents)
        super().leave(agents)
        self.input(
            f"{english.join(agent.name for agent in agents)} left the conversation"
        )

    def add_bystanders(self, *bystanders: list[Agent]):
        for bystander in bystanders:
            if bystander in self.agents:
                self.agents.remove(bystander)
            if bystander not in self.bystanders:
                self._logger.info(
                    f"{bystander.name} is now a bystander to the conversation: {self.name}"
                )
                self.bystanders.append(bystander)

    def remove_bystanders(self, *bystanders: list[Agent]):
        for bystander in bystanders:
            if bystander in self.agents:
                self.agents.remove(bystander)
            if bystander in self.bystanders:
                self._logger.info(
                    f"{bystander.name} is no longer a bystander to the conversation: {self.name}"
                )
                self.bystanders.remove(bystander)

    def name(self):
        return str(self.path)

    def _save_delta(self, *messages: list[Message]):
        for message in messages:
            # write to file
            message.save(self.path / message.name)
            self._md_file.write(f"\n{message}\n")

    def save(self):
        with open(self.path / "conversation.pkl", "wb") as f:
            pickle.dump(self, f)

    @classmethod
    def load(self, path: Path):
        # load from pickle
        with open(path / "conversation.pkl", "rb") as f:
            return pickle.load(f)

    def to_string(self, include_timestamps: bool = False):
        return "\n".join(
            [
                (
                    f"{message.sender} at {message.timestamp.strftime(consts.TIME_FMT)}: {message.text}"
                    if include_timestamps
                    else f"{message.sender}: {message.text}"
                )
                for message in self.messages
            ]
        )

    def initialize(self):
        # create dir at the path
        self.path.mkdir(self.path, parents=True, exist_ok=False)
        # open file at the path
        self._md_file = open(self.path / "conversation.md", "a")

    def close(self):
        if self._final_message:
            self.input(self._final_message)
        self._md_file.close()
        self.save()

    def __enter__(self):
        self.initialize()
        if self._initial_message:
            self.input(self._initial_message)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def __repr__(self):
        return ipywidgets.VBox(
            [IPython.display.Markdown(f"# {self.name}")]
            + [msg.__repr__() for msg in self.messages]
        )

    def __len__(self):
        return len(self.messages)

    def __getitem__(self, index):
        return self.messages[index]

    def __setitem__(self, index, value):
        self.messages[index] = value

    def __delitem__(self, index):
        del self.messages[index]

    def __iter__(self):
        return iter(self.messages)

    def __reversed__(self):
        return reversed(self.messages)

    def __contains__(self, item):
        return item in self.messages

    def __del__(self):
        self.close()
