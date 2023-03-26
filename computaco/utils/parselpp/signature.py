import inspect
import sys
from typing import Callable


def signature(fn: Callable) -> str:
    """Prints the signature of a function as it would appear in the source code.

    >>> signature(print)
    ... print(*value, sep=' ', end='\n', file=sys.stdout, flush=False)
    """
    signature = inspect.signature(fn)
    parameters = []

    for name, param in signature.parameters.items():
        param_str = name
        if param.default != inspect.Parameter.empty:
            if param.default is sys.stdout:  # Special case for sys.stdout
                default = "sys.stdout"
            else:
                default = repr(param.default)
            param_str += f"={default}"
        parameters.append(param_str)

    return f"{fn.__name__}({', '.join(parameters)})"
