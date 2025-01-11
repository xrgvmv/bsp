from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class DroneID(db.Model):
    __tablename__ = 'droneid'
    
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.BigInteger, nullable=False)
    pkt_len = db.Column(db.SmallInteger, nullable=False)
    unk = db.Column(db.SmallInteger, nullable=False)
    version = db.Column(db.SmallInteger, nullable=False)
    seq_number = db.Column(db.SmallInteger, nullable=False)
    state_info = db.Column(db.SmallInteger, nullable=False)
    serial_number = db.Column(db.String(16), nullable=False)
    longitude = db.Column(db.REAL, nullable=False)
    latitude = db.Column(db.REAL, nullable=False)
    altitude = db.Column(db.REAL, nullable=False)
    height = db.Column(db.REAL, nullable=False)
    v_north = db.Column(db.REAL, nullable=False)
    v_east = db.Column(db.REAL, nullable=False)
    v_up = db.Column(db.REAL, nullable=False)
    d_1_angle = db.Column(db.REAL, nullable=False)
    app_lat = db.Column(db.REAL, nullable=False)
    app_lon = db.Column(db.REAL, nullable=False)
    longitude_home = db.Column(db.REAL, nullable=False)
    latitude_home = db.Column(db.REAL, nullable=False)
    device_type_id = db.Column(db.SmallInteger, nullable=False)
    device_type = db.Column(db.String(16), nullable=False)
    uuid_len = db.Column(db.SmallInteger, nullable=False)
    uuid = db.Column(db.String(18))
    crc = db.Column(db.SmallInteger, nullable=False)

    def __init__(self, timestamp, pkt_len, unk, version, seq_number, state_info, serial_number, longitude, latitude, altitude, height, v_north, v_east, v_up, d_1_angle, app_lat, app_lon, longitude_home, latitude_home, device_type_id, device_type, uuid_len, uuid, crc):
        self.timestamp = timestamp
        self.pkt_len = pkt_len
        self.unk = unk
        self.version = version
        self.seq_number = seq_number
        self.state_info = state_info
        self.serial_number = serial_number
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
        self.device_type_id = device_type_id
        self.device_type = device_type
        self.uuid_len = uuid_len
        self.uuid = uuid
        self.crc = crc


