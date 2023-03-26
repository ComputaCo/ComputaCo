from typing import Literal, Optional
from computaco.abstractions import abilities
from computaco.environments.conversation import (
    AudioMessage,
    Conversation,
    ImageMessage,
    Message,
    TextMessage,
    VideoMessage,
)
from computaco.abstractions.types import Audio, Image, Text, Video

## I'm just writing here beause I don't know where else, but the agent should have an agenda in its mind. That way, it won't continually say 'yes' to should we continue the conversation (because it'll want to do other tasks instead)


class Agent(abilities.HandlesAnyInputOutput):
    name: str
    pronoun: str
    possessive_pronoun: str

    system_conversation: Optional[Conversation] = None

    def input(self, message: str | Message | None, *args, remember=True, **kwargs):
        # not using elif since a message can be of multiple types
        if message is None:
            return
        if isinstance(message, str):
            message = TextMessage("System", text=message)
        if isinstance(message, TextMessage):
            self.input_text(
                message.text, *args, sender=message.sender, remember=remember, **kwargs
            )
        if isinstance(message, ImageMessage):
            self.input_image(
                message.image, *args, sender=message.sender, remember=remember, **kwargs
            )
        if isinstance(message, AudioMessage):
            self.input_audio(
                message.audio, *args, sender=message.sender, remember=remember, **kwargs
            )
        if isinstance(message, VideoMessage):
            self.input_video(
                message.video, *args, sender=message.sender, remember=remember, **kwargs
            )

    def output(self, *args, remember=True, **kwargs) -> Message | None:
        output_type = self.output_type(*args, remember=remember, **kwargs)
        if output_type is None:
            return None
        elif output_type == Text:
            return TextMessage(self.name, text=self.output_text(*args, **kwargs))
        elif output_type == Image:
            return ImageMessage(self.name, image=self.output_image(*args, **kwargs))
        elif output_type == Audio:
            return AudioMessage(self.name, audio=self.output_audio(*args, **kwargs))
        elif output_type == Video:
            return VideoMessage(self.name, video=self.output_video(*args, **kwargs))
        elif output_type == "Multiple":
            raise NotImplementedError("Multiple output types not implemented yet")
        else:
            raise ValueError(f"Unknown output type: {output_type}")

    def output_type(
        self, *args, remember=True, **kwargs
    ) -> Literal["Text", "Image", "Audio", "Video", "Multiple", "None"]:
        raise NotImplementedError()

    # Agents CAN support multitasking. Processes canNOT.
    def fork(self):
        pass

    def merge(self):
        pass

    def __repr__(self):
        return self.name
