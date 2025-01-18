from flask_sqlalchemy import SQLAlchemy
from ..database import db

class RemoteIDMovement(db.Model):
    __tablename__ = 'remoteid_movement'

    id = db.Column(db.Integer, primary_key=True)
    drone_id = db.Column(db.Integer, db.ForeignKey('remoteid_info.id'), nullable=False)
    status = db.Column(db.SmallInteger, nullable=False)
    timestamp = db.Column(db.Float, nullable=False)
    direction = db.Column(db.Float, nullable=False)
    speed_horizontal = db.Column(db.Float, nullable=False)
    speed_vertical = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    altitude_baro = db.Column(db.Float, nullable=False)
    altitude_geo = db.Column(db.Float, nullable=False)
    height = db.Column(db.Float, nullable=False)

    def __init__(self, drone_id, status, timestamp, direction, speed_horizontal, speed_vertical, latitude, longitude, altitude_baro, altitude_geo, height):
        self.drone_id = drone_id
        self.status = status
        self.timestamp = timestamp
        self.direction = direction
        self.speed_horizontal = speed_horizontal
        self.speed_vertical = speed_vertical
        self.latitude = latitude
        self.longitude = longitude
        self.altitude_baro = altitude_baro
        self.altitude_geo = altitude_geo
        self.height = height
