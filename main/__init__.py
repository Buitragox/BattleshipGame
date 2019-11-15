from flask import Flask
from . import controller    


def create_app():
    app = Flask(__name__)

    app.config.from_pyfile('config.py')
    app.register_blueprint(controller.bp)

    return app