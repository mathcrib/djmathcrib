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
        key = os.getenv('SENDGRID_API_KEY')
        print(key)
        sg = SendGridAPIClient('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')
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
    except Exception as e:
        print(e)