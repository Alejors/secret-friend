import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class MailingClient:
  def __init__(self):
    self._server = smtplib.SMTP('smtp.gmail.com', 587)
    self._mail_user = os.environ.get("MAIL_USER")
  
  def login(self):
    self._server.starttls()
    self._server.login(self._mail_user, os.environ.get("APP_PASSWORD"))
    
  def logout(self):
    self._server.quit()
  
  def send_mail(self, recipient: str, subject: str, body: str):
    print(f"Sending mail to {recipient}, about {subject}, saying {body}")
    try:
      mail = MIMEMultipart()
      mail['From'] = self._mail_user
      mail['To'] = recipient
      mail['Subject'] = subject
      mail.attach(MIMEText(body, "html"))
      self._server.sendmail(self._mail_user, recipient, mail.as_string())
    except Exception as e:
      print(f"Error enviando correo: {e}")
