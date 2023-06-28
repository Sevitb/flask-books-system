import os
from authorsdatasend import app, mail, db
from flask_mail import Mail, Message
from flask import render_template

def send_mail(subject, recipient, template, **kwargs):
    msg = Message(subject, recipients=[recipient])
    msg.html = render_template(template, **kwargs)
    mail.send(msg)
    return True