from flask import Flask
from .routes import main

def create_app(config_filename='config.py'):
    app = Flask(__name__)
    app.config.from_pyfile(config_filename)
    
    app.register_blueprint(main)

    return app
