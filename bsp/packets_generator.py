import random
import threading
from .database import db
from bsp.models.droneid_info import DroneIDInfo
from bsp.models.droneid_movement import DroneIDMovement
from bsp.models.remoteid_info import RemoteIDInfo
from bsp.models.remoteid_movement import RemoteIDMovement
from flask import current_app
import time

class packets_generator():
    flying_droneid_info = []
    flying_remoteid_info = []
    generating_new_packets = False

    BASE_LATITUDE = 54.352025
    BASE_LONGITUDE = 18.646638
    BASE_VARIANCE = 0.01

    GENERATION_FREQUENCY = 10
    NUMBER_OF_DRONES = 5

    def __init__(self):
        pass

    def start_generating_packets(self):
        self.generate_initial_drone_info()
        self.generating_new_packets = True
        threading.Thread(target=self.generate_packets_task, args=(current_app.app_context(), )).start() 

    def generate_packets_task(self, app_context):
        app_context.push()
        while self.generating_new_packets:
            self.generate_random_data_for_multiple_drones()
            time.sleep(self.GENERATION_FREQUENCY)


    def generate_initial_drone_info(self):
        for drone_id in range(1, self.NUMBER_OF_DRONES + 1):
            new_droneid_info = DroneIDInfo(
                serial_number=f"SN{random.randint(1, 101)}",
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
            db.session.commit() 
            
            self.flying_droneid_info.append(new_droneid_info)

            new_remoteid_info = RemoteIDInfo(
                serial_number=f"SN{random.randint(1, 101)}",
                height_type=random.choice([1, 2]),
                horiz_accuracy=random.randint(1, 3),
                vert_accuracy=random.randint(1, 3),
                baro_accuracy=random.randint(1, 3),
                speed_accuracy=random.randint(1, 3),
                ts_accuracy=random.randint(1, 3)
            )

            db.session.add(new_remoteid_info)
            db.session.commit() 

            self.flying_remoteid_info.append(new_remoteid_info)

        db.session.commit() 

    def random_coordinate(self, base, variance):
        return base + random.uniform(-variance, variance)

    def generate_random_data_for_multiple_drones(self):

        for remoteid_drones in self.flying_remoteid_info:

            new_remoteid_movement = RemoteIDMovement(
                drone_id=remoteid_drones.id,
                status=random.choice([0, 1]),
                timestamp=random.uniform(1234567890.0, 1234567890.0 + 10000),
                direction=random.uniform(0, 360),
                speed_horizontal=random.uniform(0, 20), 
                speed_vertical=random.uniform(-5, 5),  
                latitude=self.random_coordinate(self.BASE_LONGITUDE, self.BASE_VARIANCE),
                longitude=self.random_coordinate(self.BASE_LATITUDE, self.BASE_VARIANCE),
                altitude_baro=random.uniform(50, 200),   
                altitude_geo=random.uniform(45, 195),    
                height=random.uniform(0, 100)       
            )

            db.session.add(new_remoteid_movement)


        for droneid_drones in self.flying_droneid_info:

            new_droneid_movement = DroneIDMovement(
                drone_id=droneid_drones.id,
                timestamp=random.randint(1234567890, 1234567890 + 10000),
                pkt_len=random.randint(100, 500),
                longitude=self.random_coordinate(self.BASE_LONGITUDE, self.BASE_VARIANCE),
                latitude=self.random_coordinate(self.BASE_LATITUDE, self.BASE_VARIANCE),
                altitude=random.uniform(50, 200),
                height=random.uniform(0, 100),
                v_north=random.uniform(-10, 10),
                v_east=random.uniform(-10, 10),
                v_up=random.uniform(-5, 5),
                d_1_angle=random.uniform(0, 360),
                app_lat=self.random_coordinate(self.BASE_LATITUDE, self.BASE_VARIANCE),
                app_lon=self.random_coordinate(self.BASE_LONGITUDE, self.BASE_VARIANCE),
                longitude_home=self.random_coordinate(self.BASE_LONGITUDE, self.BASE_VARIANCE),
                latitude_home=self.random_coordinate(self.BASE_LATITUDE, self.BASE_VARIANCE)
            )

            db.session.add(new_droneid_movement)
            
        db.session.commit()

        return

global_generator = packets_generator()