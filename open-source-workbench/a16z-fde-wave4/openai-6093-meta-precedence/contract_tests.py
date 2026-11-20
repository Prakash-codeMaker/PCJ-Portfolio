"""Standalone API contract matrix for the proposed MCP metadata precedence option.

This is not an upstream SDK test. It pins the intended merge semantics only.
"""
from copy import deepcopy


def merge_mcp_meta(resolved_meta, explicit_meta, precedence="server"):
    if precedence not in {"server", "resolver"}:
        raise ValueError("precedence must be 'server' or 'resolver'")
    if resolved_meta is None and explicit_meta is None:
        return None
    merged = {}
    if resolved_meta is not None:
        merged.update(deepcopy(resolved_meta))
    if explicit_meta is not None:
        merged.update(deepcopy(explicit_meta))
    if precedence == "resolver":
        # Re-apply resolver values last; this contract keeps unique server keys.
        merged.update(deepcopy(resolved_meta or {}))
    return merged


# 1. The default preserves the currently tested server-wins behavior.
assert merge_mcp_meta(
    {"request_id": "r1", "locale": "ja"},
    {"locale": "en", "extra": "value"},
) == {"request_id": "r1", "locale": "en", "extra": "value"}

# 2. Applications can opt into resolver precedence for colliding keys.
assert merge_mcp_meta(
    {"tenant_id": "tenant-A", "locale": "ja"},
    {"tenant_id": "tenant-B", "locale": "en"},
    "resolver",
) == {"tenant_id": "tenant-A", "locale": "ja"}

# 3. Non-colliding keys from both sources remain in the result.
assert merge_mcp_meta(
    {"request_id": "r1"},
    {"server_trace": "trace-2"},
    "resolver",
) == {"request_id": "r1", "server_trace": "trace-2"}

# 4. Input dictionaries are not mutated.
resolved = {"locale": "ja"}
explicit = {"locale": "en"}
merge_mcp_meta(resolved, explicit, "resolver")
assert resolved == {"locale": "ja"}
assert explicit == {"locale": "en"}

# 5. Nested values are deeply copied, not aliased.
nested_resolved = {"context": {"tenant": ["A"]}}
nested_explicit = {"context": {"tenant": ["B"]}}
merged = merge_mcp_meta(nested_resolved, nested_explicit, "resolver")
merged["context"]["tenant"].append("C")
assert nested_resolved == {"context": {"tenant": ["A"]}}
assert nested_explicit == {"context": {"tenant": ["B"]}}

# 6. Unsupported configuration values are rejected.
try:
    merge_mcp_meta({}, {}, "last-writer-wins")
except ValueError:
    pass
else:
    raise AssertionError("invalid precedence should be rejected")

print("Wave 4 metadata-precedence contract checks passed: 6 checks")
