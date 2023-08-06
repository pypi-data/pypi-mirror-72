from pathlib import Path

from babel.support import Translations

from aiohttp_i18n.i18n import (
    _,
    _lookup_func,
    ctx_locale,
    set_locale,
    set_default_locale,
    load_gettext_translations,
)
from aiohttp_i18n.locale import Locale, gettext_translations
from aiohttp_i18n.const import DEFAULT_LOCALE


TESTS_DIR = Path(__file__).parent


def test_ctx_locale():
    assert isinstance(ctx_locale.get(), Locale)


def test_ctx_locale_language():
    locale = ctx_locale.get()
    assert locale.language == DEFAULT_LOCALE


def test_set_default_locale():
    set_default_locale('uk')
    assert gettext_translations.default_locale == 'uk'


def test_set_locale():
    set_locale('uk')
    locale = ctx_locale.get()
    assert locale.language == 'uk'


def test_load_gettext_translations_case_1():
    directory = TESTS_DIR / 'locale'
    domain = 'test'
    langs = ('en', 'uk')

    # case 1 when all locales has translations
    load_gettext_translations(directory, domain)
    assert len(gettext_translations.supported_locales) == 2
    assert gettext_translations.supported_locales - set(langs) == set()
    assert len(gettext_translations.translations) == 2

    for lang, translation in gettext_translations.translations.items():
        assert lang in langs
        assert isinstance(translation, Translations), type(translation)


def test_load_gettext_translations_case_2():
    directory = TESTS_DIR / 'locale'
    domain = 'test'
    langs = ('en', 'uk')

    # case 2 when not all locales has translations
    set_default_locale('ru')
    load_gettext_translations(directory, domain)
    assert len(gettext_translations.supported_locales) == 3
    assert gettext_translations.supported_locales - set(langs) == {'ru'}
    assert len(gettext_translations.translations) == 2

    for lang, translation in gettext_translations.translations.items():
        assert lang in langs
        assert isinstance(translation, Translations), type(translation)


def test_make_lazy_gettext():
    set_locale('en')
    assert _('Язык') == 'Language'

    set_locale('ru')
    assert _('Язык') == 'Язык'

    set_locale('uk')
    assert _('Язык') == 'Мова'
    assert _(_('Язык')) == 'Мова'
    assert _('Test') == 'Test'


def test_gettext_via_locale():
    directory = TESTS_DIR / 'locale'
    domain = 'test'
    load_gettext_translations(str(directory), domain)

    set_locale('ru')

    assert str(_('Язык', locale='en')) == 'Language'
    assert str(_('Язык')) == 'Язык'

    assert str(_('Язык', locale='uk')) == 'Мова'
    assert str(_('Язык')) + '' == 'Язык'


def test__lookup_func():
    directory = TESTS_DIR / 'locale'
    domain = 'test'
    load_gettext_translations(str(directory), domain)

    set_locale('en')
    assert _lookup_func('Язык') == 'Language'
    assert _lookup_func('Test') == 'Test'
