from flask import render_template
from flaskup import app


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

"""
Sends an email to the administrators if an error occurs in Flaskup!
"""
if not app.debug and app.config['FLASKUP_ADMINS']:
    import logging
    from logging.handlers import SMTPHandler
    mailhost = (app.config['MAIL_SERVER'], app.config['MAIL_PORT'])
    fromaddr = app.config['DEFAULT_MAIL_SENDER']
    toaddrs = app.config['FLASKUP_ADMINS']
    subject = 'Flaskup: error'
    mail_handler = SMTPHandler(mailhost, fromaddr, toaddrs, subject)
    mail_handler.setLevel(logging.ERROR)
    app.logger.addHandler(mail_handler)
