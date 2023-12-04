from datetime import datetime
from passlib.hash import pbkdf2_sha256 as sha256

from app import db


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(90), nullable=False, unique=True)
    email = db.Column(db.String(90), nullable=False, unique=True)
    password = db.Column(db.String(90), nullable=False)
    role = db.Column(db.Integer(), nullable=False)
    image = db.Column(db.String(255), nullable=True)

    order = db.relationship('Order', backref='orders')

    @staticmethod
    def generate_hash(password):
        return sha256.hash(password)

    @staticmethod
    def verify_hash(password, hash):
        return sha256.verify(password, hash)

    def __repr__(self):
        return "<{}:{}>".format(self.id,  self.username)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(username=email).first()

    @classmethod
    def return_all(cls):
        def to_json(x):
            return {
                'username': x.username,
                'password': x.password
            }

        return {'users': list(map(lambda x: to_json(x), User.query.all()))}


class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer(), primary_key=True)
    status = db.Column(db.Integer(), nullable=False)
    description = db.Column(db.String(50), nullable=False)
    date = db.Column(db.DateTime(), default=datetime.now())
    cost = db.Column(db.Integer(), nullable=False)
    address = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'))

    user = db.relationship('User', backref='user')

    def __repr__(self):
        return "<{}:{}>".format(self.id, self.title[:10])

    @classmethod
    def find_order_by_user(cls, username):
        user_id = User.find_by_username(username).id
        return cls.query.filter_by(user_id=user_id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()


class Menu(db.Model):
    __tablename__ = 'menu'

    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    description = db.Column(db.Text(), nullable=False)
    image = db.Column(db.String(255), nullable=True)
    price = db.Column(db.Integer(), nullable=False)

    def __repr__(self):
        return "<{}:{}>".format(self.id, self.title[:10])

    @classmethod
    def return_all(cls):
        def to_json(x):
            return {
                'id': x.id,
                'title': x.title,
                'description': x.description,
                'image': x.image,
                'price': x.price
            }

        return {'menu': list(map(lambda x: to_json(x), Menu.query.all()))}

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()