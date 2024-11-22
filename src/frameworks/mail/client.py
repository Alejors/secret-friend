class MailingClient:
  def __init__(self):
    pass
  
  def send_mail(self, recipient: str, subject: str, body: str):
    print(f"Sending mail to {recipient}, about {subject}, saying {body}")
    return True