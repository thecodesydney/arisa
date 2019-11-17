from flask import render_template, current_app
from app.chatbot import bp
from app.email import send_email


@bp.route('/send_report')
def send_report(email, filename):
    file_path = current_app.config['REPORT_FOLDER'] / filename
    file_path = str(file_path.resolve())
    return send_email(subject='Arisa chatbot report',
                      sender=current_app.config['MAIL_FROM'],
                      recipients=[email],
                      text_body=render_template('chatbot/email_send_report.txt'),
                      html_body=render_template('chatbot/email_send_report.html'),
                      file_path=file_path)

'''
def test_send():
    send_report('kevin_foong@yahoo.com', 'test.txt')
'''
