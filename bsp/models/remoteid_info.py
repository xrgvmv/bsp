import datetime
from flask_sqlalchemy import SQLAlchemy
from dataclasses import dataclass
from ..database import db

    #Source : https://github.com/cyber-defence-campus/RemoteIDReceiver/blob/main/Receiver/backend/dronesniffer/models/daomodels.py

    # Attributes:
    #     id (int, optional): ID associated with the packet given by the database.
    #     oui (str): Oui of the Manufacturer.
    #     serial_number (str, optional): Serial number of the drone.
    #     timestamp (datetime, optional): Time packets has been sent.
    #     lng (float, optional): Longitude of drone. Value between -180 and 180.
    #     lat (float, optional): Latitude of drone. Value between -90 and 90.
    #     altitude (float, optional): Altitude of drone (meter above sea level)
    #     height (float, optional): Height above ground of drone.
    #     x_speed(float, optional): Speed of drone in direction x.
    #     y_speed(float, optional): Speed of drone in direction y.
    #     z_speed(float, optional): Speed of drone in direction z.
    #     yaw(float, optional): Yaw angle of drone.
    #     pilot_lng (float, optional): Longitude of pilot. Value between -180 and 180.
    #     pilot_lat (float, optional): Latitude of pilot. Value between -90 and 90.
    #     home_lng (float, optional): Longitude of home (drone starting point). Value between -180 and 180.
    #     home_lat (float, optional): Latitude of home (drone starting point). Value between -90 and 90.
    #     uuid (str): User unique identifier as 20-digit string.
    #     spoofed (bool): Assumption that RID is spoofed.

    #We assume that data added to our database is already converted (for example longitude is already a float)
    #We only save useful data information and ommit matadata (no crc) 

@dataclass
class RemoteIDInfo(db.Model):
    __tablename__ = 'remoteid_info'

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

    oui: str = db.Column(db.String(20), nullable=True)
    serial_number: str = db.Column(db.String(20), nullable=False)
    uuid: str = db.Column(db.String(20), nullable=False)
