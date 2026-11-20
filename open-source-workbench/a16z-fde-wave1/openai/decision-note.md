# OpenAI Agents SDK — MCP approval policy for tools that appear later

Upstream issue: https://github.com/openai/openai-agents-python/issues/6094

## What the discussion establishes

An existing commenter reproduced the issue against Agents SDK 0.25.0 and identified the actual path as `MCPServer._get_needs_approval_for_tool` in `agents/mcp/server.py` (the earlier `get_all_tools` pointer was imprecise).

The dictionary branch behaves like:

```python
if isinstance(policy, dict):
    return bool(policy.get(tool.name, False))
```

An unlisted tool therefore receives `False` (no approval). A callable policy with no agent available has a fail-closed fallback. The issue now has two substantive comments, so repeating the same one-line observation would add little.

## A safe immediate workaround

Until the SDK offers an explicit default, the issue discussion proposes using a callable as a deny-unlisted policy:

```python
async def needs_approval(ctx, agent, tool):
    return tool.name not in {"read_only_tool"}
```

This should be validated against the exact installed SDK version and the actual policy callback signature before production use.

## The next non-duplicate contribution

The deeper unresolved boundary is tool-list mutation. A policy might be evaluated when the server first connects, then the server can advertise a new tool later. A fix that only changes the dictionary default may still miss this path if classification is cached.

Proposed regression matrix:
1. Start with tool list `[read_record]`; explicit policy marks it safe.
2. Server later advertises `[read_record, export_all]`; the new tool must not inherit the old tool's safe classification.
3. Remove and re-add a tool; classification must be deterministic and policy-driven.
4. A callable policy is re-evaluated on the changed list.
5. Tool-list delta handling emits approval-required behavior until the new tool is explicitly classified, unless an explicitly unsafe compatibility mode is selected.

No implementation change is proposed here because the public discussion needs to settle the intended compatibility contract first.
