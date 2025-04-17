import datetime
import random
import threading
import time
import math
from enum import Enum
from bsp.models.remoteid_movement import RemoteIDMovement
from .database import db
from .cooridinate_converter import shifted_coords
from bsp.models.droneid_info import DroneIDInfo
from bsp.models.droneid_movement import DroneIDMovement
from bsp.models.droneid_flight import DroneIDFlight
from bsp.models.remoteid_info import RemoteIDInfo
from bsp.models.remoteid_flight import RemoteIDFlight
from flask import current_app

class PacketType(Enum):
    remoteid = 1
    droneid = 2

class drone_generation_info(): 
    def __init__(self, packetType: PacketType, start_x_position, start_y_position, max_height, max_vertical_speed, flight_id, info_id):
        self.packetType = packetType
        self.info_id = info_id #id of droneid_info or remoteid_info
        self.flight_id = flight_id
        self.start_x_position = start_x_position
        self.start_y_position = start_y_position
        self.x_position = start_x_position
        self.y_position = start_y_position
        self.x_velocity = 0
        self.y_velocity = 0

        self.max_height = max_height
        self.vertical_speed = max_vertical_speed
        self.height = 0


class packets_generator():
    drone_generation_infos: list[drone_generation_info] = []
    generating_new_packets = False

    BASE_LATITUDE = 54.352025 # in degress
    BASE_LONGITUDE = 18.646638 # in degress
    BASE_START_VARIANCE = 2000 # in m

    BASE_MAX_HEIGHT = 30 # in m
    BASE_MAX_HEIGHT_VARICANE = 10 # in m
    BASE_VERTICAL_SPEED = 3 # in m
    BASE_VERTICAL_SPEED_VARICANE = 1 # in m
    
    BASE_VARIANCE_YAW = 2 # degrees
    BASE_VARIANCE_ROLL = 2 # degrees
    BASE_VARIANCE_PITCH = 2 # degrees
    MAX_PITCH = 20 # degrees
    PITCH_DEGREES_PER_M_S = 0.5 # degrees per m/s


    GENERATION_PERIOD = 1 # in seconds
    SPEED_CHANGE_BIAS = 0.2 # m per seconds
    MAX_SPEED = 20 # m per seconds
    SPEED_CHANGE_TIME = 2 # in seconds
    NUMBER_OF_DRONES = 4 # per protocol
    MAX_SPEED_CHANGE = 3 # m per seconds
    last_acceleration_update = None
    

    def __init__(self):
        pass

    # It only generates new droneid_info/remoteid_info when nothis is in database
    # In other situations it only adds new flights to exitsting droneid_info/remoteid_info   
    def start_generating_packets():
        if not packets_generator.generating_new_packets:
            
            #First we search for exisitng drones in our db
            [droneid_info_ids, remoteid_info_ids] = packets_generator.get_drone_infos_ids_from_db() 

            #If we don't have enough of them, we create now droneid_infos/remoteid_infos
            if len(droneid_info_ids) < packets_generator.NUMBER_OF_DRONES or len(remoteid_info_ids) < packets_generator.NUMBER_OF_DRONES:
               [droneid_info_ids, remoteid_info_ids] = packets_generator.generate_initial_drone_info()

            #For existing drones we create new flights 
            [new_droneid_flights, new_remoteid_flights] = packets_generator.generate_new_flights(droneid_info_ids, remoteid_info_ids)
            
            packets_generator.generate_drone_generation_infos(new_droneid_flights, new_remoteid_flights)

            packets_generator.generating_new_packets = True
            threading.Thread(target=packets_generator.generate_packets_task, args=(current_app.app_context(), )).start() 


    def generate_packets_task(app_context):
        app_context.push()
        while packets_generator.generating_new_packets:
            packets_generator.generate_random_data_for_multiple_drones()
            time.sleep(packets_generator.GENERATION_PERIOD)


    def generate_drone_generation_infos(new_droneid_flights: list[DroneIDFlight], new_remoteid_flights: list[RemoteIDFlight]):
        
        for i in range(packets_generator.NUMBER_OF_DRONES):
            max_drone_height = packets_generator.BASE_MAX_HEIGHT + random.uniform(-packets_generator.BASE_MAX_HEIGHT_VARICANE, packets_generator.BASE_MAX_HEIGHT_VARICANE)
            drone_vertical_speed = packets_generator.BASE_VERTICAL_SPEED + random.uniform(-packets_generator.BASE_VERTICAL_SPEED_VARICANE, packets_generator.BASE_VERTICAL_SPEED_VARICANE)
            packets_generator.drone_generation_infos.append(drone_generation_info(PacketType.droneid, new_droneid_flights[i].home_latitude, new_droneid_flights[i].home_longitude, max_drone_height, drone_vertical_speed, new_droneid_flights[i].id, new_droneid_flights[i].droneid_info_id))
            
            max_drone_height = packets_generator.BASE_MAX_HEIGHT + random.uniform(-packets_generator.BASE_MAX_HEIGHT_VARICANE, packets_generator.BASE_MAX_HEIGHT_VARICANE)
            drone_vertical_speed = packets_generator.BASE_VERTICAL_SPEED + random.uniform(-packets_generator.BASE_VERTICAL_SPEED_VARICANE, packets_generator.BASE_VERTICAL_SPEED_VARICANE)
            packets_generator.drone_generation_infos.append(drone_generation_info(PacketType.remoteid, new_remoteid_flights[i].home_lat, new_remoteid_flights[i].home_lng, max_drone_height, drone_vertical_speed, new_remoteid_flights[i].id, new_remoteid_flights[i].remoteid_info_id))
            


    def generate_new_flights(droneid_info_ids: list, remoteid_info_ids: list):
        
        new_droneid_flights = []
        new_remoteid_flights = []

        for i in range(packets_generator.NUMBER_OF_DRONES):
            new_home_latitude, new_home_longititude = shifted_coords(packets_generator.BASE_LATITUDE, packets_generator.BASE_LONGITUDE, packets_generator.random_distance(), packets_generator.random_distance())
            new_remoteid_flight = RemoteIDFlight(
                remoteid_info_id = remoteid_info_ids[i],
                home_lat = new_home_latitude,
                home_lng = new_home_longititude
            )
            db.session.add(new_remoteid_flight)
            new_remoteid_flights.append(new_remoteid_flight)


            new_home_latitude, new_home_longititude = shifted_coords(packets_generator.BASE_LATITUDE, packets_generator.BASE_LONGITUDE, packets_generator.random_distance(), packets_generator.random_distance())
            new_droneid_flight = DroneIDFlight(
                droneid_info_id = droneid_info_ids[i],
                home_latitude = new_home_latitude,
                home_longitude = new_home_longititude
            )
            db.session.add(new_droneid_flight)
            new_droneid_flights.append(new_droneid_flight)

        db.session.commit() 

        return [new_droneid_flights, new_remoteid_flights]



    def get_drone_infos_ids_from_db():
        remoteid_info_ids = [id[0] for id in (
            RemoteIDInfo.query.order_by(RemoteIDInfo.id.desc())
            .limit(packets_generator.NUMBER_OF_DRONES)
            .with_entities(RemoteIDInfo.id)
            .all()
        ) ]
        droneid_info_ids = [id[0] for id in (
            DroneIDInfo.query.order_by(DroneIDInfo.id.desc())
            .limit(packets_generator.NUMBER_OF_DRONES)
            .with_entities(DroneIDInfo.id)
            .all()
        ) ]

        return [droneid_info_ids, remoteid_info_ids]

    def generate_serial_number(lenght):
        serial_number = [''] * lenght
        for i in range(lenght):
            rand_int = random.randint(0, 35)
            if rand_int > 9:
                serial_number[i] = chr(rand_int + 65 - 11)
            else: 
                serial_number[i] = chr(rand_int + 48)
        return ''.join(serial_number)
   
    def generate_initial_drone_info():
        
        flying_droneid_info = []
        flying_remoteid_info = []

        for drone_id in range(packets_generator.NUMBER_OF_DRONES):
            new_remoteid_info = RemoteIDInfo(
                serial_number=packets_generator.generate_serial_number(16),
                oui=packets_generator.generate_serial_number(18),
                uuid=packets_generator.generate_serial_number(18),
            )
            db.session.add(new_remoteid_info)
            flying_remoteid_info.append(new_remoteid_info)

            new_droneid_info = DroneIDInfo(
                serial_number=packets_generator.generate_serial_number(16),
                device_type = 19603,
                uuid=packets_generator.generate_serial_number(18),
            )
            db.session.add(new_droneid_info)
            flying_droneid_info.append(new_remoteid_info)

        db.session.commit() 

        return [[droneid_info.id for droneid_info in flying_droneid_info], [remoteid_info.id for remoteid_info in flying_remoteid_info]]


    def random_distance():
        return random.uniform(-packets_generator.BASE_START_VARIANCE, packets_generator.BASE_START_VARIANCE)


    def update_drone_generation_info():
        if packets_generator.last_acceleration_update is None or time.time() > packets_generator.last_acceleration_update + packets_generator.SPEED_CHANGE_TIME:
            packets_generator.last_acceleration_update = time.time()
            for drone_generation_info in packets_generator.drone_generation_infos: 
                drone_generation_info.x_velocity += random.uniform(-packets_generator.MAX_SPEED_CHANGE, packets_generator.MAX_SPEED_CHANGE)
                drone_generation_info.y_velocity += random.uniform(-packets_generator.MAX_SPEED_CHANGE, packets_generator.MAX_SPEED_CHANGE)

                drone_generation_info.x_velocity += -packets_generator.SPEED_CHANGE_BIAS if drone_generation_info.x_position > drone_generation_info.start_x_position else packets_generator.SPEED_CHANGE_BIAS
                drone_generation_info.y_velocity += -packets_generator.SPEED_CHANGE_BIAS if drone_generation_info.y_position > drone_generation_info.start_y_position else packets_generator.SPEED_CHANGE_BIAS
                
                if drone_generation_info.x_velocity > packets_generator.MAX_SPEED:
                    drone_generation_info.x_velocity = packets_generator.MAX_SPEED
                elif drone_generation_info.x_velocity < -packets_generator.MAX_SPEED:
                    drone_generation_info.x_velocity = -packets_generator.MAX_SPEED

                if drone_generation_info.y_velocity > packets_generator.MAX_SPEED:
                    drone_generation_info.y_velocity = packets_generator.MAX_SPEED
                elif drone_generation_info.y_velocity < -packets_generator.MAX_SPEED:
                    drone_generation_info.y_velocity = -packets_generator.MAX_SPEED

        for drone_generation_info in packets_generator.drone_generation_infos: 
            drone_generation_info.x_position, drone_generation_info.y_position = shifted_coords(drone_generation_info.x_position, drone_generation_info.y_position, drone_generation_info.x_velocity * packets_generator.GENERATION_PERIOD, drone_generation_info.y_velocity * packets_generator.GENERATION_PERIOD)

            if drone_generation_info.height + drone_generation_info.vertical_speed * packets_generator.GENERATION_PERIOD < drone_generation_info.max_height:
                 drone_generation_info.height += drone_generation_info.vertical_speed 
            else:
                 drone_generation_info.vertical_speed = 0


    def calculate_pitch(drone_generation_info: drone_generation_info):
        pitch = math.sqrt(drone_generation_info.x_velocity**2 + drone_generation_info.y_velocity**2) * packets_generator.PITCH_DEGREES_PER_M_S
        if pitch > packets_generator.MAX_PITCH:
            return packets_generator.MAX_PITCH + random.uniform(-packets_generator.BASE_VARIANCE_PITCH, packets_generator.BASE_VARIANCE_PITCH) 
        else:
            return pitch
        
    def generate_random_data_for_multiple_drones():

        packets_generator.update_drone_generation_info()

        for drone_generation_info in packets_generator.drone_generation_infos:
            if drone_generation_info.packetType == PacketType.remoteid:
                new_remoteid_movement = RemoteIDMovement(
                    remoteid_info_id =  drone_generation_info.info_id,
                    remoteid_flight_id = drone_generation_info.flight_id,
                    lat = drone_generation_info.x_position,
                    lng = drone_generation_info.y_position,
                    altitude = drone_generation_info.height + 10,
                    height = drone_generation_info.height,
                    x_speed = drone_generation_info.x_velocity,
                    y_speed = drone_generation_info.y_velocity,
                    z_speed = drone_generation_info.vertical_speed,
                    pitch = packets_generator.calculate_pitch(drone_generation_info),
                    roll = random.uniform(-packets_generator.BASE_VARIANCE_ROLL, packets_generator.BASE_VARIANCE_ROLL),
                    yaw = random.uniform(-packets_generator.BASE_VARIANCE_YAW, packets_generator.BASE_VARIANCE_YAW),
                    spoofed = True,
                    timestamp = datetime.datetime.now(),
                    pilot_lat = drone_generation_info.start_x_position,
                    pilot_lng = drone_generation_info.start_y_position
                )
                db.session.add(new_remoteid_movement)

            else:
                new_droneid_movement = DroneIDMovement(
                    droneid_info_id =  drone_generation_info.info_id,
                    droneid_flight_id = drone_generation_info.flight_id,
                    state_info = 5023,
                    latitude = drone_generation_info.x_position,
                    longitude = drone_generation_info.y_position,
                    altitude = drone_generation_info.height + 10,
                    height = drone_generation_info.height,
                    v_north = drone_generation_info.y_velocity,
                    v_east = drone_generation_info.x_velocity,
                    v_up = drone_generation_info.vertical_speed,
                    yaw = random.uniform(-packets_generator.BASE_VARIANCE_YAW, packets_generator.BASE_VARIANCE_YAW),
                    gps_time = datetime.datetime.now(),
                    rc_latitude = drone_generation_info.start_x_position,
                    rc_longitude = drone_generation_info.start_y_position
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
    


    def get_current_droneid_flights_ids():
        ids = []
        for drone_generation_info in packets_generator.drone_generation_infos:
            if drone_generation_info.packetType == PacketType.droneid:
                ids.append(drone_generation_info.flight_id)
        return ids

    def get_current_remoteid_flights_ids():
        ids = []
        for drone_generation_info in packets_generator.drone_generation_infos:
            if drone_generation_info.packetType == PacketType.remoteid:
                ids.append(drone_generation_info.flight_id)
        return ids