from flask_sqlalchemy import SQLAlchemy
from dataclasses import dataclass
from ..database import db

@dataclass
class RemoteIDFlight(db.Model):
    __tablename__ = 'remoteid_flight'

    id: int = db.Column(db.Integer, primary_key=True)
    remote_id: int = db.Column(db.Integer, db.ForeignKey('remoteid_info.id'), nullable=False)
 
    pilot_lat: float = db.Column(db.Float, nullable=True)
    pilot_lng: float = db.Column(db.Float, nullable=True)
    home_lng: float = db.Column(db.Float, nullable=True)
    home_lat: float = db.Column(db.Float, nullable=True)