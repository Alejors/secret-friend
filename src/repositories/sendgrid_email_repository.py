from src.frameworks.mail.sendgrid_client import SendgridClient
from src.entities import User, Event, Wish
from src.interfaces import IMailerRepository
from src.utils.mail_constants import HEADER, FOOTER


class SendGridEmailRepository(IMailerRepository):
    def __init__(self, service: SendgridClient):
        self.service = service
    
    def send_new_user_email(self, user: User, password: str):
        body = HEADER + f"""
                <h2>Hello, {user.name}!</h2><br/>
                <p>You were recently included to a Secret Santa in Secret Santa APP!<br/>
                Because of this we created an account for you.<br/><br/> 
                The initial password is: <b>{password}</b>.<br/>
                You can change it in your profile. <br/><br/>
                You can also add ideas to your wishlist to help your secret Santa get you a gift you like!<br/>
                We will notify you when the event is drawn.</p>
                """ + FOOTER
        self.service.send_mail(user.email, f"You were included in a Secret Santa!", body)
        
    def send_event_drawn_mail(self, current_participant: User, picked_user: User, wishlist: list[Wish], event: Event):
        body = HEADER + f"""
            <h2>Hello!</h2>
            <p>The <b>{event.name}</b> Secret Santa event has been drawn!</p>
            <p>You are:</p>
            <h2>{picked_user.name}'s\U0001F973</h2>
            <p>Secret Santa!</p>
            """
        if wishlist:
            wishlist_elements = ''.join([f'<li><a href={item.url}>{item.element}</a></li>' for item in wishlist if item.element is not None])
            body = body + f"<br/><p>These are some ideas from their wishlist: \U0001F381</p><ul>{wishlist_elements}</ul>"
        if event.min_price or event.max_price:
            body = body + "<br/><p>Remember the gift:</p><ul>"
            if event.min_price:
                body = body + f"<li>Has a minimum price of: ${event.min_price}</li>"
            if event.max_price:
                body = body + f"<li>Has a maximum price of: ${event.max_price}</li>"
            body = body + "</ul>"
        body = body + FOOTER
        self.service.send_mail(current_participant.email, f"You are someone's secret Santa for: {event.name}", body)
