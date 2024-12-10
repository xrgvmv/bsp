from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .routes import main

db = SQLAlchemy()

def create_app(config_filename='config.py'):
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@db:5432/bsp'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    app.config.from_pyfile(config_filename)
    
    db.init_app(app)

    app.register_blueprint(main)

    return app
