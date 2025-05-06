from src.entities import User, Event, Wish
from src.interfaces import IMailerRepository
from src.utils.mail_constants import HEADER, FOOTER


class GmailEmailRepository(IMailerRepository):
    def __init__(self, service):
        self.service = service
    
    def send_new_user_email(self, user: User, password: str):
        self.service.login()
        body = HEADER + f"""
                <h2>Hola, {user.name}!</h2><br/>
                <p>Se te incluyó recientemente en un concurso de Amigo Secreto APP!<br/>
                Por eso hemos creado una cuenta para ti. <br/><br/> 
                La clave inicial es: <b>{password}</b>.<br/>
                En tu perfil puedes modificarla. <br/><br/>
                Además puedes agregar una pequeña lista de deseos para ayudar a que te compren algo que te guste!<br/>
                Te notificaremos por correo cuando se realice el sorteo.</p>
                """ + FOOTER
        self.service.send_mail(user.email, f"Se te incluyó en un Amigo Secreto!", body)
        self.service.logout()
        
    def send_event_drawn_mail(self, current_participant: User, picked_user: User, wishlist: list[Wish], event: Event):
        self.service.login()
        body = HEADER + f"""
            <h2>Hola!</h2>
            <p>Se realizó el sorteo de <b>{event.name}</b>!</p>
            <p>Tu amigo secreto es:</p>
            <h2>{picked_user.name}!\U0001F973</h2>
            """
        if wishlist:
            wishlist_elements = ''.join([f'<li><a href={item.url}>{item.element}</a></li>' for item in wishlist if item.element is not None])
            body = body + f"<br/><p>Algunas ideas de regalo \U0001F381 son:</p><ul>{wishlist_elements}</ul>"
        if event.min_price or event.max_price:
            body = body + "<br/><p>Recuerda que el regalo:</p><ul>"
            if event.min_price:
                body = body + f"<li>Tiene un monto mínimo de: ${event.min_price}</li>"
            if event.max_price:
                body = body + f"<li>Tiene un monto máximo de: ${event.max_price}</li>"
            body = body + "</ul>"
        body = body + FOOTER
        self.service.send_mail(current_participant.email, f"Tu amigo secreto para: {event.name}", body)
        self.service.logout()
