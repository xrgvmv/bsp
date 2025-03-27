import datetime
from flask_sqlalchemy import SQLAlchemy
from dataclasses import dataclass
from ..database import db

@dataclass
class RemoteIDMovement(db.Model):
    __tablename__ = 'remoteid_movement'

    id: int = db.Column(db.Integer, primary_key=True)
    flight_id: int = db.Column(db.Integer, db.ForeignKey('remoteid_flight.id'), nullable=False)
    lng: float = db.Column(db.Float, nullable=True)
    lat: float = db.Column(db.Float, nullable=True)
    altitude: int = db.Column(db.Integer, nullable=True)
    height: int = db.Column(db.Integer, nullable=True)
    x_speed: float = db.Column(db.Float, nullable=True)
    y_speed: float = db.Column(db.Float, nullable=True)
    z_speed: float = db.Column(db.Float, nullable=True)
    pitch: float = db.Column(db.Float, nullable=True)
    roll: float = db.Column(db.Float, nullable=True)
    yaw: float = db.Column(db.Float, nullable=True)
    spoofed: bool = db.Column(db.Boolean, nullable=True)
    timestamp: datetime = db.Column(db.DateTime, nullable=True)  
