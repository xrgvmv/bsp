from flask_sqlalchemy import SQLAlchemy
from ..database import db

class RemoteIDInfo(db.Model):
    __tablename__ = 'remoteid_info'

    id = db.Column(db.Integer, primary_key=True)
    height_type = db.Column(db.SmallInteger, nullable=False)
    horiz_accuracy = db.Column(db.SmallInteger, nullable=False)
    vert_accuracy = db.Column(db.SmallInteger, nullable=False)
    baro_accuracy = db.Column(db.SmallInteger, nullable=False)
    speed_accuracy = db.Column(db.SmallInteger, nullable=False)
    ts_accuracy = db.Column(db.SmallInteger, nullable=False)

    def __init__(self, height_type, horiz_accuracy, vert_accuracy, baro_accuracy, speed_accuracy, ts_accuracy):
        self.height_type = height_type
        self.horiz_accuracy = horiz_accuracy
        self.vert_accuracy = vert_accuracy
        self.baro_accuracy = baro_accuracy
        self.speed_accuracy = speed_accuracy
        self.ts_accuracy = ts_accuracy
