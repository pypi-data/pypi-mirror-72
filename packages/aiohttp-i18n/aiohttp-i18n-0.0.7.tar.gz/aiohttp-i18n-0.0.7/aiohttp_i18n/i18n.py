import logging
import typing as t
import contextvars as c


from babel.support import LazyProxy

from .const import DEFAULT_LOCALE
from .locale import Locale, gettext_translations

logger = logging.getLogger(__name__)

ctx_locale: c.ContextVar[Locale] = c.ContextVar(
    'locale', default=Locale.get(DEFAULT_LOCALE)
)


def set_default_locale(code: str) -> None:
    gettext_translations.set_default_locale(code)


def load_gettext_translations(directory: str, domain: str) -> None:
    gettext_translations.load_translations(directory, domain)


def set_locale(code: str) -> None:
    locale = Locale.get(code)
    ctx_locale.set(locale)


def _make_lazy_gettext(lookup_func: t.Callable) -> t.Callable:
    def lazy_gettext(
        string: t.Union[LazyProxy, str],
        *args: t.Any,
        locale: t.Optional[str] = None,
        **kwargs: t.Any
    ) -> t.Union[LazyProxy, str]:

        if isinstance(string, LazyProxy):
            return string

        # disable cache by default, because it can make fluctations
        if 'enable_cache' not in kwargs:
            kwargs['enable_cache'] = False

        return LazyProxy(lookup_func, string, locale=locale, *args, **kwargs)
    return lazy_gettext


def _lookup_func(
    message: str, plural_message: t.Optional[str] = None,
    count: t.Optional[int] = None, **kwargs: t.Any,
) -> str:
    code = kwargs.pop('locale', None)
    locale = Locale.get(code) if code else ctx_locale.get()
    return locale.translate(message, plural_message, count, **kwargs)


_ = _make_lazy_gettext(_lookup_func)
