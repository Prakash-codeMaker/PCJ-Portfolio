"""Small local contract checks; not a substitute for the upstream test suites."""

def content_filter_refusal_message(finish_reason):
    if not isinstance(finish_reason, str):
        return None
    if finish_reason != "content_filter" and not finish_reason.startswith("content_filter:"):
        return None
    reason = finish_reason.partition(":")[2].strip()
    if reason:
        return f"Response withheld by the provider's content filter ({reason})."
    return "Response withheld by the provider's content filter."

assert content_filter_refusal_message("content_filter") == "Response withheld by the provider's content filter."
assert content_filter_refusal_message("content_filter: OTHER") == "Response withheld by the provider's content filter (OTHER)."
assert content_filter_refusal_message("content_filter: SAFETY") == "Response withheld by the provider's content filter (SAFETY)."
assert content_filter_refusal_message("stop") is None
assert content_filter_refusal_message("content_filtering") is None
assert content_filter_refusal_message(None) is None

def websocket_proxy_headers(headers):
    return [(name.decode(), value.decode()) for name, value in headers if name.lower() != b"sec-websocket-extensions"]

assert websocket_proxy_headers([(b"host", b"localhost"), (b"Sec-WebSocket-Extensions", b"permessage-deflate"), (b"cookie", b"a=b")]) == [("host", "localhost"), ("cookie", "a=b")]

def websocket_error_close_message(close_code):
    return {"type": "websocket.close", "code": close_code or 1011, "reason": "Upstream WebSocket error"}

assert websocket_error_close_message(1002)["code"] == 1002
assert websocket_error_close_message(None)["code"] == 1011
print("Wave 3 isolated contract checks passed: 9 checks")
