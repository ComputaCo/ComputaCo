from computaco.abstractions.types import Image


class Markdown:
    @property
    def markdown(self) -> str:
        raise NotImplementedError()


class Image:
    @property
    def image(self) -> Image:
        raise NotImplementedError()
