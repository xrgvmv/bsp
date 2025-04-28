import datetime
from flask import Blueprint, jsonify, request
from bsp.packets_generator import packets_generator
from sqlalchemy import func, asc, desc
import time

from bsp.models.droneid_info import DroneIDInfo
from bsp.models.droneid_movement import DroneIDMovement
from bsp.models.droneid_flight import DroneIDFlight

from bsp.models.remoteid_info import RemoteIDInfo
from bsp.models.remoteid_flight import RemoteIDFlight
from bsp.models.remoteid_movement import RemoteIDMovement

from sqlalchemy import func


main = Blueprint('main', __name__)


def get_flying_remoteid_info_ids():
    ids = RemoteIDMovement.query \
        .filter(RemoteIDMovement.timestamp + datetime.timedelta(seconds=10) > func.now())\
        .with_entities(RemoteIDMovement.remoteid_info_id)\
        .distinct()\
        .all()
    return [id for (id,) in ids]

def get_flying_droneid_info_ids():
    ids = DroneIDMovement.query \
        .filter(DroneIDMovement.gps_time + datetime.timedelta(seconds=10) > func.now())\
        .with_entities(DroneIDMovement.droneid_info_id)\
        .distinct()\
        .all()
    return [id for (id,) in ids]


def get_current_remoteid_flights_ids():
    ids = RemoteIDMovement.query \
        .filter(RemoteIDMovement.timestamp + datetime.timedelta(seconds=10) > func.now())\
        .with_entities(RemoteIDMovement.remoteid_flight_id)\
        .distinct()\
        .all()
    return [id for (id,) in ids]

def get_current_droneid_flights_ids():
    ids = DroneIDMovement.query \
        .filter(DroneIDMovement.gps_time + datetime.timedelta(seconds=10) > func.now())\
        .with_entities(DroneIDMovement.droneid_flight_id)\
        .distinct()\
        .all()
    return [id for (id,) in ids]


#live data 

