# Open-source contribution workbench — Wave 7

Prepared 20 November 2026. This wave adds two LangChain issues with small, source-grounded fixes and focused tests.

## Active targets

| Project | Issue | Proposed change | Validation |
|---|---|---|---|
| LangChain OpenAI | https://github.com/langchain-ai/langchain/issues/41813 | Raise a descriptive TypeError when a Chat Completions response contains choices: [], rather than returning an empty ChatResult that later causes IndexError in invoke()/ainvoke() | Patch parses; contract harness covers empty, null, and valid choices |
| LangChain Core | https://github.com/langchain-ai/langchain/issues/41951 | Append provider paths to the URL path component, preserving existing query parameters and fragments for environment and context-based gateway URLs | Patch parses; contract harness covers slash normalization, queries, and fragments |

## Source inspected

- libs/partners/openai/langchain_openai/chat_models/base.py — blob bbad6fd0af891a4420da8fdfa290c8096141fe57.
- libs/partners/openai/tests/unit_tests/chat_models/test_base.py — blob 520960a0d8ff5bb5bcb8fff07baa9520b4aeb7b3.
- libs/core/langchain_core/utils/_gateway.py — blob c927f794bda6a699a32d2e65294a4c8f865325e5.
- libs/core/tests/unit_tests/utils/test_gateway.py — blob 30e023c6686f2ae1f4134a6784b64558b46e6a17.

## Validation

- test_wave7_contracts.py: 8 dependency-free contract checks passed.
- Both patch files parse with git apply --stat.
- The tests proposed in the diffs are written against existing upstream test modules.

## Limits

The patch files were not applied to complete upstream checkouts. The LangChain test suites, type checks, lint, mocked HTTP reproduction for #41813, and gateway context integration tests for #41951 were not run. git apply --stat validates diff syntax only; it does not establish clean application to the latest upstream revision.

No upstream repository was changed, and no upstream PR or issue comment is claimed. The associated GitHub PR is a draft portfolio workbench PR in the author's own repository only.
