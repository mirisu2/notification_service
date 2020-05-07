from flask import Flask, request
from flask_mail import Mail
import logging.handlers as handlers
import logging
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address


app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('production.cfg', silent=True)
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
