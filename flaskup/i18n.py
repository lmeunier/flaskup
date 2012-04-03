from flask import g, request
from flaskup import babel

AVAILABLE_LOCALES = [ 'fr', 'en' ]

@babel.localeselector
def get_locale():
    return request.accept_languages.best_match(AVAILABLE_LOCALES)

