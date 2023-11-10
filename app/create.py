from app import app, db

with app.app_context():
    from models import *
    db.create_all()