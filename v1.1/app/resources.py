from flask_restful import Resource, reqparse, abort
from flask import request, jsonify, make_response
from models import *
import enum


class UserRole(enum.Enum):
    Admin = 0
    User = 1


def fields_checking(json, params: list):
    for param in params:
        if param not in json:
            return param


class UserRegistration(Resource):
    def post(self):
        if not request.json:
            abort(400)

        data = request.get_json()

        errors = fields_checking(data, ['username', 'email', 'password', 'role'])
        if errors:
            return make_response(jsonify({'Error': f'Missing {errors} field'}), 400)

        if User.find_by_username(data['username']):
            return {'message': 'User {} already exists'.format(data['username'])}
        elif User.find_by_email(data['email']):
            return {'message': 'User with email {} already exists'.format(data['email'])}
        else:
            user = User(username=data['username'],
                        email=data['email'],
                        password=User.generate_hash(data['password']),
                        role=UserRole[data['role']],
                        image=data['image'])

            user.save_to_db()

            return make_response(jsonify({'Response': 'Successful'}), 200)
        pass


class UserLogin(Resource):
    def post(self):
        if not request.json:
            abort(400)

        data = request.get_json()

        errors = fields_checking(data, ['username', 'password'])
        if errors:
            return make_response(jsonify({'Error': f'Missing {errors} field'}), 400)

        user = User.find_by_username(data['username'])

        if user is None:
            return make_response(jsonify({'Error': 'Non-existing user'}), 400)
        else:
            if User.verify_hash(data['password'], user.password):
                return make_response(jsonify({'Response': 'Successful login'}), 200)
            else:
                return make_response(jsonify({'Response': 'Wrong password'}), 400)


class AllUsers(Resource):
    def get(self):
        return jsonify(User.return_all())

    def delete(self):
        return {'message': 'Delete all users'}


class Orders(Resource):
    def get(self):
        data = request.get_json()

        errors = fields_checking(data, ['user_id'])
        if errors:
            return make_response(jsonify({'Error': f'Missing {errors} field'}), 400)

        if not User.find_by_username(data['username']):
            return make_response(jsonify({'Error': 'Non-existing user'}), 400)

        response = Order.find_order_by_user(data['username'])
        if not response:
            return make_response(jsonify({'Error': 'Non-existing order'}), 400)

        result = {
            'id': response.id,
            'status': response.status,
            'description': response.description,
            'date': response.date,
            'cost': response.cost,
            'address': response.address,
            'level': response.level
        }

        return jsonify(result)

    def post(self):
        data = request.get_json()

        errors = fields_checking(data, ['status', 'description', 'date', 'cost', 'address', 'user_id'])
        if errors:
            return make_response(jsonify({'Error': f'Missing {errors} field'}), 400)

        order = Order(
            status=data['status'],
            description=data['description'],
            date=data['date'],
            cost=data['cost'],
            address=data['address'],
            user_id=data['user_id']
        )

        Order.save_to_db(order)

        return make_response(jsonify({'Response': 'Successful added order'}), 200)


class MenuItems(Resource):
    def get(self):
        return jsonify(Menu.return_all())

    def post(self):
        data = request.get_json()

        errors = fields_checking(data, ['id', 'title', 'description', 'image', 'price'])
        if errors:
            return make_response(jsonify({'Error': f'Missing {errors} field'}), 400)

        menuItem = Menu(
            title=data['title'],
            description=data['description'],
            image=data['image'],
            price=data['price']
        )

        return jsonify(menuItem)
