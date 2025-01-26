from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .routes import main
from .database import db

def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@db:5432/bsp'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    
    with app.app_context():
        db.create_all()
        
    from bsp.models.droneid_info import DroneIDInfo
    from bsp.models.droneid_movement import DroneIDMovement
    from bsp.models.remoteid_info import RemoteIDInfo
    from bsp.models.remoteid_movement import RemoteIDMovement

    app.register_blueprint(main)

    return app
 