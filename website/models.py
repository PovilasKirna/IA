from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask_login import UserMixin
from sqlalchemy.sql import func
from flask import current_app
from . import db

class Proposal(db.Model):
    id = db.Column(
        db.Integer,
        primary_key=True
    )
    name = db.Column(
        db.String(50),
        nullable=False
    )
    description = db.Column(
        db.Text(10000),
        nullable=False
    )
    starting_date = db.Column(
        db.DateTime,
        nullable=True
    )
    ending_date = db.Column(
        db.DateTime,
        nullable=True
    )
    proposal_status = db.Column(
        db.String(20),
        default='Pending',
        nullable=False
    )
    date_created = db.Column(
        db.DateTime(timezone=True),
        default=func.now()
    )
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('user.id')
    )
    def get_reset_token(self, expires_sec=600):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'proposal_id' : self.id}).decode('utf-8')
    
    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            proposal_id = s.loads(token)['proposal_id']
        except:
            return None
        return Proposal.query.get(proposal_id)
    
    def __repr__(self):
        return '<Proposal {}>'.format(self.name)

class User(db.Model, UserMixin):
    
    id = db.Column(
        db.Integer,
        primary_key=True
    )
    name = db.Column(
        db.String(50),
        nullable=False
    )
    surname = db.Column(
        db.String(50),
        nullable=False
    )
    email = db.Column(
        db.String(100),
        index=True,
        unique=True,
        nullable=False
    )
    password = db.Column(
        db.String(255),
        nullable=False
    )
    phone = db.Column(
        db.String(15),
        nullable=False
    )
    registered = db.Column(
        db.Boolean,
        default=False
    )
    active = db.Column(
        db.Boolean,
        nullable=True
    )
    confirmed_At = db.Column(
        db.DateTime,
        nullable=True
    )
    role = db.Column(
        db.String(10),
        nullable=True
    )
    profile_picture = db.Column(
        db.String(50),
        nullable=False,
        default='default.png'
    )
    
    def get_reset_token(self, expires_sec=600):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id' : self.id}).decode('utf-8')
    
    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)
    
    proposals = db.relationship('Proposal')
    events = db.relationship('ClassEvent')


class ClassEvent(db.Model):
    id = db.Column(
        db.Integer,
        primary_key=True
    )
    name = db.Column(
        db.String(50),
        nullable=False
    )  
    starting_date = db.Column(
        db.DateTime,
        nullable=False
    )
    ending_date = db.Column(
        db.DateTime,
        nullable=False
    )
    starting_location = db.Column(
        db.String(100),
        default='',
        nullable=False
    )
    ending_location = db.Column(
        db.String(100),
        default='',
        nullable=False
    )
    route = db.Column(
        db.String(500),
        default='',
        nullable=False
    )
    goal = db.Column(
        db.String(500),
        default='',
        nullable=False
    )
    event_content = db.Column(
        db.String(1000),
        default='',
        nullable=False
    )
    skipped_lessons = db.Column(
        db.String(20),
        default='',
        nullable=False
    )
    teacher = db.Column(
        db.String(50),
        nullable=False
    )
    assistant = db.Column(
        db.String(50),
        nullable=False
    )
    destination = db.Column(
        db.String(100),
        nullable=False
    )  
    atending_class = db.Column(
        db.Integer,
        db.ForeignKey('class.id')
    )
    document = db.Column(
        db.String(50),
        nullable=False,
        default='template.docx'
    )
    date_created = db.Column(
        db.DateTime(timezone=True),
        default=func.now()
    )
    event_status = db.Column(
        db.String(20),
        default='Pending',
        nullable=False
    )
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('user.id')
    )
    
    def __repr__(self):
        return '<Event {}>'.format(self.name)

class Parent(db.Model):
    id = db.Column(
        db.Integer,
        primary_key=True
    )
    name = db.Column(
        db.String(50),
        nullable=False
    )
    surname = db.Column(
        db.String(50),
        nullable=False
    )
    email = db.Column(
        db.String(100),
        index=True,
        unique=True,
        nullable=False
    )
    phone = db.Column(
        db.String(15),
        nullable=False
    )
    child_id = db.Column(
        db.Integer,
        db.ForeignKey('pupil.id')
    )

class Pupil(db.Model):
    id = db.Column(
        db.Integer,
        primary_key=True
    )
    name = db.Column(
        db.String(50),
        nullable=False
    )
    surname = db.Column(
        db.String(50),
        nullable=False
    )
    email = db.Column(
        db.String(100),
        index=True,
        unique=True,
        nullable=False
    )
    phone = db.Column(
        db.String(15),
        nullable=False
    )
    pupilCode = db.Column(
        db.String(10),
        nullable=False,
        unique=True
    )
    birthdate = db.Column(
        db.Date,
        nullable=False
    )
    tevai = db.relationship('Parent')
    klase = db.Column(
        db.Integer,
        db.ForeignKey('class.id')
    )
    
    def __repr__(self):
        return '<Student {}, {} {}>'.format(self.pupilCode, self.name, self.surname)
    
class Class(db.Model):
    id = db.Column(
        db.Integer,
        primary_key=True
    )
    name = db.Column(
        db.String(50),
        nullable=False
    )
    
    pupils = db.relationship('Pupil')
    
    def __repr__(self):
        return '<Class {}>' % (self.name)
