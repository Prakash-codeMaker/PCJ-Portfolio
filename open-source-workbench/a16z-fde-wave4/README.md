# Open-source engineering workbench — Wave 4

Prepared 20 November 2026. This wave investigates MCP metadata precedence in the OpenAI Agents SDK and adds a backwards-compatible API design proposal with standalone contract tests.

## Active proposal

**OpenAI Agents SDK #6093 — server _meta overrides application resolver metadata**

- Issue: https://github.com/openai/openai-agents-python/issues/6093
- Source inspected: src/agents/mcp/util.py (blob d51a773342c93239a1b79f1056ca889f37599d57) and src/agents/mcp/server.py (blob 57fa9e1d65c7db0d01e0c9312e00f400056bff65).
- Existing behavior: _merge_mcp_meta(resolved_meta, explicit_meta) copies resolver values first and server-declared static _meta second. On key collision, static server values win.
- Compatibility evidence: tests/mcp/test_mcp_util.py (blob b61985656d14225074536b1cf86e64fa2e08ab10) explicitly expects the server's static locale value to override the resolver's value. A default reversal would break an existing contract.

### Proposed API

Add an explicit option such as:

    MCPServerStdio(..., tool_meta_resolver_precedence="resolver")

Values:
- "server" — current behavior and default, preserving compatibility.
- "resolver" — application resolver values win only when keys collide; non-overlapping keys are retained from both sources.

This makes the trust decision visible at the server configuration boundary instead of silently changing current behavior. Applications that inject tenant IDs, authorization context, or audit context should choose "resolver" when those fields must not be overwritten by remote tool declarations.

The proposal does not claim that MCP _meta itself is an authorization mechanism. It only prevents accidental or untrusted key overwrite in the metadata passed to call_tool.

### Contract tests included

The standalone test matrix checks:
1. Default/server precedence maintains current merge output.
2. Resolver precedence keeps app-owned colliding values.
3. Non-colliding values from both sources are preserved.
4. Neither input mapping is mutated.
5. Nested values are deep-copied.
6. Invalid precedence values are rejected by the proposed validation contract.

## Triage exclusions (avoid duplicate or weak work)

- OpenAI #6091: a contributor already published a tested fork fix for settled sibling tool calls on cancellation; two other commenters independently reproduced and tested it. Further work should address only the documented guardrail boundary or another distinct gap.
- OpenAI #6072: multiple contributors have already supplied local patches and end-to-end test evidence in the issue thread. The remaining open question is the semantics of repeated sticky decisions; reimplementing the narrow patch would duplicate existing work.
- Modal #4154: the pinned grpclib 0.4.7/0.4.9 default SSL context already calls set_alpn_protocols(['h2']); no generic missing-ALPN patch is justified from the current source.
- Anthropic #2202, #2205, #2206, #2207, #2184 and #2185 each already have matching open PRs (#2208, #2210, #2209, #2216, #2188 and #2187 respectively).

## Validation and limits

- The standalone merge-contract matrix passes six checks.
- The current upstream behavior and compatibility expectation were read directly from the implementation and existing test.
- The API proposal has not been integrated into the full SDK source tree.
- No full OpenAI Agents SDK test suite, MCP client/server integration test, or maintainer compatibility review was run.
- This is a draft portfolio workbench PR only; no upstream repository was modified and no upstream PR is claimed.
