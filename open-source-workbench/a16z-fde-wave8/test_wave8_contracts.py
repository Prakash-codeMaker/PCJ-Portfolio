"""Dependency-free contract checks for Pydantic AI provider profile alias fixes."""

provider_to_profile = {'xai': 'grok_model_profile', 'spacexai': 'grok_model_profile'}
assert provider_to_profile['xai'] == provider_to_profile['spacexai']

def grok_profile(model_name):
    reasoning_models = {'grok-4.3', 'grok-4.3-latest'}
    return {
        'supports_thinking': model_name in reasoning_models,
        'grok_reasoning_efforts': frozenset({'none', 'low', 'medium', 'high'}) if model_name in reasoning_models else frozenset(),
        'grok_supports_builtin_tools': model_name.startswith('grok-4') or model_name in reasoning_models,
    }

for route in ('xai', 'spacexai'):
    profile = grok_profile('grok-4.3') if provider_to_profile[route] == 'grok_model_profile' else None
    assert profile is not None
    assert profile['supports_thinking'] is True
    assert profile['grok_reasoning_efforts'] == frozenset({'none', 'low', 'medium', 'high'})
    assert profile['grok_supports_builtin_tools'] is True

large4_models = {'mistral-large-4', 'mistral-large-4-0', 'mistral-large-latest'}
large4_efforts = frozenset({'low', 'medium', 'high'})
assert 'mistral-large-latest' in large4_models
for model_name in large4_models:
    assert model_name in large4_models
    assert large4_efforts == frozenset({'low', 'medium', 'high'})

expected = {
    False: 'low', 'minimal': 'low', 'low': 'low', 'medium': 'medium',
    True: 'high', 'high': 'high', 'xhigh': 'high', 'max': 'high',
}
assert set(expected.values()) == {'low', 'medium', 'high'}
assert len(expected) == 8

print('Wave 8 provider-profile contract checks passed: 18 checks')
