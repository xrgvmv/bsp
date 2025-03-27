from flask_sqlalchemy import SQLAlchemy
from dataclasses import dataclass
from ..database import db

@dataclass
class DroneIDFlight(db.Model):
    __tablename__ = 'droneid_flight'

    id: int = db.Column(db.Integer, primary_key=True)
    drone_id: int = db.Column(db.Integer, db.ForeignKey('droneid_info.id'), nullable=False)
 
    rc_latitude: int = db.Column(db.Float, nullable=True)
    rc_longitude: int = db.Column(db.Float, nullable=True)
    home_longitude: int = db.Column(db.Float, nullable=True)
    home_latitude: int = db.Column(db.Float, nullable=True)