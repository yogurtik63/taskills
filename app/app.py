from flask import Flask, make_response, jsonify, request, abort
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from config import *

app = Flask(__name__)
app.config.from_object(Configuration)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from models import *


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.route('/user', methods=['GET'])
def get_user():
    result = {'user': 'ok'}

    return jsonify()


# @app.route('/user', methods=['POST'])
# def new_user():
#     if not request.json:
#         abort(400)


if __name__ == '__main__':
    app.run(debug=True)