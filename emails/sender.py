import os

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


def send_email(from_email, to_emails, subject, content):
    message = Mail(
        from_email=from_email,
        to_emails=to_emails,
        subject=subject,
        html_content=content,
    )
    try:
        key = os.getenv('SENDER_API_KEY')
        sg = SendGridAPIClient(key)
        response = sg.send(message)
        print(response.status_code)
    except Exception as e:
        print(e)
