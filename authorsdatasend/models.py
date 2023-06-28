from authorsdatasend import db, login_manager
from flask_login import (LoginManager, UserMixin, login_required,
			  login_user, current_user, logout_user)
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(100),unique=True)
    password_hash = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    
    def __repr__(self):
        return "<{}:{}>".format(self.id, self.username)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self,  password):
        return check_password_hash(self.password_hash, password)

class Books(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Title =  db.Column(db.Text, nullable=False)
    allowRegistration =  db.Column(db.Integer, nullable=False, default=1)

class Chapters(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bookID = db.Column(db.Integer, nullable=False)
    bookTitle = db.Column(db.Text, nullable = False)
    chapterTitle = db.Column(db.Text, nullable=False)
    authorsCount = db.Column(db.Integer, nullable=False)
    authorsCountMax = db.Column(db.Integer, nullable=False)
    allowRegistration =  db.Column(db.Integer, nullable=False, default=1)

    def getAuthCount(self):
        return self.authorsCount

    def getAuthCountMax(self):
        return self.authorsCountMax
    
    def increaseAuthCount(self):
        self.authorsCount += 1
        return True

    def setAuthCountMax(self):
        self.authorsCountMax
        return True

class AuthorsTable(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lastName = db.Column(db.String(150), nullable=False)
    firstName = db.Column(db.String(150), nullable=False)
    midName = db.Column(db.String(150), nullable=False)
    jobAddress = db.Column(db.Text, nullable=False)
    jobAddress1 = db.Column(db.Text, nullable=False)
    ORCID = db.Column(db.Text, nullable=False)
    lastNameTranslit = db.Column(db.String(150), nullable=False)
    firstNameTranslit = db.Column(db.String(150), nullable=False)
    midNameTranslit = db.Column(db.String(150), nullable=False)
    bookTitle = db.Column(db.Text, nullable=False)
    chapterTitle = db.Column(db.Text, nullable=False)
    phoneNumber = db.Column(db.String(50), nullable=False)
    bookID = db.Column(db.Integer, nullable=False)
    chapterID = db.Column(db.Integer, nullable=False)
    emailAdress = db.Column(db.String(150), nullable=False)
    authorComment = db.Column(db.Text, default=False)
    paid = db.Column(db.Boolean, default=False)
    comment = db.Column(db.Text, default=False, nullable=True)


@login_manager.user_loader
def load_user(user_id):
    return db.session.query(User).get(user_id)