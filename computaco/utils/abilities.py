from computaco.environments.conversation import (
    AudioMessage,
    ImageMessage,
    Message,
    TextMessage,
    VideoMessage,
)
from computaco.abstractions.types import Audio, Image, Text, Video


class HandlesTextInput:
    def input_text(self, text: Text, *args, sender="Info", remember=True, **kwargs):
        raise NotImplementedError()


class HandlesTextOutput:
    def output_text(self, *args, remember=True, **kwargs) -> Text | None:
        raise NotImplementedError()


class HandlesImageInput:
    def input_image(self, video: Image, *args, sender="Info", remember=True, **kwargs):
        raise NotImplementedError()


class HandlesImageOutput:
    def output_image(self, *args, remember=True, **kwargs) -> Image | None:
        raise NotImplementedError()


class HandlesAudioInput:
    def input_audio(self, video: Audio, *args, sender="Info", remember=True, **kwargs):
        raise NotImplementedError()


class HandlesAudioOutput:
    def output_audio(self, *args, remember=True, **kwargs) -> Audio | None:
        raise NotImplementedError()


class HandlesVideoInput:
    def input_video(self, video: Video, *args, sender="Info", remember=True, **kwargs):
        raise NotImplementedError()


class HandlesVideoOutput:
    def output_video(self, *args, remember=True, **kwargs) -> Video | None:
        raise NotImplementedError()


class HandlesAnyInput(
    HandlesTextInput, HandlesImageInput, HandlesAudioInput, HandlesVideoInput
):
    def input(self, message: str | Message | None, *args, remember=True, **kwargs):
        raise NotImplementedError()

    def __call__(self, message: str | Message | None, *args, remember=True, **kwargs):
        return self.input(message, *args, remember=remember, **kwargs)


class HandlesAnyOutput(
    HandlesTextOutput, HandlesImageOutput, HandlesAudioOutput, HandlesVideoOutput
):
    def output(self, *args, remember=True, **kwargs) -> Message | None:
        raise NotImplementedError()


class HandlesTextInputOutput(HandlesTextInput, HandlesTextOutput):
    def input_output_text(
        self, message: Text | None, *args, remember=True, **kwargs
    ) -> Text | None:
        if message is None:
            return None
        self.input(message, *args, remember=remember, **kwargs)
        return self.output(*args, remember=remember, **kwargs)


class HandlesImageInputOutput(HandlesImageInput, HandlesImageOutput):
    def input_output_image(
        self, message: Image | None, *args, remember=True, **kwargs
    ) -> Image | None:
        if message is None:
            return None
        self.input(message, *args, remember=remember, **kwargs)
        return self.output(*args, remember=remember, **kwargs)


class HandlesAudioInputOutput(HandlesAudioInput, HandlesAudioOutput):
    def input_output_audio(
        self, message: Audio | None, *args, remember=True, **kwargs
    ) -> Audio | None:
        if message is None:
            return None
        self.input(message, *args, remember=remember, **kwargs)
        return self.output(*args, remember=remember, **kwargs)


class HandlesVideoInputOutput(HandlesVideoInput, HandlesVideoOutput):
    def input_output_video(
        self, message: Video | None, *args, remember=True, **kwargs
    ) -> Video | None:
        if message is None:
            return None
        self.input(message, *args, remember=remember, **kwargs)
        return self.output(*args, remember=remember, **kwargs)


class HandlesAnyInputOutput(HandlesAnyInput, HandlesAnyOutput):
    def input_output(
        self, message: str | Message | None, *args, remember=True, **kwargs
    ) -> Message | None:
        if message is None:
            return None
        self.input(message, *args, remember=remember, **kwargs)
        return self.output(*args, remember=remember, **kwargs)

    def __call__(
        self, message: str | Message | None, *args, remember=True, **kwargs
    ) -> Message | None:
        return self.input_output(message, *args, remember=remember, **kwargs)
