import datetime
import random
import threading
import time
from enum import Enum

from bsp.models.remoteid_movement import RemoteIDMovement
from .database import db
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
    def __init__(self, packetType: PacketType, start_x_position, start_y_position, flight_id, info_id):
        self.packetType = packetType
        self.info_id = info_id #id of droneid_info or remoteid_info
        self.flight_id = flight_id
        self.start_x_position = start_x_position
        self.start_y_position = start_y_position
        self.x_position = start_x_position
        self.y_position = start_y_position
        self.x_velocity = 0
        self.y_velocity = 0



class packets_generator():
    drone_generation_infos: list[drone_generation_info] = []
    generating_new_packets = False

    BASE_LATITUDE = 54.352025 # in degress
    BASE_LONGITUDE = 18.646638 # in degress
    BASE_VARIANCE = 0.01 # in degress
    GENERATION_PERIOD = 1 # in seconds
    NUMBER_OF_DRONES = 4 # per protocol
    MAX_SPEED_CHANGE = 0.01 # degrees per seconds
    SPEED_CHANGE_TIME = 2

    last_acceleration_update = None
    

    def __init__(self):
        pass

    # It only generates new droneid_info/remoteid_info when nothis is in database
    # In other situations it only adds new flights to exitsting droneid_info/remoteid_info   
    def start_generating_packets():
        if not packets_generator.generating_new_packets:
            
            #First we search for exisitng drones in our db
            [droneid_info_ids, remoteid_info_ids] = packets_generator.get_drone_infos_ids_from_db() 

            #If we don't have enought of them, we create now droneid_infos/remoteid_infos
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
            packets_generator.drone_generation_infos.append(drone_generation_info(PacketType.droneid, new_droneid_flights[i].home_latitude, new_droneid_flights[i].home_longitude, new_droneid_flights[i].id, new_droneid_flights[i].drone_id))
            packets_generator.drone_generation_infos.append(drone_generation_info(PacketType.remoteid, new_remoteid_flights[i].home_lat, new_remoteid_flights[i].home_lng, new_remoteid_flights[i].id, new_remoteid_flights[i].remote_id))
            


    def generate_new_flights(droneid_info_ids: list, remoteid_info_ids: list):
        
        new_droneid_flights = []
        new_remoteid_flights = []

        for i in range(packets_generator.NUMBER_OF_DRONES):
            new_home_latitude = packets_generator.BASE_LATITUDE + packets_generator.random_variance()
            new_home_longititude = packets_generator.BASE_LONGITUDE + packets_generator.random_variance()
            new_remoteid_flight = RemoteIDFlight(
                remote_id = remoteid_info_ids[i],
                pilot_lat = new_home_latitude,
                pilot_lng = new_home_longititude,
                home_lat = new_home_latitude,
                home_lng = new_home_longititude
            )
            db.session.add(new_remoteid_flight)
            new_remoteid_flights.append(new_remoteid_flight)


            new_home_latitude = packets_generator.BASE_LATITUDE + packets_generator.random_variance()
            new_home_longititude = packets_generator.BASE_LONGITUDE + packets_generator.random_variance()
            new_droneid_flight = DroneIDFlight(
                drone_id = droneid_info_ids[i],
                rc_latitude = new_home_latitude,
                rc_longitude = new_home_longititude,
                home_longitude = new_home_latitude,
                home_latitude = new_home_longititude
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

    def generate_initial_drone_info():
        
        flying_droneid_info = []
        flying_remoteid_info = []

        for drone_id in range(packets_generator.NUMBER_OF_DRONES):
            new_remoteid_info = RemoteIDInfo(
                serial_number=f"SN{random.randint(1, 1001)}",
                oui=f"OUI{random.randint(1, 1001)}",
                uuid=f"UUID{random.randint(1, 1001)}",
            )
            db.session.add(new_remoteid_info)
            flying_remoteid_info.append(new_remoteid_info)

            new_droneid_info = DroneIDInfo(
                serial_number=f"SN{random.randint(1, 101)}",
                device_type = 1234,
                uuid=f"UUID{random.randint(1, 1001)}",
            )
            db.session.add(new_droneid_info)
            flying_droneid_info.append(new_remoteid_info)

        db.session.commit() 

        return [[droneid_info.id for droneid_info in flying_droneid_info], [remoteid_info.id for remoteid_info in flying_remoteid_info]]


    def random_variance():
        return random.uniform(-packets_generator.BASE_VARIANCE, packets_generator.BASE_VARIANCE)


    def update_drone_generation_info():
        if packets_generator.last_acceleration_update is None or time.time() > packets_generator.last_acceleration_update + packets_generator.SPEED_CHANGE_TIME:
            packets_generator.last_acceleration_update = time.time()
            for drone_generation_info in packets_generator.drone_generation_infos: 
                drone_generation_info.x_velocity += random.uniform(-packets_generator.MAX_SPEED_CHANGE, packets_generator.MAX_SPEED_CHANGE)
                drone_generation_info.y_velocity += random.uniform(-packets_generator.MAX_SPEED_CHANGE, packets_generator.MAX_SPEED_CHANGE)

        for drone_generation_info in packets_generator.drone_generation_infos: 
            drone_generation_info.x_position += drone_generation_info.x_velocity * packets_generator.GENERATION_PERIOD
            drone_generation_info.y_position += drone_generation_info.y_velocity * packets_generator.GENERATION_PERIOD


    def generate_random_data_for_multiple_drones():

        packets_generator.update_drone_generation_info()

        for drone_generation_info in packets_generator.drone_generation_infos:
            if drone_generation_info.packetType == PacketType.remoteid:
                new_remoteid_movement = RemoteIDMovement(
                    drone_id =  drone_generation_info.info_id,
                    flight_id = drone_generation_info.flight_id,
                    lat = drone_generation_info.x_position,
                    lng = drone_generation_info.y_position,
                    altitude = 50,
                    height = 20,
                    x_speed = 10,
                    y_speed = 10,
                    z_speed = 10,
                    pitch = 5,
                    roll = 5,
                    yaw = 5,
                    spoofed = True,
                    timestamp = datetime.datetime.now()
                )
                db.session.add(new_remoteid_movement)

            else:
                new_droneid_movement = DroneIDMovement(
                    drone_id =  drone_generation_info.info_id,
                    flight_id = drone_generation_info.flight_id,
                    state_info = 1234,
                    latitude = drone_generation_info.x_position,
                    longitude = drone_generation_info.y_position,
                    altitude = 50,
                    height = 20,
                    v_north = 10,
                    v_east = 10,
                    v_up = 10,
                    yaw = 5,
                    gps_time = datetime.datetime.now()
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
