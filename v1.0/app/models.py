from datetime import datetime
from passlib.hash import pbkdf2_sha256 as sha256
from sqlalchemy.dialects.mysql import DECIMAL

from app import db
import enum


class UserRole(enum.Enum):
    Admin = 'Admin'
    User = 'User'


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(90), nullable=False, unique=True)
    email = db.Column(db.String(90), nullable=False, unique=True)
    password = db.Column(db.String(90), nullable=False)
    role = db.Column(db.Enum(UserRole), nullable=False)
    image = db.Column(db.String(255), nullable=True)
    level = db.Column(db.Integer())
    count = db.Column(db.Integer())

    @staticmethod
    def generate_hash(password):
        return sha256.hash(password)

    @staticmethod
    def verify_hash(password, hash):
        return sha256.verify(password, hash)

    def __repr__(self):
        return "<{}:{}>".format(self.id,  self.username)


class Route(db.Model):
    __tablename__ = 'routes'

    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text(), nullable=False)
    image = db.Column(db.String(255), nullable=True)
    edge_1 = db.Column(db.String(128))
    edge_2 = db.Column(db.String(128))

    points = db.relationship('Point', backref='route')

    def __repr__(self):
        return "<{}:{}>".format(self.id, self.title[:10])


class Point(db.Model):
    __tablename__ = 'points'

    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text(), nullable=False)
    image = db.Column(db.String(255), nullable=True)
    location = db.Column(db.String(128), nullable=False)
    route_id = db.Column(db.Integer(), db.ForeignKey('routes.id'))

    def __repr__(self):
        return "<{}:{}>".format(self.id, self.title[:10])


class Event(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text(), nullable=False)
    image = db.Column(db.String(255), nullable=True)
    date = db.Column(db.DateTime(), default=datetime.now())

    def __repr__(self):
        return "<{}:{}>".format(self.id, self.title[:10])


class Ticket(db.Model):
    __tablename__ = 'tickets'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    reg_date = db.Column(db.DateTime(), default=datetime.now())
    event_id = db.Column(db.Integer(), db.ForeignKey('events.id'))
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'))

    def __repr__(self):
        return "<{}:{}>".format(self.id, self.title[:10])