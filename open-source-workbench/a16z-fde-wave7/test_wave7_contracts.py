"""Dependency-free contract checks for LangChain issues #41813 and #41951."""
from urllib.parse import urlsplit, urlunsplit


def append_provider_path(base_url: str, provider_path: str) -> str:
    parts = urlsplit(base_url)
    path = f"{parts.path.rstrip('/')}/{provider_path.lstrip('/')}"
    return urlunsplit(parts._replace(path=path))


assert append_provider_path("https://eu.gateway.example.com/", "openai/v1") == "https://eu.gateway.example.com/openai/v1"
assert append_provider_path("https://eu.gateway.example.com/proxy/", "openai/v1") == "https://eu.gateway.example.com/proxy/openai/v1"
assert append_provider_path("https://gateway.example.test/proxy?tenant=demo", "openai/v1") == "https://gateway.example.test/proxy/openai/v1?tenant=demo"
assert append_provider_path("https://gateway.example.test/proxy/?tenant=demo&region=eu", "/anthropic") == "https://gateway.example.test/proxy/anthropic?tenant=demo&region=eu"
assert append_provider_path("https://gateway.example.test/proxy?tenant=demo#section", "openai/v1") == "https://gateway.example.test/proxy/openai/v1?tenant=demo#section"


def choices_error(choices):
    if choices is None:
        raise TypeError("Received response with null value for 'choices'.")
    if not choices:
        raise TypeError("Received response with empty list for 'choices'.")
    return list(choices)


try:
    choices_error([])
except TypeError as exc:
    assert "empty list for 'choices'" in str(exc)
else:
    raise AssertionError("expected empty choices to be rejected")

try:
    choices_error(None)
except TypeError as exc:
    assert "null value for 'choices'" in str(exc)
else:
    raise AssertionError("expected null choices to be rejected")

choice = {"index": 0, "message": {"role": "assistant", "content": "ok"}}
assert choices_error([choice]) == [choice]

print("Wave 7 contract checks passed: 8 checks")
