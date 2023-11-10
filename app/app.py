import sqlalchemy
from flask import Flask, make_response, jsonify, request, abort
from flask_sqlalchemy import SQLAlchemy
from utils import *
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
                image=request.json['image'],
                count=0)

    db.session.add(user)
    db.session.commit()

    return make_response(jsonify({'Response': 'Successful'}), 200)


@app.route('/user/<username>', methods=['GET'])
def get_user(username):
    user = db.session.query(User).filter_by(username=username).first()

    result = {
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'password': user.password,
        'role': user.role.value,
        'image': user.image,
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
        image=request.json['image'],
        edge_1=f"{request.json['edge_1'][0]} {request.json['edge_1'][1]}",
        edge_2=f"{request.json['edge_2'][0]} {request.json['edge_2'][1]}"
    )

    db.session.add(route)
    db.session.commit()

    return make_response(jsonify({'Response': 'Successful'}), 200)


@app.route('/route/<id>', methods=['GET'])
def get_route(id):
    id = int(id)
    if id > 0:
        route = db.session.query(Route).filter_by(id=id).first()

        result = {
            'id': route.id,
            'title': route.title,
            'description': route.description,
            'image': route.image,
            'edge_1': list(map(int, route.edge_1.split(' '))),
            'edge_2': list(map(int, route.edge_2.split(' ')))
        }
    else:
        routes = db.session.query(Route).all()

        result = {
            'routes': [{'id': m_route.id,
                        'title': m_route.title,
                        'description': m_route.description,
                        'image': m_route.image,
                        'edge_1': list(map(float, m_route.edge_1.split())),
                        'edge_2': list(map(float, m_route.edge_2.split()))} for m_route in routes]}

    return jsonify(result)


@app.route('/route/<id>', methods=['DELETE'])
def delete_route(id):
    id = int(id)
    db.session.query(Point).filter_by(route_id=id).delete()
    db.session.query(Route).filter_by(id=id).delete()

    db.session.commit()

    return make_response(jsonify({'Response': 'Successful'}), 200)


@app.route('/point', methods=['POST'])
def new_point():
    if not request.json:
        abort(400)

    if "points" in request.json:
        for m_point in request.json['points']:
            m_point = Point(
                title=m_point['title'],
                description=m_point['description'],
                image=m_point['image'],
                location=f"{m_point['location'][0]} {m_point['location'][1]}",
                route_id=request.json['route_id']
            )

            db.session.add(m_point)
            db.session.commit()
    else:
        point = Point(
            title=request.json['title'],
            description=request.json['description'],
            image=request.json['image'],
            location=f"{request.json['location'][0]} {request.json['location'][1]}",
            route_id=request.json['route_id']
        )

        db.session.add(point)
        db.session.commit()

    return make_response(jsonify({'Response': 'Successful'}), 200)


@app.route('/point/<id>', methods=['GET'])
def get_point(id):
    id = int(id)
    points = db.session.query(Point).filter_by(route_id=id).all()

    result = {
        'points': [{'id': m_point.id,
                    'title': m_point.title,
                    'description': m_point.description,
                    'image': m_point.image,
                    'location': list(map(float, m_point.location.split()))} for m_point in points]}

    return jsonify(result)


@app.route('/point/<id>', methods=['DELETE'])
def delete_point(id):
    id = int(id)
    db.session.query(Point).filter_by(id=id).delete()

    db.session.commit()

    return make_response(jsonify({'Response': 'Successful'}), 200)


@app.route('/event', methods=['POST'])
def new_event():
    if not request.json:
        abort(400)

    event = Event(title=request.json['title'],
                description=request.json['description'],
                image=request.json['image'],
                date=datetime(*request.json['date']))

    db.session.add(event)
    db.session.commit()

    return make_response(jsonify({'Response': 'Successful'}), 200)


@app.route('/event/<time>', methods=['GET'])
def get_events(time):
    if time.isdigit():
        time = int(time)
        event = db.session.query(Event).filter_by(id=time).first()

        result = {
            'id': event.id,
            'title': event.title,
            'description': event.description,
            'image': event.image,
            'date': event.date
        }
    else:
        if time == 'future':
            events = db.session.query(Event).filter(Event.date > datetime.now()).all()
        elif time == 'past':
            events = db.session.query(Event).filter(Event.date < datetime.now()).all()
        elif time == 'all':
            events = db.session.query(Event).all()
        elif len(time.split()) == 3:
            m_date = datetime(*list(map(int, time.split())))
            events = db.session.query(Event).filter(
                sqlalchemy.func.extract('year', Event.date) == m_date.year,
                sqlalchemy.func.extract('month', Event.date) == m_date.month,
                sqlalchemy.func.extract('day', Event.date) == m_date.day).all()
        else:
            abort(400)

        result = {'events': [{'id': event.id, 'title': event.title, 'description': event.description, 'date': event.date} for event in events]}

    return jsonify(result)


@app.route('/event/<id>', methods=['DELETE'])
def delete_event(id):
    id = int(id)
    db.session.query(Event).filter_by(id=id).delete()

    db.session.commit()

    return make_response(jsonify({'Response': 'Successful'}), 200)


if __name__ == '__main__':
    from models import *
    db.init_app(app)

    # with app.app_context():
    #     from models import *
    #
    #     db.create_all()

    app.run(debug=False)