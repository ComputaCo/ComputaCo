from typing import Protocol, runtime_checkable


@runtime_checkable
class Process(Protocol):
    async def __call__(*args, **kwargs) -> None:
        ...
