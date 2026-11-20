# Exa MCP server — preserve provenance and mark retrieved page text as untrusted

Upstream issue: https://github.com/exa-labs/exa-mcp-server/issues/458

## Observed integration problem

Search and fetch responses currently combine server/provider metadata and retrieved web-page text in a single text block. Hosts then have difficulty distinguishing trusted metadata (such as source title and URL) from untrusted instructions embedded in page content.

## Proposed non-breaking contract

Keep the existing text block byte-for-byte compatible for clients that consume it. In parallel, return a structured per-result envelope that keeps metadata separate from retrieved content and labels the latter with a trust marker:

```json
{
  "results": [
    {
      "title": "Example page",
      "url": "https://example.org/page",
      "author": "Example author",
      "publishedDate": "2026-11-20",
      "content": "Retrieved page text...",
      "contentTrust": "untrusted_external_content"
    }
  ]
}
```

Do not prepend a trust warning into the content text itself; the trust boundary should be represented as metadata outside the content string.

## Test plan

- Adversarial page text such as "ignore previous instructions" remains data and carries the untrusted marker.
- Missing text but available highlights retains title and URL.
- Multiple results preserve order and one provenance envelope per result.
- Missing or malformed URLs follow the existing sanitizer policy; never invent a source URL.
- Search and fetch use the same provenance model.
- Legacy text rendering stays unchanged when the structured output is disabled.

## Maintainer decision needed

Which supported MCP clients are expected to consume structured results today, and should provenance be represented using structured content, annotations, or a resource/link payload? This decision should precede implementation because clients may privilege structured fields over text blocks.

This note is a design proposal, not evidence that the server has been changed or that a prompt-injection defence has been fully validated.
