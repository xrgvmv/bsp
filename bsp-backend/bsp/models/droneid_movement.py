import datetime
from flask_sqlalchemy import SQLAlchemy
from dataclasses import dataclass
from ..database import db

@dataclass
class DroneIDMovement(db.Model):
    __tablename__ = 'droneid_movement'

    id: int = db.Column(db.Integer, primary_key=True)
    droneid_info_id: int = db.Column(db.Integer, db.ForeignKey('droneid_info.id'), nullable=False) #not necessery but makes queries easier
    droneid_flight_id: int = db.Column(db.Integer, db.ForeignKey('droneid_flight.id'), nullable=False)

    #len_pack: int = db.Column(db.SmallInteger, nullable=True)
    #zero_byte: int = db.Column(db.SmallInteger, nullable=True)
    #sequence_num: int = db.Column(db.SmallInteger, nullable=True)
    state_info: int = db.Column(db.SmallInteger, nullable=True)
    latitude: int = db.Column(db.Float, nullable=False)
    longitude: int = db.Column(db.Float, nullable=False)
    altitude: int = db.Column(db.Float, nullable=False)
    height: int = db.Column(db.Float, nullable=False)
    v_north: int = db.Column(db.Float, nullable=False)
    v_east: int = db.Column(db.Float, nullable=False)
    v_up: int = db.Column(db.Float, nullable=False)
    yaw: int = db.Column(db.Float, nullable=False)
    gps_time: datetime = db.Column(db.DateTime(timezone=True), nullable=False)
    #crc: str = db.Column(db.SmallInteger, nullable=True)
    rc_latitude: int = db.Column(db.Float, nullable=True)
    rc_longitude: int = db.Column(db.Float, nullable=True)
