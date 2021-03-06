import logging
from os import environ

from flask import Flask, request
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_mail import Mail
from pyrogram import Client

app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('production.cfg', silent=True)
if not app.config.get('SECRET_KEY'):
    app.config['DEBUG'] = environ.get('DEBUG')
    app.config['SECRET_KEY'] = environ.get('SECRET_KEY')
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
    app.config['API_ID'] = environ.get('API_ID')
    app.config['API_HASH'] = environ.get('API_HASH')

mail = Mail(app)

bot_app = Client("notify_bot", app.config['API_ID'], app.config['API_HASH'], bot_token=app.config['TELEGRAM_API_TOKEN'])

logger = logging.getLogger('__notify__')
ch_console = logging.StreamHandler()
ch_console.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
ch_console.setFormatter(formatter)
logger.addHandler(ch_console)

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=[],
    headers_enabled=True,
    strategy='fixed-window-elastic-expiry'
)
limiter.logger.addHandler(ch_console)


@limiter.request_filter
def ip_whitelist():
    return request.remote_addr == "127.0.0.1"


from app.api import v1, v2

limiter.limit("5 per second")(v1.bp)
limiter.limit("5 per second")(v2.bp)

app.register_blueprint(v1.bp)
app.register_blueprint(v2.bp)


@app.route("/ping")
@limiter.limit("2 per minute", override_defaults=False)
def ping():
    return "PONG"
