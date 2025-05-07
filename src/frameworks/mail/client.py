import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class MailingClient:
  def __init__(self):
    pass
    # Mailing Client requires the possibility to send emails
    # If the user has not set up the environment variables, it will not work
    # but only print to the console that is sending an email
    # self._server = smtplib.SMTP('smtp.gmail.com', 587)
    # self._mail_user = os.environ.get("MAIL_USER")
  
  def login(self):
    print("Logging in...")
    # self._server.starttls()
    # self._server.login(self._mail_user, os.environ.get("APP_PASSWORD"))
    
  def logout(self):
    print("Logging out...")
    # self._server.quit()
  
  def send_mail(self, recipient: str, subject: str, body: str):
    try:
      # mail = MIMEMultipart()
      # mail['From'] = self._mail_user
      # mail['To'] = recipient
      # mail['Subject'] = subject
      # mail.attach(MIMEText(body, "html"))
      # self._server.sendmail(self._mail_user, recipient, mail.as_string())
      print(f"Enviando correo a {recipient} con asunto: {subject}")
    except Exception as e:
      print(f"Error enviando correo: {e}")
