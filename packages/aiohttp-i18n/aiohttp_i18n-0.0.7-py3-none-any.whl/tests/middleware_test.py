import pytest
from pathlib import Path

from aiohttp import web
from aiohttp_i18n.i18n import (
    _,
    set_locale,
    set_default_locale,
    load_gettext_translations,
)
from aiohttp_i18n.middleware import babel_middleware


TESTS_DIR = Path(__file__).parent


@pytest.fixture(autouse=True)
def locales():
    directory = TESTS_DIR / 'locale'
    domain = 'test'

    set_default_locale('ru')
    load_gettext_translations(directory, domain)


async def test_middleware_with_client(aiohttp_client):
    async def hello(request):
        set_locale('uk')
        return web.Response(text=str(_('Язык')))

    async def hello_default(request):
        return web.Response(text=str(_('Язык')))

    app = web.Application(middlewares=[babel_middleware])
    app.router.add_get('/', hello)
    app.router.add_get('/default', hello_default)

    client = await aiohttp_client(app)

    resp = await client.get('/')
    assert resp.status == 200

    text = await resp.text()
    assert 'Мова' in text

    resp = await client.get('/default')
    assert resp.status == 200

    text = await resp.text()
    assert 'Language' in text


async def test_middleware_with_headers(aiohttp_client):

    async def hello(request):
        return web.Response(text=str(_('Язык')))

    app = web.Application(middlewares=[babel_middleware])
    app.router.add_get('/', hello)

    client = await aiohttp_client(app, headers={'ACCEPT-LANGUAGE': 'uk'})

    resp = await client.get('/')
    assert resp.status == 200

    text = await resp.text()
    assert 'Мова' in text


async def test_middleware_with_cookies(aiohttp_client):

    async def hello(request):
        return web.Response(text=str(_('Язык')))

    app = web.Application(middlewares=[babel_middleware])
    app.router.add_get('/', hello)

    client = await aiohttp_client(app, cookies={'locale': 'uk'})

    resp = await client.get('/')
    assert resp.status == 200

    text = await resp.text()
    assert 'Мова' in text
