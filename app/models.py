from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, AnonymousUserMixin
from . import db, login_manager, mongo
import datetime

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    
    password_hash = db.Column(db.String(128))

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def is_administrator(self):
        if(self.email == '409430484@qq.com'):
            return True    
        return False

    @staticmethod
    def generate_fake(count=10):
        from sqlalchemy.exc import IntegrityError
        from random import seed
        import forgery_py

        seed()
        for i in range(count):
            u = User(email = forgery_py.internet.email_address(),
                username = forgery_py.internet.user_name(True),
                password = forgery_py.lorem_ipsum.word())
            db.session.add(u)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()
    def __repr__(self):
        return '<User %r>' % self.username

class AnonymousUser(AnonymousUserMixin):
    def is_administrator(self):
        return False 
        
login_manager.anonymous_user = AnonymousUser

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Questionnaire(mongo.Document):
    meta = {
        'collection':'questionnaire'
    }
    title = mongo.StringField(required = True,default = 'unamed questionnaire')
    tag = mongo.StringField()
    timestamp = mongo.DateTimeField(
            default = datetime.datetime.now()
        )
    user_id = mongo.StringField()
    
    def __repr__(self):
        return "Ques '{}'".format(self.title)

class Item(mongo.Document):
    question = mongo.StringField(required = True)
    no = mongo.IntField()
    kind = mongo.StringField()
    need = mongo.BooleanField()
    choice = mongo.ListField(mongo.StringField())
    vote = mongo.ListField(mongo.StringField())
    questionnaire = mongo.ReferenceField(Questionnaire)


class Map(mongo.EmbeddedDocument):
    #k_item = mongo.EmbeddedDocumentField(Item)
    v_choice = mongo.ListField(mongo.StringField())

class Answer(mongo.Document):
    meta = {
        'collection':'answer'
    }
    questionnaire = mongo.ReferenceField(Questionnaire)
    timestamp = mongo.DateTimeField(
            default = datetime.datetime.now()
        )
    map_list = mongo.ListField(mongo.EmbeddedDocumentField(Map))