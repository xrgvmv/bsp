import random
import asyncio
from .database import db
from bsp.models.droneid_info import DroneIDInfo
from bsp.models.droneid_movement import DroneIDMovement
from bsp.models.remoteid_info import RemoteIDInfo
from bsp.models.remoteid_movement import RemoteIDMovement

def generate_initial_drone_info():
    base_latitude = 54.352025
    base_longitude = 18.646638

    for drone_id in range(1, 6):
        new_droneid_info = DroneIDInfo(
            serial_number=f"SN{drone_id}",
            device_type_id=random.randint(1, 5),
            device_type="UAV",
            uuid_len=18,
            uuid=f"UUID-{drone_id}",
            crc=random.randint(1000, 9999),
            unk=random.randint(0, 10),
            version=random.randint(1, 5),
            seq_number=random.randint(1, 100),
            state_info=random.randint(1, 5)
        )

        db.session.add(new_droneid_info)

        new_remoteid_info = RemoteIDInfo(
            height_type=random.choice([1, 2]),
            horiz_accuracy=random.randint(1, 3),
            vert_accuracy=random.randint(1, 3),
            baro_accuracy=random.randint(1, 3),
            speed_accuracy=random.randint(1, 3),
            ts_accuracy=random.randint(1, 3)
        )

        db.session.add(new_remoteid_info)

    db.session.commit()

def random_coordinate(base, variance):
    return base + random.uniform(-variance, variance)

def generate_random_data_for_multiple_drones():
    base_latitude = 54.352025
    base_longitude = 18.646638

    for drones in range(1, 6):

        new_remoteid_movement = RemoteIDMovement(
            drone_id=drones,
            status=random.choice([0, 1]),
            timestamp=random.uniform(1234567890.0, 1234567890.0 + 10000),
            direction=random.uniform(0, 360),
            speed_horizontal=random.uniform(0, 20), 
            speed_vertical=random.uniform(-5, 5),  
            latitude=random_coordinate(base_latitude, 0.01),
            longitude=random_coordinate(base_longitude, 0.01),
            altitude_baro=random.uniform(50, 200),   
            altitude_geo=random.uniform(45, 195),    
            height=random.uniform(0, 100)       
        )

        db.session.add(new_remoteid_movement)

        new_droneid_movement = DroneIDMovement(
            drone_id=drones,
            timestamp=random.randint(1234567890, 1234567890 + 10000),
            pkt_len=random.randint(100, 500),
            longitude=random_coordinate(base_longitude, 0.01),
            latitude=random_coordinate(base_latitude, 0.01),
            altitude=random.uniform(50, 200),
            height=random.uniform(0, 100),
            v_north=random.uniform(-10, 10),
            v_east=random.uniform(-10, 10),
            v_up=random.uniform(-5, 5),
            d_1_angle=random.uniform(0, 360),
            app_lat=random_coordinate(base_latitude, 0.01),
            app_lon=random_coordinate(base_longitude, 0.01),
            longitude_home=random_coordinate(base_longitude, 0.01),
            latitude_home=random_coordinate(base_latitude, 0.01)
        )

        db.session.add(new_droneid_movement)
        
    db.session.commit()

    return

def start_periodic_task():
    from run import app
    from bsp.task import periodic_task

    with app.app_context():
        generate_initial_drone_info()
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(periodic_task())