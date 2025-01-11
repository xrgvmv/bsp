from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class RemoteID(db.Model):
    __tablename__ = 'remoteid'

    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.SmallInteger, nullable=False)
    direction = db.Column(db.REAL, nullable=False)
    speed_horizontal = db.Column(db.REAL, nullable=False)
    speed_vertical = db.Column(db.REAL, nullable=False)
    latitude = db.Column(db.DECIMAL, nullable=False)
    longitude = db.Column(db.DECIMAL, nullable=False)
    altitude_baro = db.Column(db.REAL, nullable=False)
    altitude_geo = db.Column(db.REAL, nullable=False)
    height_type = db.Column(db.SmallInteger, nullable=False)
    height = db.Column(db.REAL, nullable=False)
    horiz_accuracy = db.Column(db.SmallInteger, nullable=False)
    vert_accuracy = db.Column(db.SmallInteger, nullable=False)
    baro_accuracy = db.Column(db.SmallInteger, nullable=False)
    speed_accuracy = db.Column(db.SmallInteger, nullable=False)
    ts_accuracy = db.Column(db.SmallInteger, nullable=False)
    timestamp = db.Column(db.REAL, nullable=False)

    def __init__(self, status, direction, speed_horizontal, speed_vertical, latitude, longitude, altitude_baro, altitude_geo, height_type, height, horiz_accuracy, vert_accuracy, baro_accuracy, speed_accuracy, ts_accuracy, timestamp):
        self.status = status
        self.direction = direction
        self.speed_horizontal = speed_horizontal
        self.speed_vertical = speed_vertical
        self.latitude = latitude
        self.longitude = longitude
        self.altitude_baro = altitude_baro
        self.altitude_geo = altitude_geo
        self.height_type = height_type
        self.height = height
        self.horiz_accuracy = horiz_accuracy
        self.vert_accuracy = vert_accuracy
        self.baro_accuracy = baro_accuracy
        self.speed_accuracy = speed_accuracy
        self.ts_accuracy = ts_accuracy
        self.timestamp = timestamp
