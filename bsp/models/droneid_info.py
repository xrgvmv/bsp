from flask_sqlalchemy import SQLAlchemy
from dataclasses import dataclass
from ..database import db

@dataclass
class DroneIDInfo(db.Model):
    __tablename__ = 'droneid_info'

    id: int = db.Column(db.Integer, primary_key=True)
    serial_number: str = db.Column(db.String(16), nullable=False)
    device_type_id: int = db.Column(db.SmallInteger, nullable=False)
    device_type: str = db.Column(db.String(16), nullable=False)
    uuid_len: int = db.Column(db.SmallInteger, nullable=False)
    uuid: str = db.Column(db.String(18))
    crc: int = db.Column(db.SmallInteger, nullable=False)
    unk: int = db.Column(db.SmallInteger, nullable=False)  
    version: int = db.Column(db.SmallInteger, nullable=False)  
    seq_number: int = db.Column(db.SmallInteger, nullable=False) 
    state_info: int = db.Column(db.SmallInteger, nullable=False)
