import os
from pathlib import Path
from fastapi.templating import Jinja2Templates
from config.settings import get_settings

settings = get_settings()
templates = Jinja2Templates(directory='templates/mails')

# conf = ConnectionConfig(
#     MAIL_USERNAME='',#os.environ.get("MAIL_USERNAME", ""),
#     MAIL_PASSWORD='pepjrjhppypcaqhc', #os.environ.get("MAIL_PASSWORD", ""),
#     MAIL_FROM='quantumsoftlutions@gmail.com',#os.environ.get("MAIL_USERNAME", ''),
#     MAIL_PORT=587,
#     MAIL_SERVER="smtp.gmail.com",
#     MAIL_STARTTLS=True,
#     MAIL_SSL_TLS=False,
#     MAIL_DEBUG=True,
#     TEMPLATE_FOLDER=Path(__file__).parent.parent / "templates",
#     USE_CREDENTIALS=os.environ.get("USE_CREDENTIALS", True),
#     VALIDATE_CERTS = os.environ.get("VALIDATE_CERTS", True),
# )

# fm = FastMail(conf)


# async def send_email(recipients: list, subject: str, context: dict, template_name: str,
#                      background_tasks: BackgroundTasks):
#     print(os.environ.get("MAIL_USERNAME", ""))
#     print(os.environ.get("MAIL_PASSWORD", ""))
#     message = MessageSchema(
#         subject=subject,
#         recipients=recipients,
#         template_body=context,
#         subtype=MessageType.html
#     )

#     background_tasks.add_task(fm.send_message, message, template_name=template_name)


import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from jinja2 import Environment, FileSystemLoader

async def send_email(recipients, subject, context, template_name):
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    usuario_smtp = 'quantumsoftlutions@gmail.com'
    contraseña_smtp = 'pepjrjhppypcaqhc'

    context['request'] = None

    mensaje = MIMEMultipart()
    mensaje['From'] = usuario_smtp
    mensaje['To'] = ', '.join(recipients)
    mensaje['Subject'] = subject


    cuerpo_renderizado = templates.TemplateResponse(
        name=template_name,
        context=context,
    ).body

    if isinstance(cuerpo_renderizado, bytes):
        cuerpo_renderizado = cuerpo_renderizado.decode('utf-8')

    mensaje.attach(MIMEText(cuerpo_renderizado, 'html'))

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(usuario_smtp, contraseña_smtp)
        server.sendmail(usuario_smtp, recipients, mensaje.as_string())

