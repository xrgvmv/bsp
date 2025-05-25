from flask_sqlalchemy import SQLAlchemy
from dataclasses import dataclass
from ..database import db


#Full DJI DroneID packed type 2

#1 00000000 len_pack byte
#1 00000001 zero_byte byte
#1 00000002 version byte
#2 00000003 sequence_num unsigned short
#2 00000005 state_info unsigned short
#16 00000007 serial_num char[16]
#4 00000017 longitude int
#4 0000001b latitude int
#2 0000001f altitude short
#2 00000021 height short
#2 00000023 v_north short
#2 00000025 v_east short
#2 00000027 v_up short
#2 00000029 yaw short
#8 0000002b gps_time unsigned long long
#4 00000033 rc_latitude int
#4 00000037 rc_longitude int
#4 0000003b home_longitude int
#4 0000003f home_latitude int
#1 00000043 device_type byte
#1 00000044 uuid_len byte
#20 00000045 uuid char[20]
#2 00000059 crc unsigned short

#We assume that data added to our database is already converted (for example longitude is already a float)
#We only save useful data information and ommit matadata (for example uuid_len) 

@dataclass
class DroneIDInfo(db.Model):
    __tablename__ = 'droneid_info'

    id: int = db.Column(db.Integer, primary_key=True)
    
    #version: int = db.Column(db.SmallInteger, nullable=True)
    serial_number: str = db.Column(db.String(16), nullable=False)
    device_type: int = db.Column(db.SmallInteger, nullable=True)
    #uuid_len: int = db.Column(db.SmallInteger, nullable=True)
    uuid: str = db.Column(db.String(20), nullable=False)

   

