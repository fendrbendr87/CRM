from app import db, login, app
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from time import time
from datetime import datetime
import jwt
#from flask_admin import Admin
#from flask_admin.contrib.sqla import ModelView

#admin = Admin(app)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    People=db.relationship('People', backref='people', lazy='dynamic')
    ProfileNotes=db.relationship('ProfileNotes', backref='profilenotes', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash=generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
        {'reset_password': self.id, 'exp': time() + expires_in},
        app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)

#WHENEVER YOU EDIT THE MODELS, MAKE SURE YOU ADD THE NEW FIELDS TO THE FORMS YOU WILL BE PASSING BACK TO THE ROUTE.PY!
class People(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name=db.Column(db.String(20))
    last_name=db.Column(db.String(20))
    phone_cell=db.Column(db.Integer)
    ptype=db.Column(db.String(6))
    pstatus=db.Column(db.String(7))
    notes=db.Column(db.String(140))
    house_number=db.Column(db.String(140))
    street_name=db.Column(db.String(140))
    city_name=db.Column(db.String(140))
    state_name=db.Column(db.String(140))
    zip_code=db.Column(db.String(140))
    price=db.Column(db.Integer)
    user_account_pk=db.Column(db.Integer, db.ForeignKey('user.id'))
    ProfileNotes=db.relationship('ProfileNotes', backref='peopleprofilenotes', lazy='dynamic')

    def __repr__(self):
        return '<People> first_name: {}, last_name: {}, phone_cell: {}, ptype: {}, pstatus: {}, notes: {}'.format(self.first_name, self.last_name, self.phone_cell, self.ptype, self.pstatus, self.notes)

class ProfileNotes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pnotes=db.Column(db.String(280))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    people_account_pk=db.Column(db.Integer, db.ForeignKey('people.id'))
    user_account_pk=db.Column(db.Integer, db.ForeignKey('user.id'))


    def __repr__(self):
        return '<ProfileNotes> pnotes: {}'.format(self.pnotes)

class ClosedDeals(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name=db.Column(db.String(20))
    last_name=db.Column(db.String(20))
    phone_cell=db.Column(db.Integer)
    ptype=db.Column(db.String(6))
    house_number=db.Column(db.String(140))
    street_name=db.Column(db.String(140))
    city_name=db.Column(db.String(140))
    state_name=db.Column(db.String(140))
    zip_code=db.Column(db.String(140))
    price=db.Column(db.Integer)
    user_account_pk=db.Column(db.Integer, db.ForeignKey('user.id'))

#admin.add_view(ModelView(User, db.session))
#admin.add_view(ModelView(Prospects, db.session))
#admin.add_view(ModelView(Clients, db.session))

@login.user_loader
def load_user(id):
    return User.query.get(int(id))