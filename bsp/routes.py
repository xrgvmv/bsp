from flask import Blueprint, jsonify
from bsp.models.droneid_info import DroneIDInfo
from bsp.models.droneid_movement import DroneIDMovement
from bsp.models.remoteid_info import RemoteIDInfo
from bsp.models.remoteid_movement import RemoteIDMovement
from bsp.functions import generate_initial_drone_info

main = Blueprint('main', __name__)

@main.route('/api/generate_initial_drone_info', methods=['GET'])
def generate_initial_drone_info_route():
    try:
        generate_initial_drone_info()
        return jsonify({"message": "Data generated"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@main.route('/api/get_remoteid_info', methods=['POST'])
def get_remoteid_info():
    try:
        remote_id_info = RemoteIDInfo.query.all()
        if remote_id_info:
            return jsonify([ri.to_dict() for ri in remote_id_info]), 200
        else:
            return jsonify({"message": "No data"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@main.route('/api/get_droneid_info', methods=['POST'])
def get_droneid_info():
    try:
        drone_id_info = DroneIDInfo.query.all()
        if drone_id_info:
            return jsonify([di.to_dict() for di in drone_id_info]), 200 
        else:
            return jsonify({"message": "No data"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@main.route('/api/get_remoteid_movement', methods=['POST'])
def get_remoteid_movement():
    try:
        remote_id_movements = RemoteIDMovement.query.group_by(RemoteIDMovement.drone_id).order_by(RemoteIDMovement.id.desc()).all()  
        if remote_id_movements:
            return jsonify([rim.to_dict() for rim in remote_id_movements]), 200
        else:
            return jsonify({"message": "No data"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@main.route('/api/get_droneid_movement', methods=['POST'])
def get_droneid_movement():
    try:
        drone_id_movements = DroneIDMovement.query.group_by(DroneIDMovement.drone_id).order_by(DroneIDMovement.id.desc()).all()
        if drone_id_movements:
            return jsonify([dim.to_dict() for dim in drone_id_movements]), 200
        else:
            return jsonify({"message": "No data"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500