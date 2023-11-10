from app import db


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(90), nullable=False, unique=True)
    name = db.Column(db.String(90), nullable=False)
    email = db.Column(db.String(90), nullable=False, unique=True)
    password = db.Column(db.String(90), nullable=False)
    count = db.Column(db.Integer())

