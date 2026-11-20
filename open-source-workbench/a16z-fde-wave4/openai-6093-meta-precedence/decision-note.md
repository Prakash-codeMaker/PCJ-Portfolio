# OpenAI Agents SDK #6093 — MCP request metadata precedence

Issue: https://github.com/openai/openai-agents-python/issues/6093

## Source-grounded current behavior

In src/agents/mcp/util.py, MCPUtil._merge_mcp_meta(resolved_meta, explicit_meta) performs a deep-copy merge in this order:

1. Copy resolved_meta, produced at runtime by the application's tool_meta_resolver.
2. Copy explicit_meta, captured from the remote tool's static MCP _meta at discovery time.

Therefore a collision is resolved in favor of explicit_meta. In this path, that value originates from the MCP server's list_tools response and is not signed or authenticated by the application.

The existing test test_to_function_tool_merges_static_mcp_meta_with_resolver explicitly expects {"locale": "en"} from the server to override {"locale": "ja"} from the resolver. So a global default reversal would break an existing tested contract.

The public MCPServer constructor documents tool_meta_resolver as a callable producing request metadata but does not document the precedence relationship against static tool metadata.

## Proposed backwards-compatible extension

Add a server configuration field:

    tool_meta_resolver_precedence: Literal["server", "resolver"] = "server"

- server: preserves today's merge ordering exactly.
- resolver: resolver values are copied last and win collisions.
- Both modes preserve non-colliding keys and deep-copy both inputs.

The default deliberately remains "server" because that is what the existing tests currently guarantee. Applications with security-sensitive resolver values can explicitly opt into "resolver".

This should be threaded through the base MCPServer constructor and concrete stdio / streamable-HTTP constructors, then passed through the invoke_mcp_tool call path into the merge helper.

## Security / semantics boundary

This change is a metadata-precedence control, not an authorization engine. It does not make MCP _meta trusted and does not guarantee that a remote server will honor a field. It only determines which local value is included in the outgoing request when both sources provide the same key.

Separately, custom_data_extractor currently receives result.meta from the MCP server in a read-only mapping. That is a different inbound trust boundary: downstream extractors should treat it as server-controlled data and must not use it as trusted policy unless they verify it.

## Tests needed in the upstream suite

- Retain the existing default test where server static locale wins.
- Add a resolver-precedence test where local tenant_id and auth_context override server collisions.
- Verify unique keys from both sides remain.
- Verify nested structures are not mutated or aliased across calls.
- Verify invalid option values fail during server construction.
- Test each concrete MCP transport constructor to ensure it forwards the option.

No upstream code change is asserted by this note.
