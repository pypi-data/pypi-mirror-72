To set default locale change DEFAULT_LOCALE

Usage:

1. Add translations dirs
    locales_dir = APP_DIR / 'locale'
    set_default_locale(app_config['locale'])
    load_gettext_translations(str(locales_dir), LOCALES_DOMAIN_NAME)

2. Add middleware to application
    app = web.Application(
        debug=app_config['debug'],
        middlewares=[
            babel_middleware(),
        ]
    )
