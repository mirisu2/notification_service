from flask import Blueprint, request, jsonify

from app import app
from app import bot_app

bp = Blueprint('v2', __name__, url_prefix='/api/v2')


@bp.before_request
def check_api_header():
    header_api_key = request.headers.get('X-Notify-Api-Key')
    if not header_api_key:
        return jsonify({'error': 'The request header does not have an API access key'}), 403
    if header_api_key not in app.config['ALLOWED_TOKENS']:
        # Maybe later I'll add a DB for storing tokens
        return jsonify({'error': 'Access denied'}), 403


@bp.route('/telegram', methods=['POST'])
def send_message_on_telegram():
    data = request.get_json(force=True)
    chat_id = int(data.get('id'))
    text = data.get('text')
    with bot_app:
        r = bot_app.send_message(chat_id, text)
    return str(r['outgoing'])
