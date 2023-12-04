from flask import Flask, make_response, jsonify
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from config import *

import views, models, resources

app = Flask(__name__)
app.config.from_object(Configuration)
app.config['JSON_AS_ASCII'] = False

api = Api(app)

db = SQLAlchemy()


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


api.add_resource(resources.UserRegistration, '/registration')
api.add_resource(resources.UserLogin, '/login')
api.add_resource(resources.AllUsers, '/users')
api.add_resource(resources.Orders, '/order')


if __name__ == '__main__':
    from models import *
    db.init_app(app)

    with app.app_context():
        from models import *

        db.create_all()

    app.run(debug=False)