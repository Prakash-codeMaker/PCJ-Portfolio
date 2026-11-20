# Open-source contribution workbench — Wave 3

Prepared 20 November 2026. This wave contains two additional issue-grounded patch proposals across Modal and the OpenAI Agents SDK.

## Active contributions

| Project | Issue | Proposed work | Current state |
|---|---|---|---|
| Modal client | [#4150](https://github.com/modal-labs/modal-client/issues/4150) | Stop forwarding the browser's Sec-WebSocket-Extensions offer to an upstream aiohttp socket that does not negotiate compression; surface upstream WebSocket errors with a non-success close code | Source-grounded patch and focused tests prepared; isolated contract checks passed |
| OpenAI Agents SDK | [#6095](https://github.com/openai/openai-agents-python/issues/6095) | Recognize provider-qualified content_filter: REASON terminal signals, synthesize a refusal when the message is omitted, and preserve the provider's reason across non-streaming and streaming paths | Source-grounded patch and regression changes prepared; isolated contract checks passed |

## Duplicate work excluded

- Anthropic skills #2176 — matching PR [#2179](https://github.com/anthropics/skills/pull/2179) already exists.
- Exa MCP #477 — matching PR [#478](https://github.com/exa-labs/exa-mcp-server/pull/478) already exists.
- Anthropic skills #2246 — matching PR [#2247](https://github.com/anthropics/skills/pull/2247) already exists.
- Modal #4142 — issue author already published a full fix commit on a fork: [c7302531](https://github.com/Batuhan1999/modal-client/commit/c7302531).

## Validation

The dependency-free harness in test_wave3_logic.py passes 9 isolated contract checks:
- Standard content_filter keeps its existing fallback refusal message.
- Provider-qualified content_filter: OTHER and content_filter: SAFETY preserve the reason.
- Ordinary finish reasons, near-miss prefixes, and null values are not classified as content filters.
- WebSocket extension-offer filtering is case-insensitive and retains unrelated headers.
- WebSocket errors preserve 1002 / 1011 close codes and use 1011 when none is available.

Both patch files parse with git apply --stat.

## Important limits

These are not full upstream test runs. The Modal pytest suite and real aiohttp 3.14.2+ WebSocket integration were not run. The OpenAI Agents SDK unit tests and provider endpoint reproduction were not run. The local harness mirrors helper contracts, not the complete source modules.

No upstream branch, commit, issue comment, or PR has been created by this work. The connected GitHub integration has read access to upstream repositories but no upstream push permission; issue-comment writes are blocked. This portfolio PR is a reviewable record in the author's own repository only.
