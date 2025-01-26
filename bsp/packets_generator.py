import random
import threading
import time
from enum import Enum
from .database import db
from bsp.models.droneid_info import DroneIDInfo
from bsp.models.droneid_movement import DroneIDMovement
from bsp.models.remoteid_info import RemoteIDInfo
from bsp.models.remoteid_movement import RemoteIDMovement
from flask import current_app

class PacketType(Enum):
    remoteid = 1
    droneid = 2

class drone_generation_info(): 
    def __init__(self, packetType: PacketType, start_x_position, start_y_position, info_id):
        self.packetType = packetType
        self.info_id = info_id #id of droneid_info or remoteid_info
        self.start_x_position = start_x_position
        self.start_y_position = start_y_position
        self.x_position = start_x_position
        self.y_position = start_y_position
        self.x_velocity = 0
        self.y_velocity = 0
        self.x_acceleration = 0
        self.y_acceleration = 0


class packets_generator():
    drone_generation_infos = []
    generating_new_packets = False
    last_acceleration_update = 0

    BASE_LATITUDE = 54.352025 # in degress
    BASE_LONGITUDE = 18.646638 # in degress
    BASE_VARIANCE = 0.01 # in degress
    ACCELERATION_CHANGE_MAX = 0.01 # degress / s^2
    CENTER_ATTRACTION = 0.1 # in [degress / s^2] / degress
    GENERATION_PERIOD = 1 # in seconds
    NUMBER_OF_DRONES = 5 # per protocol
    ACCELERATION_UPDATE_PERIOD = 5 # in seconds


    def __init__(self):
        print("created generator")
        pass

    def start_generating_packets():
        if not packets_generator.generating_new_packets:
            print("starting generating")
            packets_generator.generate_initial_drone_info()
            packets_generator.generating_new_packets = True
            threading.Thread(target=packets_generator.generate_packets_task, args=(current_app.app_context(), )).start() 

    def generate_packets_task(app_context):
        app_context.push()
        while packets_generator.generating_new_packets:
            packets_generator.generate_random_data_for_multiple_drones()
            time.sleep(packets_generator.GENERATION_PERIOD)


    def generate_initial_drone_info():
        
        flying_droneid_info = []
        flying_remoteid_info = []

        for drone_id in range(packets_generator.NUMBER_OF_DRONES):
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
            
            flying_droneid_info.append(new_droneid_info)

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

            flying_remoteid_info.append(new_remoteid_info)

        db.session.commit() 

        for i in range(packets_generator.NUMBER_OF_DRONES):
            packets_generator.drone_generation_infos.append(drone_generation_info(PacketType.droneid, packets_generator.BASE_LATITUDE + packets_generator.random_variance(), packets_generator.BASE_LONGITUDE + packets_generator.random_variance(), flying_droneid_info[i].id))
            packets_generator.drone_generation_infos.append(drone_generation_info(PacketType.remoteid, packets_generator.BASE_LATITUDE + packets_generator.random_variance(), packets_generator.BASE_LONGITUDE + packets_generator.random_variance(), flying_remoteid_info[i].id))


    def random_variance():
        return random.uniform(-packets_generator.BASE_VARIANCE, packets_generator.BASE_VARIANCE)


    def update_drone_generation_info():
        if packets_generator.last_acceleration_update is None or time.time() > packets_generator.last_acceleration_update + packets_generator.ACCELERATION_UPDATE_PERIOD:
            packets_generator.last_acceleration_update = time.time()
            for drone_generation_info in packets_generator.drone_generation_infos: 
                drone_generation_info.x_acceleration += random.uniform(-packets_generator.ACCELERATION_CHANGE_MAX, packets_generator.ACCELERATION_CHANGE_MAX)
                drone_generation_info.x_acceleration += (drone_generation_info.start_x_position - drone_generation_info.x_position) \
                    * packets_generator.CENTER_ATTRACTION
                drone_generation_info.y_acceleration += random.uniform(-packets_generator.ACCELERATION_CHANGE_MAX, packets_generator.ACCELERATION_CHANGE_MAX)
                drone_generation_info.y_acceleration += (drone_generation_info.start_y_position - drone_generation_info.y_position) \
                    * packets_generator.CENTER_ATTRACTION

        for drone_generation_info in packets_generator.drone_generation_infos: 
            drone_generation_info.x_velocity += drone_generation_info.x_acceleration * packets_generator.GENERATION_PERIOD
            drone_generation_info.y_velocity += drone_generation_info.y_acceleration * packets_generator.GENERATION_PERIOD

            drone_generation_info.x_position += drone_generation_info.x_velocity * packets_generator.GENERATION_PERIOD
            drone_generation_info.y_position += drone_generation_info.y_velocity * packets_generator.GENERATION_PERIOD


    def generate_random_data_for_multiple_drones():

        packets_generator.update_drone_generation_info()

        for drone_generation_info in packets_generator.drone_generation_infos:
            if drone_generation_info.packetType == PacketType.remoteid:
                new_remoteid_movement = RemoteIDMovement(
                    drone_id=drone_generation_info.info_id,
                    status=random.choice([0, 1]),
                    timestamp=random.uniform(1234567890.0, 1234567890.0 + 10000),
                    direction=random.uniform(0, 360),
                    speed_horizontal=random.uniform(0, 20), 
                    speed_vertical=random.uniform(-5, 5),  
                    latitude=drone_generation_info.y_position,
                    longitude=drone_generation_info.x_position,
                    altitude_baro=random.uniform(50, 200),   
                    altitude_geo=random.uniform(45, 195),    
                    height=random.uniform(0, 100)       
                )

                db.session.add(new_remoteid_movement)

            else:
                new_droneid_movement = DroneIDMovement(
                    drone_id=drone_generation_info.info_id,
                    timestamp=random.randint(1234567890, 1234567890 + 10000),
                    pkt_len=random.randint(100, 500),
                    latitude=drone_generation_info.y_position,
                    longitude=drone_generation_info.x_position,
                    altitude=random.uniform(50, 200),
                    height=random.uniform(0, 100),
                    v_north=random.uniform(-10, 10),
                    v_east=random.uniform(-10, 10),
                    v_up=random.uniform(-5, 5),
                    d_1_angle=random.uniform(0, 360),
                    app_lat= drone_generation_info.y_position,
                    app_lon= drone_generation_info.x_position,
                    longitude_home=drone_generation_info.start_y_position,
                    latitude_home=drone_generation_info.start_x_position
                )

                db.session.add(new_droneid_movement)
            
        db.session.commit()
        return
    
    def get_flying_droneid_info_ids():
        ids = []
        for drone_generation_info in packets_generator.drone_generation_infos:
            if drone_generation_info.packetType == PacketType.droneid:
                ids.append(drone_generation_info.info_id)

        return ids

    def get_flying_remoteid_info_ids():
        ids = []
        for drone_generation_info in packets_generator.drone_generation_infos:
            if drone_generation_info.packetType == PacketType.remoteid:
                ids.append(drone_generation_info.info_id)

        return ids
