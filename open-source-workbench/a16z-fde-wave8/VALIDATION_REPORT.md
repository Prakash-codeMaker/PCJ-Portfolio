# Wave 8 validation report

## Issue and duplicate checks
- Pydantic AI #14034: open issue, no matching open PR found in targeted GitHub search.
- Pydantic AI #14033: open issue, no matching open PR found in targeted GitHub search.
- The source code was fetched directly from the current repository default branch before preparing the patch.

## Source inspection
- `pydantic_ai_slim/pydantic_ai/providers/vercel.py` — blob `6e73af03df753960f53a5a0bdaa735e9f6cda0e7`.
- `tests/providers/test_vercel.py` — blob `14c6b1a1cc7fcee1af6c30b708c667b7193b7881`.
- `pydantic_ai_slim/pydantic_ai/providers/mistral.py` — blob `612a188c64deb7cafdce1e51e8f41f9a8b524189`.
- `tests/models/test_mistral.py` — blob `a7513c3d5bda9aca667fa3b54b65922e32b7d85e`.
- Grok profile source — `pydantic_ai_slim/pydantic_ai/profiles/grok.py`.

## External evidence
- Vercel's official AI Gateway page identifies `spacexai/grok-4.3` and SpaceXAI as its provider: https://vercel.com/ai-gateway/models/spacexai/grok-4.3.
- Mistral's official docs confirm Large 4 accepts `low`, `medium`, and `high` reasoning effort: https://docs.mistral.ai/inference/conversations/reasoning.
- The alias-to-Large-4 mapping for `mistral-large-latest` is supplied in Pydantic AI issue #14033 by the issue author; not independently verified against Mistral's live API here.

## Local validation
- `python test_wave8_contracts.py`: 18 provider-profile contract checks passed.
- `git apply --stat` parsed the Vercel and Mistral diffs.

## Not validated
- Full Pydantic AI tests, lint, formatting, static type checking, and API integration were not run.
- The patch files have not been applied to a complete current upstream checkout; `git apply --stat` is a syntax check only.
- No upstream PR or issue comment was created.
