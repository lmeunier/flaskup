from flask import request
from flaskup import app, babel

AVAILABLE_LOCALES = ['fr', 'en', 'de']


@babel.localeselector
def get_locale():
    return request.accept_languages.best_match(AVAILABLE_LOCALES)


app.jinja_env.globals['babel'] = babel
app.jinja_env.globals['babel_get_local'] = get_locale
