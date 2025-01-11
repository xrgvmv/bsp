from .database import db
from bsp.models.remoteid import RemoteID
from bsp.models.droneid import DroneID

def add_data_to_db():
    new_remoteid = RemoteID(
        status=1,
        direction=45.0,
        speed_horizontal=12.5,
        speed_vertical=1.2,
        latitude=52.2296756,
        longitude=21.0122287,
        altitude_baro=100.5,
        altitude_geo=98.3,
        height_type=2,
        height=50.0,
        horiz_accuracy=1,
        vert_accuracy=1,
        baro_accuracy=1,
        speed_accuracy=1,
        ts_accuracy=1,
        timestamp=1234567890.0
    )

    db.session.add(new_remoteid)
    db.session.commit()
    return