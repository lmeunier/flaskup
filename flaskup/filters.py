from flaskup import app

@app.template_filter()
def dateformat(value, format='%H:%M / %d-%m-%Y'):
    return value.strftime(format)


