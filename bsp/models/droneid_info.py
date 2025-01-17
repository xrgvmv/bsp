from flask_sqlalchemy import SQLAlchemy
from ..database import db

class DroneIDInfo(db.Model):
    __tablename__ = 'droneid_info'

    id = db.Column(db.Integer, primary_key=True)
    serial_number = db.Column(db.String(16), nullable=False)
    device_type_id = db.Column(db.SmallInteger, nullable=False)
    device_type = db.Column(db.String(16), nullable=False)
    uuid_len = db.Column(db.SmallInteger, nullable=False)
    uuid = db.Column(db.String(18))
    crc = db.Column(db.SmallInteger, nullable=False)
    unk = db.Column(db.SmallInteger, nullable=False)  
    version = db.Column(db.SmallInteger, nullable=False)  
    seq_number = db.Column(db.SmallInteger, nullable=False) 
    state_info = db.Column(db.SmallInteger, nullable=False) 

    def __init__(self, serial_number, device_type_id, device_type, uuid_len, uuid, crc, unk, version, seq_number, state_info):
        self.serial_number = serial_number
        self.device_type_id = device_type_id
        self.device_type = device_type
        self.uuid_len = uuid_len
        self.uuid = uuid
        self.crc = crc
        self.unk = unk
        self.version = version
        self.seq_number = seq_number
        self.state_info = state_info