#flying drones infos 
@main.route('/api/get_current_remoteid_info', methods=['GET'])
def get_current_remoteid_info():
    try:
        id_list = get_flying_remoteid_info_ids()
        print(id_list)
        remote_id_infos = RemoteIDInfo.query.filter(RemoteIDInfo.id.in_(id_list))
        if remote_id_infos:
            return jsonify({"remoteid_info_list": [ri for ri in remote_id_infos]}), 200
        else:
            return jsonify({"message": "No data"}), 404
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@main.route('/api/get_current_droneid_info', methods=['GET'])
def get_current_droneid_info():
    try:
        id_list = get_flying_droneid_info_ids()
        drone_id_infos = DroneIDInfo.query.filter(DroneIDInfo.id.in_(id_list))
        if drone_id_infos:
            return jsonify({"droneid_info_list": [di for di in drone_id_infos]}), 200
        else:
            return jsonify({"message": "No data"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500



#flying drones flights
@main.route('/api/get_current_remoteid_flights', methods=['GET'])
def get_current_remoteid_flights():
    try:
        id_list = get_current_remoteid_flights_ids()
        remote_id_infos = RemoteIDFlight.query.filter(RemoteIDFlight.id.in_(id_list))
        if remote_id_infos:
            return jsonify({"remoteid_flights_list": [ri for ri in remote_id_infos]}), 200
        else:
            return jsonify({"message": "No data"}), 404
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@main.route('/api/get_current_droneid_flights', methods=['GET'])
def get_current_droneid_flights():
    try:
        id_list = get_current_droneid_flights_ids()
        drone_id_infos = DroneIDFlight.query.filter(DroneIDFlight.id.in_(id_list))
        if drone_id_infos:
            return jsonify({"droneid_flights_list": [di for di in drone_id_infos]}), 200
        else:
            return jsonify({"message": "No data"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500


#flying drones movements
@main.route('/api/get_current_remoteid_movement', methods=['GET'])
def get_remoteid_movement():
    try:
        id_list = get_flying_remoteid_info_ids()
        
        subquery = RemoteIDMovement.query \
            .filter(RemoteIDMovement.remoteid_info_id.in_(id_list)) \
            .with_entities(RemoteIDMovement.remoteid_info_id, func.max(RemoteIDMovement.id).label('max_id')) \
            .group_by(RemoteIDMovement.remoteid_info_id) \
            .subquery()

        remote_id_movements = RemoteIDMovement.query \
            .join(subquery, RemoteIDMovement.id == subquery.c.max_id)
        
        if remote_id_movements:
            return jsonify({"remoteid_movement_list": [rim for rim in remote_id_movements]}), 200
        else:
            return jsonify({"message": "No data"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@main.route('/api/get_current_droneid_movement', methods=['GET'])
def get_droneid_movement():
    try:
        id_list = get_flying_droneid_info_ids()

        subquery = DroneIDMovement.query \
            .filter(DroneIDMovement.droneid_info_id.in_(id_list)) \
            .with_entities(DroneIDMovement.droneid_info_id, func.max(DroneIDMovement.id).label('max_id')) \
            .group_by(DroneIDMovement.droneid_info_id) \
            .subquery()

        drone_id_movements = DroneIDMovement.query \
            .join(subquery, DroneIDMovement.id == subquery.c.max_id)
        
        if drone_id_movements:
            return jsonify({"droneid_movement_list": [dim for dim in drone_id_movements]}), 200
        else:
            return jsonify({"message": "No data"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    



    #historic data

@main.route('/api/get_all_remoteid_info', methods=['GET'])
def get_all_remoteid_info():
    try:
        remote_id_infos = RemoteIDInfo.query.all()
        if remote_id_infos:
            return jsonify({"remoteid_info_list": [ri for ri in remote_id_infos]}), 200
        else:
            return jsonify({"message": "No data"}), 404
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@main.route('/api/get_all_droneid_info', methods=['GET'])
def get_all_droneid_info():
    try:
        drone_id_infos = DroneIDInfo.query.all()
        if drone_id_infos:
            return jsonify({"droneid_info_list": [di for di in drone_id_infos]}), 200
        else:
            return jsonify({"message": "No data"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@main.route('/api/get_droneid_movements_based_on_id_of_drone_and_flight', methods=['GET'])
def get_droneid_movements_based_on_id_of_drone_and_flight():
    try:
        flight_id = request.args.get('flight_id', type=int)
        drone_id = request.args.get('drone_id', type=int)
        
        if flight_id is None or drone_id is None:
            return jsonify({"error": "Missing parameters"}), 400

        droneid_movements = DroneIDMovement.query.filter_by(droneid_flight_id=flight_id, droneid_info_id=drone_id).order_by(DroneIDMovement.gps_time).all()
        if droneid_movements:
            return jsonify({"droneid_movements": [dm for dm in droneid_movements]}), 200
        else:
            return jsonify({"message": "No data"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@main.route('/api/get_remoteid_movements_based_on_id_of_drone_and_flight', methods=['GET'])
def get_remoteid_movements_based_on_id_of_drone_and_flight():
    try:
        flight_id = request.args.get('flight_id', type=int)
        drone_id = request.args.get('drone_id', type=int)
        
        if flight_id is None or drone_id is None:
            return jsonify({"error": "Missing parameters"}), 400

        remoteid_movements = RemoteIDMovement.query.filter_by(remoteid_flight_id=flight_id, remoteid_info_id=drone_id).order_by(RemoteIDMovement.timestamp).all()
        if remoteid_movements:
            return jsonify({"remoteid_movements": [rm for rm in remoteid_movements]}), 200
        else:
            return jsonify({"message": "No data"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@main.route('/api/get_droneid_flights_based_on_id_of_drone', methods=['GET'])
def get_droneid_flights_based_on_id_of_drone():
    try:
        drone_id = request.args.get('drone_id', type=int)
        
        if drone_id is None:
            return jsonify({"error": "Missing parameters"}), 400

        droneid_flights = DroneIDFlight.query.filter_by(droneid_info_id=drone_id).all()
        
        flights_data = []
        for flight in droneid_flights:
            first_entry = (
                DroneIDMovement.query
                .filter_by(droneid_flight_id=flight.id, droneid_info_id=drone_id)
                .order_by(asc(DroneIDMovement.gps_time))
                .first()
            )
            last_entry = (
                DroneIDMovement.query
                .filter_by(droneid_flight_id=flight.id, droneid_info_id=drone_id)
                .order_by(desc(DroneIDMovement.gps_time))
                .first()
            )
    
            flights_data.append({
                "flight_id": flight.id,
                "drone_id": flight.droneid_info_id,
                "start_time": first_entry.gps_time.isoformat() if first_entry else None,
                "end_time": last_entry.gps_time.isoformat() if last_entry else None,
                "rc_longitude": flight.home_longitude,
                "rc_latitude": flight.home_latitude
            })

        if flights_data:
            return jsonify({"droneid_flights": flights_data}), 200
        else:
            return jsonify({"message": "No data"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@main.route('/api/get_remoteid_flights_based_on_id_of_drone', methods=['GET'])
def get_remoteid_flights_based_on_id_of_drone():
    try:
        drone_id = request.args.get('drone_id', type=int)
        
        if drone_id is None:
            return jsonify({"error": "Missing parameters"}), 400

        remoteid_flights = RemoteIDFlight.query.filter_by(remoteid_info_id=drone_id).all()
        
        flights_data = []
        for flight in remoteid_flights:
            first_entry = (
                RemoteIDMovement.query
                .filter_by(remoteid_flight_id=flight.id, remoteid_info_id=drone_id)
                .order_by(asc(RemoteIDMovement.timestamp))
                .first()
            )
            last_entry = (
                RemoteIDMovement.query
                .filter_by(remoteid_flight_id=flight.id, remoteid_info_id=drone_id)
                .order_by(desc(RemoteIDMovement.timestamp))
                .first()
            )

            flights_data.append({
                "flight_id": flight.id,
                "drone_id": flight.remoteid_info_id,
                "start_time": first_entry.timestamp.isoformat() if first_entry else None,
                "end_time": last_entry.timestamp.isoformat() if last_entry else None,
                "home_lng": flight.home_lng,
                "home_lat": flight.home_lat
            })

        if flights_data:
            return jsonify({"remoteid_flights": flights_data}), 200
        else:
            return jsonify({"message": "No data"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@main.route('/api/get_droneid_movements', methods=['GET'])
def get_droneid_movements():
    try:
        drone_id = request.args.get('drone_id', type=int)
        limit = request.args.get('limit', default=100, type=int)

        if not drone_id:
            return jsonify({"error": "Missing drone_id"}), 400

        flight = (
            DroneIDFlight.query
            .filter_by(droneid_info_id=drone_id)
            .order_by(desc(DroneIDFlight.id))
            .first()
        )

        if not flight:
            return jsonify({"error": "No flight found for this drone_id"}), 404

        movements = (
            DroneIDMovement.query
            .filter_by(droneid_info_id=drone_id, droneid_flight_id=flight.id)
            .order_by(desc(DroneIDMovement.gps_time))
            .limit(limit)
            .all()
        )

        result = [{
            "id": m.id,
            "drone_id": m.droneid_info_id,
            "flight_id": m.droneid_flight_id,
            "lat": m.latitude,
            "lng": m.longitude,
            "altitude": m.altitude,
            "height": m.height,
            "v_north": m.v_north,
            "v_east": m.v_east,
            "v_up": m.v_up,
            "yaw": m.yaw,
            "gps_time": m.gps_time.isoformat(),
            "rc_latitude": m.rc_latitude,
            "rc_longitude": m.rc_longitude
        } for m in movements]

        return jsonify({"droneid_movements": result}), 200 if result else (jsonify({"message": "No data"}), 404)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@main.route('/api/get_remoteid_movements', methods=['GET'])
def get_remoteid_movements():
    try:
        drone_id = request.args.get('drone_id', type=int)
        limit = request.args.get('limit', default=100, type=int)

        if not drone_id:
            return jsonify({"error": "Missing drone_id"}), 400

        flight = (
            RemoteIDFlight.query
            .filter_by(remoteid_info_id=drone_id)
            .order_by(desc(RemoteIDFlight.id))
            .first()
        )

        if not flight:
            return jsonify({"error": "No flight found for this drone_id"}), 404

        movements = (
            RemoteIDMovement.query
            .filter_by(remoteid_info_id=drone_id, remoteid_flight_id=flight.id)
            .order_by(desc(RemoteIDMovement.timestamp))
            .limit(limit)
            .all()
        )

        result = [{
            "id": m.id,
            "drone_id": m.remoteid_info_id,
            "flight_id": m.remoteid_flight_id,
            "lat": m.lat,
            "lng": m.lng,
            "altitude": m.altitude,
            "height": m.height,
            "x_speed": m.x_speed,
            "y_speed": m.y_speed,
            "z_speed": m.z_speed,
            "pitch": m.pitch,
            "roll": m.roll,
            "yaw": m.yaw,
            "spoofed": m.spoofed,
            "timestamp": m.timestamp.isoformat(),
            "pilot_lat": m.pilot_lat,
            "pilot_lng": m.pilot_lng
        } for m in movements]

        return jsonify({"remoteid_movements": result}), 200 if result else (jsonify({"message": "No data"}), 404)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@main.route('/api/get_current_flight_based_on_drone_id', methods=['GET'])
def get_current_flight_based_on_drone_id():
    try:
        drone_id = request.args.get('drone_id', type=int)
        
        if drone_id is None:
            return jsonify({"error": "Missing parameters"}), 400

        flight = DroneIDFlight.query.filter_by(droneid_info_id=drone_id).order_by(desc(DroneIDFlight.id)).first()
        
        if flight:
            return jsonify({"droneid_flight": {
                "flight_id": flight.id,
                "drone_id": flight.droneid_info_id,
                "home_longitude": flight.home_longitude,
                "home_latitude": flight.home_latitude
            }}), 200
        else:
            return jsonify({"message": "No data"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@main.route('/api/get_current_flight_based_on_remote_id', methods=['GET'])
def get_current_flight_based_on_remote_id():
    try:
        remote_id = request.args.get('remote_id', type=int)
        
        if remote_id is None:
            return jsonify({"error": "Missing parameters"}), 400

        flight = RemoteIDFlight.query.filter_by(remoteid_info_id=remote_id).order_by(desc(RemoteIDFlight.id)).first()
        
        if flight:
            return jsonify({"remoteid_flight": {
                "flight_id": flight.id,
                "drone_id": flight.remoteid_info_id,
                "home_longitude": flight.home_lng,
                "home_latitude": flight.home_lat
            }}), 200
        else:
            return jsonify({"message": "No data"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500