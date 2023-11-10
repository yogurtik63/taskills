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
    count = db.Column(db.Integer())

    def __repr__(self):
        return "<{}:{}>".format(self.id,  self.username)


class Route(db.Model):
    __tablename__ = 'routes'
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text(), nullable=False)
    image = db.Column(db.String(255), nullable=True)

    points = db.relationship('Point', backref='route')

    def __repr__(self):
        return "<{}:{}>".format(self.id, self.title[:10])