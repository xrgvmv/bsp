from flask_sqlalchemy import SQLAlchemy
from dataclasses import dataclass
from ..database import db

@dataclass
class RemoteIDInfo(db.Model):
    __tablename__ = 'remoteid_info'

    serial_number: str = db.Column(db.String(16), nullable=False) # temporary solution, not real field
    id: int = db.Column(db.Integer, primary_key=True)
    height_type: int = db.Column(db.SmallInteger, nullable=False)
    horiz_accuracy: int = db.Column(db.SmallInteger, nullable=False)
    vert_accuracy: int = db.Column(db.SmallInteger, nullable=False)
    baro_accuracy: int = db.Column(db.SmallInteger, nullable=False)
    speed_accuracy: int = db.Column(db.SmallInteger, nullable=False)
    ts_accuracy: int = db.Column(db.SmallInteger, nullable=False)
