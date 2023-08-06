from __future__ import annotations

import os
import logging
import typing as t

from babel.core import Locale as _Locale
from babel.support import Translations, NullTranslations

from .const import DEFAULT_LOCALE

logger = logging.getLogger(__name__)


class _GettextTranslations:
    _translations: t.Dict[str, t.Union[Translations, NullTranslations]] = {}
    _default_locale: str = DEFAULT_LOCALE
    _supported_locales: t.Set[str] = set()

    @property
    def translations(self) -> t.Dict[
        str, t.Union[Translations, NullTranslations]
    ]:
        return self._translations

    @property
    def supported_locales(self) -> t.Set[str]:
        return self._supported_locales

    @property
    def default_locale(self) -> str:
        return self._default_locale

    def set_default_locale(self, code: str) -> None:
        self._default_locale = code
        _supported_locales = set(self._translations.keys())
        _supported_locales.add(self.default_locale)
        self._supported_locales = _supported_locales

    def load_translations(self, directory: str, domain: str) -> None:
        for lang in os.listdir(directory):
            if os.path.isfile(os.path.join(directory, lang)):
                continue
            try:
                translation = Translations.load(directory, [lang], domain)
                if lang in self._translations:
                    self._translations[lang].merge(translation)
                else:
                    self._translations[lang] = translation
            except Exception as e:
                logging.error(
                    "Cannot load translation for '%s': %s", lang, str(e)
                )
                continue
        self._supported_locales = set(self._translations.keys())
        self._supported_locales.add(self.default_locale)
        logging.info("Supported locales: %s", sorted(self._supported_locales))


gettext_translations = _GettextTranslations()


class Locale(_Locale):

    @classmethod
    def get(cls, code: str) -> Locale:
        if code not in gettext_translations.supported_locales:
            code = gettext_translations.default_locale

        translations = gettext_translations.translations.get(
            code, NullTranslations()
        )
        locale = cls.parse(code)
        locale.translations = translations
        return locale

    def translate(
        self,
        message: str,
        plural_message: t.Optional[str] = None,
        count: t.Optional[int] = None,
        **kwargs: str,
    ) -> str:
        """ Translate message
        """
        if plural_message is not None:
            assert count is not None
            message = self.translations.ungettext(
                message, plural_message, count
            )
        else:
            message = self.translations.ugettext(message)

        return message.format(**kwargs) if len(kwargs) else message
