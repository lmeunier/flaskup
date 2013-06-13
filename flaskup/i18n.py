from flask import request
from flaskup import babel

AVAILABLE_LOCALES = ['fr', 'en', 'de']


@babel.localeselector
def get_locale():
    return request.accept_languages.best_match(AVAILABLE_LOCALES)
