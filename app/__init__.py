from flask import Flask
from config import config
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app(config_name):
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'kkjiioopasd'
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    app.debug = True
    with app.app_context():
        db.init_app(app)

    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api')

    return app
