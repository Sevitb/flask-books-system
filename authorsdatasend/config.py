import os

TESTING=True

SQLALCHEMY_DATABASE_URI='sqlite:///isc.db'
SQLALCHEMY_TRACK_MODIFICATIONS=False

MAIL_SERVER='mail.authorsdatasend.ru'
MAIL_PORT=465
MAIL_USE_TLS=True
MAIL_USERNAME='info@authorsdatasend.ru'
MAIL_DEFAULT_SENDER='info@authorsdatasend.ru'
MAIL_PASSWORD=os.environ.get("MAIL_PASSWORD")

SECRET_KEY=os.environ.get("SECRET_KEY")
