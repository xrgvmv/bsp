from flask_sqlalchemy import SQLAlchemy
from dataclasses import dataclass
from ..database import db

@dataclass
class DroneIDMovement(db.Model):
    __tablename__ = 'droneid_movement'

    id: int = db.Column(db.Integer, primary_key=True)
    drone_id: int = db.Column(db.Integer, db.ForeignKey('droneid_info.id'), nullable=False)
    timestamp: int = db.Column(db.BigInteger, nullable=False)
    pkt_len: int = db.Column(db.SmallInteger, nullable=False)
    longitude: float = db.Column(db.Float, nullable=False)
    latitude: float = db.Column(db.Float, nullable=False)
    altitude: float = db.Column(db.Float, nullable=False)
    height: float = db.Column(db.Float, nullable=False)
    v_north: float = db.Column(db.Float, nullable=False)
    v_east: float = db.Column(db.Float, nullable=False)
    v_up: float = db.Column(db.Float, nullable=False)
    d_1_angle: float = db.Column(db.Float, nullable=False)
    app_lat: float = db.Column(db.Float, nullable=False)
    app_lon: float = db.Column(db.Float, nullable=False)
    longitude_home: float = db.Column(db.Float, nullable=False)
    latitude_home: float = db.Column(db.Float, nullable=False)
