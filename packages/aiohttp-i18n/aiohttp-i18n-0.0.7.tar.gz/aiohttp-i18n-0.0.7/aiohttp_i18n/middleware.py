import logging
import typing as t

from aiohttp import web
from babel.core import UnknownLocaleError

from .i18n import set_locale

logger = logging.getLogger(__name__)


@web.middleware
async def babel_middleware(
    request: web.Request,
    handler: t.Callable,
) -> t.Callable:
    ''' check headers first, then check cookies
    leave default locale if no lang code present
    '''
    _code = request.headers.get('ACCEPT-LANGUAGE')
    if _code:
        _code = _code[:2]
    if not _code:
        _code = request.cookies.get('locale')

    if _code:
        try:
            set_locale(_code)
        except (ValueError, UnknownLocaleError):
            pass
        except Exception as e:
            raise e

    return await handler(request)
