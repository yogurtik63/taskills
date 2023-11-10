from flask import Flask, make_response, jsonify, request, abort
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from config import *

app = Flask(__name__)
app.config.from_object(Configuration)
app.config['JSON_AS_ASCII'] = False

db = SQLAlchemy(app)
# with app.app_context():
#     from models import *
#     db.create_all()

migrate = Migrate(app, db)

from models import *


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.route('/user', methods=['POST'])
def new_user():
    if not request.json:
        abort(400)

    user = User(username=request.json['username'],
                name=request.json['name'],
                email=request.json['email'],
                password=request.json['password'])

    db.session.add(user)
    db.session.commit()

    return make_response(jsonify({'Response': 'Successful'}), 200)


@app.route('/user/<username>', methods=['GET'])
def get_user(username):
    user = db.session.query(User).filter_by(username=username).first()

    result = {
        'username': user.username,
        'name': user.name,
        'email': user.email,
        'password': user.password,
        'role': user.role,
        'count': user.count
    }

    return jsonify(result)


# @app.route('/user', methods=['POST'])
# def new_user():
#     if not request.json:
#         abort(400)


if __name__ == '__main__':
    app.run(debug=True)