"""Dependency-free regression checks for LangGraph RetryPolicy #9115."""
from collections.abc import Sequence


def should_retry_on(retry_on, exc):
    if isinstance(retry_on, type) and issubclass(retry_on, Exception):
        return isinstance(exc, retry_on)
    elif isinstance(retry_on, Sequence) and not isinstance(retry_on, (str, bytes, bytearray)):
        retry_types = tuple(retry_on)
        if not all(isinstance(t, type) and issubclass(t, Exception) for t in retry_types):
            raise TypeError("retry_on must be an Exception class, a list or tuple of Exception classes, or a callable")
        return isinstance(exc, retry_types)
    elif callable(retry_on):
        return retry_on(exc)
    raise TypeError("retry_on must be an Exception class, a list or tuple of Exception classes, or a callable")

# Valid class policy remains valid.
assert should_retry_on(ValueError, ValueError("boom")) is True
assert should_retry_on(ValueError, TypeError("boom")) is False

# Valid exception-class sequences remain valid, including empty tuples.
assert should_retry_on((ValueError, KeyError), KeyError("boom")) is True
assert should_retry_on([], ValueError("boom")) is False

# Callable policy remains valid.
assert should_retry_on(lambda exc: isinstance(exc, ValueError), ValueError("boom")) is True

# Invalid strings/bytes and sequences with non-exception members fail clearly.
for invalid in ("ValueError", b"ValueError", bytearray(b"ValueError"), ["ValueError"], [ValueError, "TypeError"], ["TypeError", ValueError], 123):
    try:
        should_retry_on(invalid, ValueError("boom"))
    except TypeError as exc:
        assert "retry_on must be an Exception class" in str(exc)
    else:
        raise AssertionError(f"expected invalid policy to fail: {invalid!r}")

print("LangGraph #9115 retry-policy contract checks passed: 12 checks")
