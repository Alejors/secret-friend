import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


class SendgridClient:
    def __init__(self):
        self._client = SendGridAPIClient(os.environ.get("SENDGRID_API_KEY"))
        self._mail_user = os.environ.get("MAIL_USER")
    
    def send_mail(self, recipient: str, subject: str, body: str):
        try:
            mail = Mail(
                from_email=self._mail_user,
                to_emails=recipient,
                subject=subject,
                html_content=body
            )
            response = self._client.send(mail)
            if response.status_code == 202:
                print(f"Email sent to {recipient}")
        except Exception as e:
            print(f"Error Sending Mail: {e}")
