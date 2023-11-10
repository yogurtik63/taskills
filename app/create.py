from app import app, db

with app.app_context():
    db.init_app(app)

    from models import *
    db.create_all()