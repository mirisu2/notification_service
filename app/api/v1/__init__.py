import json

import requests
from flask import Blueprint, request, jsonify

from app import app
from app import app_func

bp = Blueprint('v1', __name__, url_prefix='/api/v1')


@bp.before_request
def check_api_header():
    header_api_key = request.headers.get('X-Notify-Api-Key')
    if not header_api_key:
        return jsonify({'error': 'The request header does not have an API access key'}), 403
    if header_api_key not in app.config['ALLOWED_TOKENS']:
        # Maybe later I'll add a DB for storing tokens
        return jsonify({'error': 'Access denied'}), 403


@bp.route('/telegram', methods=['GET', 'POST'])
def send_message_on_telegram():
    data = request.get_json()
    id = data.get('id')
    text = data.get('text')
    url = 'https://api.telegram.org/bot{}/sendMessage'.format(app.config.get('TELEGRAM_API_TOKEN'))
    try:
        res = requests.post(url,
                            data=json.dumps({"chat_id": id, "text": text}),
                            headers={
                                "Content-Type": "application/json",
                                "User-agent": "Mozilla/5.0 (X11; Linux x86_64) Chrome/75.0.3770.142 Safari/537.36"
                            }
                            )
        return app_func.make_response_telegram(res.json())

    except requests.exceptions.ConnectionError as e:
        return jsonify(
            status=False,
            error_text=str(e)
        )


@bp.route('/email', methods=['GET'])
def send_email():
    data = request.get_json()
    return app_func.send_mail_and_make_response(data)
