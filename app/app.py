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


@app.route('/route', methods=['POST'])
def new_route():
    if not request.json:
        abort(400)

    route = Route(
        title=request.json['title'],
        description=request.json['description'],
        image=(request.json['image'] if request.json['image'] != '' else ''),
        edge_1=f"{request.json['edge_1'][0]} {request.json['edge_1'][1]}",
        edge_2=f"{request.json['edge_2'][0]} {request.json['edge_2'][1]}"
    )

    db.session.add(route)
    db.session.commit()

    return make_response(jsonify({'Response': 'Successful'}), 200)


@app.route('/route/<id>', methods=['GET'])
def get_route(id):
    if id != 0:
        route = db.session.query(Route).filter_by(id=id).first()

        result = {
            'title': route.title,
            'description': route.description,
            'image': route.image,
            'edge_1': list(map(int, route.edge_1.split())),
            'edge_2': list(map(int, route.edge_2.split()))
        }
    else:
        routes = db.session.query(Route).all()

        result = {
            'routes': [{'id': m_route.id,
                        'title': m_route.title,
                        'description': m_route.description,
                        'image': m_route.image,
                        'edge_1': list(map(int, m_route.edge_1.split())),
                        'edge_2': list(map(int, m_route.edge_2.split()))} for m_route in routes]}

    return jsonify(result)


@app.route('/route/<id>', methods=['DELETE'])
def delete_route(id):
    points = db.session.query(Point).filter_by(route_id=id).all()
    route = db.session.query(Point).filter_by(id=id).first()
    db.session.delete(points)
    db.session.delete(route)

    db.session.commit()

    return make_response(jsonify({'Response': 'Successful'}), 200)


@app.route('/point', methods=['POST'])
def new_point():
    if not request.json:
        abort(400)

    point = Point(
        title=request.json['title'],
        description=request.json['description'],
        image=(request.json['image'] if request.json['image'] != '' else ''),
        point_x=request.json['point_x'],
        point_y=request.json['point_y']
    )

    db.session.add(point)
    db.session.commit()

    return make_response(jsonify({'Response': 'Successful'}), 200)


@app.route('/point/<id>', methods=['GET'])
def get_point(id):
    points = db.session.query(Route).filter_by(route_id=id).first()

    result = {
        'points': [{'id': m_point.id,
                    'title': m_point.title,
                    'description': m_point.description,
                    'image': m_point.image,
                    'point_x': m_point.point_x,
                    'point_y': m_point.point_y} for m_point in points]}

    return jsonify(result)


if __name__ == '__main__':
    from models import *
    db.init_app(app)

    # with app.app_context():
    #     from models import *
    #
    #     db.create_all()

    app.run(debug=True)