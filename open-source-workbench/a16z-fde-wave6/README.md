# Open-source contribution workbench — Wave 6

Prepared 20 November 2026. This wave expands beyond the Modal and OpenAI SDK targets into LangGraph.

## Active target

**LangGraph #9115 — invalid RetryPolicy.retry_on sequences bypass the documented TypeError**

- Issue: https://github.com/langchain-ai/langgraph/issues/9115
- Current implementation: libs/langgraph/langgraph/pregel/_retry.py, blob 58e2fafe2ed065acf68562c68db9c462d8cf3c99.
- Existing tests: libs/langgraph/tests/test_retry.py, blob e251445147d73647b2c77818ec247cab198b394c.
- Public RetryPolicy annotation: libs/langgraph/langgraph/types.py, blob 4385c0e00c0af9dc3e73c981c8899ca93ab40c15.
- Issue #9115 is open; the targeted open-PR search found no matching PR.

### Problem

The implementation checks Sequence before checking for a class. Since str, bytes and bytearray are Sequences, a malformed value such as "ValueError" is converted to a tuple of characters and passed to isinstance(). A list containing non-exception members has the same class of problem; a mixed tuple can behave inconsistently depending on whether an earlier member matches.

The declared RetryPolicy type accepts an Exception class, a Sequence of Exception classes, or a callable. It does not declare string class names.

### Proposed fix

- Recognize an Exception subclass before the Sequence branch.
- Exclude str, bytes and bytearray from the Sequence branch.
- Validate every sequence element is an Exception class before calling isinstance().
- Preserve callable policies and valid empty sequences.
- Raise the existing documented TypeError for invalid values.

The patch includes regression cases for string, bytes, bytearray, string-only sequences, and mixed sequences where a valid exception class comes before or after an invalid string.

## Validation

- Dependency-free contract harness: 12 checks passed.
- git apply --stat parsed the two-file patch.
- Existing valid class, tuple, empty sequence, and callable behavior is covered in the local harness.

## Limits

The patch is not applied to a complete LangGraph checkout. The upstream pytest suite, typing checks, and full graph invocation reproduction were not run. This is a draft portfolio PR only: no LangGraph upstream branch, issue comment or PR is claimed.
