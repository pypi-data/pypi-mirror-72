from aiohttp_i18n import __all__


def test_imports():
    assert '_' in __all__
    assert 'babel_middleware' in __all__
    assert 'set_default_locale' in __all__
    assert 'load_gettext_translations' in __all__
    assert 'set_locale' in __all__
