from flask import Blueprint, jsonify
from bsp.packets_generator import packets_generator
from sqlalchemy import func

from bsp.models.droneid_info import DroneIDInfo
from bsp.models.droneid_movement import DroneIDMovement
from bsp.models.droneid_flight import DroneIDFlight

from bsp.models.remoteid_info import RemoteIDInfo
from bsp.models.remoteid_flight import RemoteIDFlight
from bsp.models.remoteid_movement import RemoteIDMovement

main = Blueprint('main', __name__)


#live data 

#flying drones infos 
@main.route('/api/get_current_remoteid_info', methods=['GET'])
def get_current_remoteid_info():
    try:
        id_list = packets_generator.get_flying_remoteid_info_ids()
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
        id_list = packets_generator.get_flying_droneid_info_ids()
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
        id_list = packets_generator.get_current_remoteid_flights_ids()
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
        id_list = packets_generator.get_current_droneid_flights_ids()
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
        id_list = packets_generator.get_flying_remoteid_info_ids()
        
        subquery = RemoteIDMovement.query \
            .filter(RemoteIDMovement.drone_id.in_(id_list)) \
            .with_entities(RemoteIDMovement.drone_id, func.max(RemoteIDMovement.id).label('max_id')) \
            .group_by(RemoteIDMovement.drone_id) \
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
        id_list = packets_generator.get_flying_droneid_info_ids()

        subquery = DroneIDMovement.query \
            .filter(DroneIDMovement.drone_id.in_(id_list)) \
            .with_entities(DroneIDMovement.drone_id, func.max(DroneIDMovement.id).label('max_id')) \
            .group_by(DroneIDMovement.drone_id) \
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
        drone_id_infos = RemoteIDInfo.query.all()
        if drone_id_infos:
            return jsonify({"droneid_info_list": [di for di in drone_id_infos]}), 200
        else:
            return jsonify({"message": "No data"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500