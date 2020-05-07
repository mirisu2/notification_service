from flask import Blueprint, request, jsonify
import json
from app import app
import requests
from app import app_func

bp = Blueprint('api', __name__, url_prefix='/api/v1')


@bp.before_request
def check_api_header():
    header_api_key = request.headers.get('X-Notify-Api-Key')
    if not header_api_key:
        return jsonify({'error': 'The request header does not have an API access key'}), 403
    if header_api_key not in app.config['ALLOWED_TOKENS']:
        # Maybe later I'll add a DB for storing tokens
        return jsonify({'error': 'Access denied'}), 403


@bp.route('/telegram', methods=['GET'])
def input_search():
    data = request.get_json()
    id = data.get('id')
    text = data.get('text')
    url = 'https://api.telegram.org/bot{}/sendMessage'.format(app.config.get('TELEGRAM_API_TOKEN'))
    res = requests.post(url,
                        data=json.dumps({ "chat_id": id, "text": text}),
                        headers={
                            "Content-Type": "application/json",
                            "User-agent": "Mozilla/5.0 (X11; Linux x86_64) Chrome/75.0.3770.142 Safari/537.36"
                            }
                        )
    return app_func.make_response_telegram(res.json())


@bp.route('/email', methods=['GET'])
def get_last_calls():
    data = request.get_json()
    return app_func.send_mail_and_make_response(data)
