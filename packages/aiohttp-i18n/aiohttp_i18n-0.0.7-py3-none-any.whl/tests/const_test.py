from aiohttp_i18n.const import DEFAULT_LOCALE


def test_const_default_locale():
    assert DEFAULT_LOCALE == 'en'
