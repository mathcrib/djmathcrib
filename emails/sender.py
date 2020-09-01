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