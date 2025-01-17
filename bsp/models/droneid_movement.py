from flask_sqlalchemy import SQLAlchemy
from ..database import db

class DroneIDMovement(db.Model):
    __tablename__ = 'droneid_movement'

    id = db.Column(db.Integer, primary_key=True)
    drone_id = db.Column(db.Integer, db.ForeignKey('droneid_info.id'), nullable=False)
    timestamp = db.Column(db.BigInteger, nullable=False)
    pkt_len = db.Column(db.SmallInteger, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    altitude = db.Column(db.Float, nullable=False)
    height = db.Column(db.Float, nullable=False)
    v_north = db.Column(db.Float, nullable=False)
    v_east = db.Column(db.Float, nullable=False)
    v_up = db.Column(db.Float, nullable=False)
    d_1_angle = db.Column(db.Float, nullable=False)
    app_lat = db.Column(db.Float, nullable=False)
    app_lon = db.Column(db.Float, nullable=False)
    longitude_home = db.Column(db.Float, nullable=False)
    latitude_home = db.Column(db.Float, nullable=False)

    def __init__(self, drone_id, timestamp, pkt_len, longitude, latitude, altitude, height, v_north, v_east, v_up, d_1_angle, app_lat, app_lon, longitude_home, latitude_home):
        self.drone_id = drone_id
        self.timestamp = timestamp
        self.pkt_len = pkt_len
        self.longitude = longitude
        self.latitude = latitude
        self.altitude = altitude
        self.height = height
        self.v_north = v_north
        self.v_east = v_east
        self.v_up = v_up
        self.d_1_angle = d_1_angle
        self.app_lat = app_lat
        self.app_lon = app_lon
        self.longitude_home = longitude_home
        self.latitude_home = latitude_home