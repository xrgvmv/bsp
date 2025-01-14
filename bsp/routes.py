from flask import Blueprint, render_template
from bsp.models.remoteid import RemoteID
from bsp.models.droneid import DroneID
from bsp.functions import add_data_to_db

main = Blueprint('main', __name__)

@main.route('/')
def home():
    return render_template('index.html')

@main.route('/about')
def about():
    return render_template('about.html')

@main.route('/add_data')
def add_data():
    add_data_to_db()
    return "Dane zostały dodane do bazy!"

@main.route('/map_view')
def map_view():
    remote_id = RemoteID.query.first()
    return render_template('map.html', remote_id=remote_id.to_dict()) 