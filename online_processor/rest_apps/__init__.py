from flask import Flask, render_template
from config import config


def create_app():
    app = Flask(__name__)
    # app.config.from_object(config[config_name])
    # config[config_name].init_app(app)

    from .main import inf_restful as main_blueprint
    app.register_blueprint(main_blueprint)
    return app
