# Pydantic AI provider-profile fixes — Wave 8

Prepared 20 November 2026. This wave adds two narrow provider compatibility fixes with focused regression coverage.

## 1. Vercel AI Gateway — issue #14034

Issue: https://github.com/pydantic/pydantic-ai/issues/14034

Vercel AI Gateway currently exposes Grok under the `spacexai/` provider slug. The official Vercel model page uses `spacexai/grok-4.3` in its model ID and identifies SpaceXAI as the provider. Pydantic AI's `VercelProvider.model_profile` map only routes `xai` to `grok_model_profile`, so `spacexai/grok-4.3` silently misses the Grok capabilities profile.

Proposed change: add `spacexai: grok_model_profile` as an alias, retaining `xai` for compatibility. Regression coverage checks profile routing and Grok 4.3 reasoning/native-tool fields.

Official model evidence: https://vercel.com/ai-gateway/models/spacexai/grok-4.3

## 2. Mistral — issue #14033

Issue: https://github.com/pydantic/pydantic-ai/issues/14033

The public Mistral API reportedly resolves `mistral-large-latest` to Mistral Large 4, but Pydantic AI's `_LARGE_4_MODELS` set only includes `mistral-large-4` and `mistral-large-4-0`. Therefore the alias misses `supports_thinking`, `thinking_always_enabled`, and the allowed `low` / `medium` / `high` reasoning effort profile.

Proposed change: add `mistral-large-latest` to the native-provider model set and run the existing effort mapping test matrix against that alias too. The upstream issue author supplied the public `/v1/models` alias/capability evidence dated 19 November 2026; this bundle does not independently call the Mistral API.

Official Large 4 reasoning documentation: https://docs.mistral.ai/inference/conversations/reasoning

## Validation

- Dependency-free provider-profile contract harness: 18 checks passed.
- Both diffs parse with `git apply --stat`.
- Changes are narrowly scoped to provider profile routing and the existing provider tests.

## Limits

- The Pydantic AI upstream test suite, formatting, type checks, and provider API integrations were not run.
- The Mistral latest-alias behavior is grounded in the issue reporter's API observation; it was not independently re-queried in this session.
- `git apply --stat` validates diff syntax only, not clean application to the latest upstream checkout.
- No upstream branch, commit, issue comment, or pull request was created. The related PR is a draft portfolio PR in `Prakash-codeMaker/PCJ-Portfolio` only.
