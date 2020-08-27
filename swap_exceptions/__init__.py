from typing import Any, Callable, ContextManager, Dict, Iterable, Tuple, Type, Union

import six

if six.PY2:
    from contextlib2 import contextmanager
else:
    from contextlib import contextmanager

__all__ = ["swap_exceptions"]

# Exception type or iterable of exception types
ExceptionSourceType = Union[Type[Exception], Tuple[Type[Exception]]]
ExceptionTargetType = Union[Exception, Callable[[Exception], Exception]]
ExceptionMappingType = Dict[ExceptionSourceType, ExceptionTargetType]

SwapExceptionsReturnType = Union[ContextManager, Callable[[Callable], Callable]]


@contextmanager
def swap_exceptions(exception_mapping, raise_from=True):
    # type: (ExceptionMappingType, bool) -> SwapExceptionsReturnType
    """
    Swap raised exception with other exceptions.

    :param exception_mapping: Mapping between exception types (or tuples of them)
     and exceptions to swap to (or functions creating them)
    :param raise_from: Should use raise from to raise exceptions
    """
    exception_sources = tuple(_flatten_recursively(exception_mapping.keys()))

    try:
        yield
    except exception_sources as exc:
        for exc_source, exc_target in exception_mapping.items():
            if isinstance(exc, exc_source):
                # Get new exception to swap to
                if isinstance(exc_target, Exception):
                    new_exc = exc_target
                else:  # exc_target is a callable
                    new_exc = exc_target(exc)

                # Raise new exception
                if raise_from:
                    six.raise_from(new_exc, exc)
                else:
                    raise new_exc


def _flatten_recursively(iterable):
    # type: (Iterable[Any]) -> Iterable[Any]
    """
    itertools.chain but make it recursive
    """
    for elem in iterable:
        try:
            # imagine these lines say 'yield from elem'
            for e in elem:
                yield e

        except TypeError:  # elem is not iterable
            yield elem
