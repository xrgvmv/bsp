from flask_sqlalchemy import SQLAlchemy
from dataclasses import dataclass
from ..database import db

@dataclass
class RemoteIDMovement(db.Model):
    __tablename__ = 'remoteid_movement'

    id: int = db.Column(db.Integer, primary_key=True)
    drone_id: int = db.Column(db.Integer, db.ForeignKey('remoteid_info.id'), nullable=False)
    status: int = db.Column(db.SmallInteger, nullable=False)
    timestamp: float = db.Column(db.Float, nullable=False)
    direction: float = db.Column(db.Float, nullable=False)
    speed_horizontal: float = db.Column(db.Float, nullable=False)
    speed_vertical: float = db.Column(db.Float, nullable=False)
    latitude: float = db.Column(db.Float, nullable=False)
    longitude: float = db.Column(db.Float, nullable=False)
    altitude_baro: float = db.Column(db.Float, nullable=False)
    altitude_geo: float = db.Column(db.Float, nullable=False)
    height: float = db.Column(db.Float, nullable=False)
