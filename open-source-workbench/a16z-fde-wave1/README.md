# Open-source engineering workbench — Wave 1

Prepared 20 November 2026 by Prakash Chand Jain.

This is a public engineering workbench, not a claim of upstream acceptance. It records candidate issue analysis, patch design, focused tests, and the next actions that remain.

## Active contribution tracks

| Project | Upstream issue | Work in this branch | Current state |
|---|---|---|---|
| Modal Python client | [#4155](https://github.com/modal-labs/modal-client/issues/4155) | Retry delay must respect the configured `Retries(max_delay=...)` ceiling; patch and tests included | Open issue; no matching PR appeared in the current open-PR search |
| OpenAI Agents SDK | [#6094](https://github.com/openai/openai-agents-python/issues/6094) | Review note covering the dictionary-policy fail-open default and tool-list-change boundary | Design/review track; issue already has two detailed comments, so this branch avoids posting a duplicate |
| Exa MCP server | [#458](https://github.com/exa-labs/exa-mcp-server/issues/458) | Backwards-compatible provenance and untrusted-content contract | Design track; maintainer agreement needed before changing MCP result shape |

## Superseded candidates — deliberately not presented as new contributions

- Palantir policy-bot #1397: the same default-conclusion-description fix is already represented by open PRs #1398 and #1457. The prepared patch is therefore not an active contribution.
- Anthropic skills #2239: the same title-placeholder detection fix already has open PR #2240. The prepared patch is therefore not an active contribution.

Avoiding duplicate work is part of the contribution process. The superseded patch files remain in the downloadable local archive for audit, but are intentionally excluded from this active branch.

## Validation performed

- Modal isolated retry-cap regression matrix: 4 checks passed.
- OpenAI minimal policy-default reproduction: passed. The upstream issue's comments additionally contain an independent reproduction against Agents SDK 0.25.0 and correct the relevant entry point to `MCPServer._get_needs_approval_for_tool`.
- Exa structured provenance fixture: passed as a schema/contract check only.
- Anthropic's superseded local placeholder tests: 4 passed, but the issue now has an existing PR.
- Python compileall passed on the original bundle.

The Modal upstream test addition has not been run against a complete Modal checkout. Palantir Go tests were not run. Exa's fixture does not test the server implementation. OpenAI's mini reproduction is not a full SDK test.

## What has not happened

No upstream PR has been submitted, accepted, or merged by this workbench. The connected GitHub integration has read access but no push permission on the five target repositories; its issue-comment write was rejected by GitHub with a 403. This branch is in the author's own portfolio repository and does not alter any upstream project.

## Next useful work

1. For Modal, validate the patch against a full checkout and submit via a maintainer-approved fork/PR route.
2. For OpenAI, add tests for approval reclassification when an MCP server's advertised tool list changes, building on the existing discussion rather than repeating it.
3. For Exa, ask maintainers which MCP-compatible location should carry provenance before implementing a potentially client-breaking contract.
4. Re-scan open PRs before starting any replacement issue; do not assume the issue list has stayed unchanged.
