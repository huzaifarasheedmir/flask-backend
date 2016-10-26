from flask import Flask

from config import config


def create_app(config_name):
    """Create app withe provided config name """

    app = Flask(__name__)
    app.config.from_object(config[config_name])

    from app.orders import orders as orders_blueprint
    app.register_blueprint(orders_blueprint, url_prefix='/v1.0')

    return app
