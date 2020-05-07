from flask import jsonify
from flask_mail import Message, smtplib
from app import mail


def make_response_telegram(res: dict):
    """make response from telegram API response"""
    if res.get('ok'):
        return jsonify(status=True)

    if not res.get('ok'):
        return jsonify(
            status=False,
            error_code=res.get('error_code'),
            description=res.get('description')
        )


def send_mail_and_make_response(data: dict):
    """send email and make response"""
    address = data.get('email')
    subject = data.get('subject')
    body = data.get('body')
    res = {
        'status': False,
        'description': 'E-mail was sent'
    }

    msg = Message(subject, recipients=[address], body=body)

    try:
        mail.send(msg)
        res['status'] = True
    except smtplib.SMTPRecipientsRefused as e:
        res['description'] = str(e)
    return jsonify(
        status=res['status'],
        description=res['description']
    )
