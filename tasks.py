import secret
from celery import Celery
from marrow.mailer import Mailer
from config import admin_mail

celery = Celery('tasks', backend='redis://localhost', broker='redis://localhost')


def configured_mailer():
    config = {
        'transport.debug': True,
        'transport.timeout': 1,
        'transport.user': 'smtp',
        'transport.host': 'smtp.exmail.qq.com',
        'transport.port': 465,
        'transport.tls': 'ssl',
        'transport.username': admin_mail,
        'transport.password': secret.mail_password,
    }
    m = Mailer(config)
    m.start()
    return m


@celery.task(bind=True)
def send_async(self, subject, author, to, plain):
    mailer = configured_mailer()
    try:
        m = mailer.new(
            subject=subject,
            author=author,
            to=to,
        )
        m.plain = plain
        mailer.send(m)
        raise ValueError('tetest')
    except Exception as exc:
        raise self.retry(exc=exc, countdown=10)
