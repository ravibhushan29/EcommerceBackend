from django.core.mail import send_mail


class CustomException(Exception):
    pass


def mail(subject, message_apply, from_email, receiver, html_message=None):
    send_mail(subject, message_apply, 'Ecommerce'+'<'+from_email+'>', receiver, html_message=html_message)
    return 'Mails sent'