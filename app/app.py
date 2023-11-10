from flask import Flask, make_response, jsonify, request, abort
from flask_sqlalchemy import SQLAlchemy

from config import *

app = Flask(__name__)
app.config.from_object(Configuration)
app.config['JSON_AS_ASCII'] = False

db = SQLAlchemy()


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.route('/user', methods=['POST'])
def new_user():
    if not request.json:
        abort(400)

    user = User(username=request.json['username'],
                email=request.json['email'],
                password=request.json['password'],
                role=UserRole[request.json['role']],
                count=0)

    db.session.add(user)
    db.session.commit()

    return make_response(jsonify({'Response': 'Successful'}), 200)


@app.route('/user/<username>', methods=['GET'])
def get_user(username):
    user = db.session.query(User).filter_by(username=username).first()

    result = {
        'username': user.username,
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
    db.init_app(app)
    with app.app_context():
        from models import *

        db.create_all()

    app.run(debug=True)