from collections import deque


def merge_types(types, name=None):
    name = name or "_".join(t.__name__ for t in types)
    return type(
        name,
        types,
        {k: v for t in types for k, v in t.__dict__},
    )


def flatten_type(type):
    """Returns a glom-style list of constituient types, starting from `type`

    >>> flatten_type(str)
    ... 'str': str
    >>> class INPUT:
            b: int
            c: bool
    >>> flatten_type(A):
    ... ['INPUT.b': int, 'INPUT.c': bool]
    """
    result = []
    queue = deque([(type, "")])

    while queue:
        current_type, current_path = queue.popleft()

        if hasattr(current_type, "__dict__"):
            for attr, attr_type in current_type.__dict__.items():
                if not callable(attr_type) and not attr.startswith("__"):
                    new_path = f"{current_path}.{attr}" if current_path else attr
                    queue.append((attr_type, new_path))
        else:
            result.append((current_path, current_type))

    return result
