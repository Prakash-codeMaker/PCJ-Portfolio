# Wave 3 validation report

## Fresh issue checks
- Modal #4150 remains open. A targeted open-PR search returned no matching PR.
- OpenAI Agents SDK #6095 remains open. A targeted open-PR search returned no matching PR.
- Anthropic #2176 is excluded because open PR #2179 already addresses GIFBuilder state mutation.
- Exa #477 is excluded because open PR #478 addresses stringified domain lists.
- Anthropic #2246 is excluded because open PR #2247 addresses the v1 streamable HTTP example hardening.
- Modal #4142 is excluded because the issue author already published a full fork commit c7302531.

## Source inspection performed
- Modal: py/modal/_runtime/asgi.py and py/test/web_server_proxy_test.py.
- OpenAI Agents SDK: src/agents/models/chatcmpl_helpers.py, src/agents/models/openai_chatcompletions.py, src/agents/models/chatcmpl_stream_handler.py, src/agents/extensions/models/litellm_model.py, src/agents/extensions/models/any_llm_model.py, and the associated Chat Completions tests.

## Local validation
- python test_wave3_logic.py: Wave 3 isolated contract checks passed: 9 checks.
- git apply --stat parsed the Modal patch and the OpenAI Agents SDK patch.

## Not validated
- No complete Modal repository checkout, pytest suite, live browser WebSocket, or aiohttp 3.14.2+ integration test was run.
- No complete OpenAI Agents SDK checkout, pytest suite, Gemini endpoint, LiteLLM or AnyLLM integration test was run.
- git apply --stat proves patch syntax only; it does not prove the patch applies cleanly to a later upstream commit.
- No upstream PR has been opened or accepted.
