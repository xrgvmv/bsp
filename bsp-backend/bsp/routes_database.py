from flask import Blueprint, jsonify, request
from bsp.packets_generator import packets_generator
from sqlalchemy import func, asc, desc

from bsp.models.droneid_info import DroneIDInfo
from bsp.models.droneid_movement import DroneIDMovement
from bsp.models.droneid_flight import DroneIDFlight

from bsp.models.remoteid_info import RemoteIDInfo
from bsp.models.remoteid_flight import RemoteIDFlight
from bsp.models.remoteid_movement import RemoteIDMovement

from sqlalchemy import func

from .database import db

routes_database = Blueprint('routes_database', __name__)

@routes_database.route('/api/routes_database/get/droneid_movement', methods=['GET'])
def get_droneid_movement():
    try:
        movements = DroneIDMovement.query.all()
        return jsonify(movements), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@routes_database.route('/api/routes_database/get/remoteid_movement', methods=['GET'])
def get_remoteid_movement():
    try:
        movements = RemoteIDMovement.query.all()
        return jsonify(movements), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@routes_database.route('/api/routes_database/get/droneid_info', methods=['GET'])
def get_droneid_info():
    try:
        movements = DroneIDInfo.query.all()
        return jsonify(movements), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@routes_database.route('/api/routes_database/get/remoteid_info', methods=['GET'])
def get_remoteid_info():
    try:
        movements = RemoteIDInfo.query.all()
        return jsonify(movements), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@routes_database.route('/api/routes_database/get/droneid_flight', methods=['GET'])
def get_droneid_flight():
    try:
        movements = DroneIDFlight.query.all()
        return jsonify(movements), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@routes_database.route('/api/routes_database/get/remoteid_flight', methods=['GET'])
def get_remoteid_flight():
    try:
        movements = RemoteIDFlight.query.all()
        return jsonify(movements), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def save_records(ModelClass, data):
    if not isinstance(data, list):
        data = [data]

    records = [ModelClass(**item) for item in data]
    db.session.add_all(records)
    db.session.commit()
    return jsonify({
        'message': f'Saved {len(records)} records',
        'ids': [r.id for r in records]
    }), 201

@routes_database.route('/api/routes_database/post/droneid_info', methods=['POST'])
def post_droneid_info():
    try:
        data = request.get_json()
        return save_records(DroneIDInfo, data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@routes_database.route('/api/routes_database/post/droneid_movement', methods=['POST'])
def post_droneid_movement():
    try:
        data = request.get_json()
        return save_records(DroneIDMovement, data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@routes_database.route('/api/routes_database/post/droneid_flight', methods=['POST'])
def post_droneid_flight():
    try:
        data = request.get_json()
        return save_records(DroneIDFlight, data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@routes_database.route('/api/routes_database/post/remoteid_info', methods=['POST'])
def post_remoteid_info():
    try:
        data = request.get_json()
        return save_records(RemoteIDInfo, data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@routes_database.route('/api/routes_database/post/remoteid_flight', methods=['POST'])
def post_remoteid_flight():
    try:
        data = request.get_json()
        return save_records(RemoteIDFlight, data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@routes_database.route('/api/routes_database/post/remoteid_movement', methods=['POST'])
def post_remoteid_movement():
    try:
        data = request.get_json()
        return save_records(RemoteIDMovement, data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
