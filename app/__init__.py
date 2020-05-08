from flask import Flask, request
from flask_mail import Mail
import logging.handlers as handlers
import logging
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from os import environ


app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('production.cfg', silent=True)
if not app.config.get('SECRET_KEY'):
    app.config['DEBUG'] = environ.get('DEBUG')
    app.config['ENV'] = environ.get('ENV')
    app.config['MAIL_SERVER'] = environ.get('MAIL_SERVER')
    app.config['MAIL_PORT'] = environ.get('MAIL_PORT')
    app.config['MAIL_USE_TLS'] = environ.get('MAIL_USE_TLS')
    app.config['MAIL_USE_SSL'] = environ.get('MAIL_USE_SSL')
    app.config['MAIL_DEBUG'] = environ.get('MAIL_DEBUG')
    app.config['MAIL_USERNAME'] = environ.get('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = environ.get('MAIL_PASSWORD')
    app.config['MAIL_DEFAULT_SENDER'] = environ.get('MAIL_DEFAULT_SENDER')
    app.config['MAIL_MAX_EMAILS'] = environ.get('MAIL_MAX_EMAILS')
    app.config['MAIL_ASCII_ATTACHMENTS'] = environ.get('MAIL_ASCII_ATTACHMENTS')
    app.config['MAIL_SUPPRESS_SEND'] = environ.get('MAIL_SUPPRESS_SEND')
    app.config['TELEGRAM_API_TOKEN'] = environ.get('TELEGRAM_API_TOKEN')
    app.config['ALLOWED_TOKENS'] = environ.get('ALLOWED_TOKENS')

mail = Mail(app)

ch_file = handlers.RotatingFileHandler('logs/app.log', maxBytes=1000000, backupCount=5)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
ch_file.setFormatter(formatter)

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=[],
    headers_enabled=True,
    strategy='fixed-window-elastic-expiry'
)
limiter.logger.addHandler(ch_file)


@limiter.request_filter
def ip_whitelist():
    return request.remote_addr == "127.0.0.1"


from app.api import v1
limiter.limit("5 per second")(v1.bp)
app.register_blueprint(v1.bp)


@app.route("/ping")
@limiter.limit("1 per minute", override_defaults=False)
def ping():
    return "PONG"
