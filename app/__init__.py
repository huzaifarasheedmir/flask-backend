from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

from config import config

db = SQLAlchemy()


def create_app(config_name):
    """Create app withe provided config name """

    app = Flask(__name__)
    app.config.from_object(config[config_name])

    db.init_app(app)

    from app.orders import orders as orders_blueprint
    app.register_blueprint(orders_blueprint, url_prefix='/v1.0')

    return app
