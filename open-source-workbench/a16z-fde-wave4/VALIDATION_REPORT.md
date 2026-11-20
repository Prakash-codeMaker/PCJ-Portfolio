# Wave 4 validation report

## Active issue checked

OpenAI Agents SDK issue #6093 is open. A targeted search found no matching open PR at the time of this check.

The current merge helper and the existing behavior test were fetched directly:
- src/agents/mcp/util.py blob d51a773342c93239a1b79f1056ca889f37599d57
- src/agents/mcp/server.py blob 57fa9e1d65c7db0d01e0c9312e00f400056bff65
- tests/mcp/test_mcp_util.py blob b61985656d14225074536b1cf86e64fa2e08ab10

Existing test currently asserts that static server metadata overrides the resolver value for a colliding locale key. This is why the proposed change keeps current behavior as the default and introduces an opt-in resolver-precedence setting.

## Local validation

contract_tests.py — six standalone merge-contract checks passed:
- compatibility default;
- opt-in resolver wins;
- unique keys retained;
- inputs unchanged;
- nested copy isolation;
- invalid configuration rejected.

## Triage evidence

- OpenAI #6091 has a tested fix on a contributor's fork and additional independent verification in the issue comments.
- OpenAI #6072 has a tested narrow patch plus several end-to-end reproduction/verification comments; repeated sticky-decision semantics remain a design choice.
- Modal #4154: grpclib 0.4.7 and 0.4.9 default SSL contexts both set ALPN to h2.
- Anthropic #2202/#2205/#2206/#2207/#2184/#2185 have matching open PRs #2208/#2210/#2209/#2216/#2188/#2187.

## Not validated

- No changes were applied to a full upstream Agents SDK checkout.
- No MCP transport integration tests were run.
- The opt-in API shape is a proposal requiring maintainer agreement.
- No upstream branch, issue comment, or PR was created.
