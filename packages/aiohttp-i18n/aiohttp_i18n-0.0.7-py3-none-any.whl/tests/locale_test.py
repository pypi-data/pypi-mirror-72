from pathlib import Path

import pytest
from aiohttp_i18n.i18n import ctx_locale
from aiohttp_i18n.locale import gettext_translations, Translations


TESTS_DIR = Path(__file__).parent
DIRECTORY = TESTS_DIR / 'locale'
DOMAIN = 'test'


def test_locale_load_file_count(mocker):
    mocker.spy(Translations, 'load')
    gettext_translations.load_translations(DIRECTORY, DOMAIN)
    assert Translations.load.call_count == 2


def test_locale_load_file_except(mocker):

    gettext_translations._translations = {}
    mocker.patch.object(
        Translations, 'load', side_effect=ValueError('something wrong')
    )
    gettext_translations.load_translations(DIRECTORY, DOMAIN)
    assert len(gettext_translations.supported_locales) == 1


def test_locale_except(mocker):
    locale = ctx_locale.get()
    with pytest.raises(Exception):
        locale.translate('test', plural_message='test')

    assert locale.translate('test', plural_message='test', count=1) == 'test'
    assert locale.translate('test', plural_message='test', count=2) == 'test'
