from flask import Blueprint, jsonify
from bsp.models.droneid_info import DroneIDInfo
from bsp.models.droneid_movement import DroneIDMovement
from bsp.models.remoteid_info import RemoteIDInfo
from bsp.models.remoteid_movement import RemoteIDMovement
from bsp.packets_generator import global_generator
from sqlalchemy import func


main = Blueprint('main', __name__)


@main.route('/api/get_remoteid_info', methods=['GET'])
def get_remoteid_info():
    try:
        # remote_id_info = RemoteIDInfo.query.all()
        # if remote_id_info:
        #     return jsonify([ri.to_dict() for ri in remote_id_info]), 200
        # else:
        #     return jsonify({"message": "No data"}), 404
        
        return jsonify([ri for ri in global_generator.flying_remoteid_info]), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@main.route('/api/get_droneid_info', methods=['GET'])
def get_droneid_info():
    try:
        # drone_id_info = DroneIDInfo.query.all()
        # if drone_id_info:
        #     return jsonify([di.to_dict() for di in drone_id_info]), 200 
        # else:
        #     return jsonify({"message": "No data"}), 404

        return jsonify([di for di in global_generator.flying_droneid_info]), 200

        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@main.route('/api/get_remoteid_movement', methods=['GET'])
def get_remoteid_movement():
    try:
        id_list = [drone.id for drone in global_generator.flying_remoteid_info]
        
        subquery = RemoteIDMovement.query \
            .filter(RemoteIDMovement.drone_id.in_(id_list)) \
            .with_entities(RemoteIDMovement.drone_id, func.max(RemoteIDMovement.id).label('max_id')) \
            .group_by(RemoteIDMovement.drone_id) \
            .subquery()

        remote_id_movements = RemoteIDMovement.query \
            .join(subquery, RemoteIDMovement.id == subquery.c.max_id)
        
        if remote_id_movements:
            return jsonify([rim for rim in remote_id_movements]), 200
        else:
            return jsonify({"message": "No data"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@main.route('/api/get_droneid_movement', methods=['GET'])
def get_droneid_movement():
    try:
        id_list = [drone.id for drone in global_generator.flying_droneid_info]

        subquery = DroneIDMovement.query \
            .filter(DroneIDMovement.drone_id.in_(id_list)) \
            .with_entities(DroneIDMovement.drone_id, func.max(DroneIDMovement.id).label('max_id')) \
            .group_by(DroneIDMovement.drone_id) \
            .subquery()

        drone_id_movements = DroneIDMovement.query \
            .join(subquery, DroneIDMovement.id == subquery.c.max_id)
        
        if drone_id_movements:
            return jsonify([dim for dim in drone_id_movements]), 200
        else:
            return jsonify({"message": "No data"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500