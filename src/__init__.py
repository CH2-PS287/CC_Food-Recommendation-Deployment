from flask import Flask, render_template
# from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

from src.config import Config

load_dotenv()
# instantiate the db
# db = SQLAlchemy()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # initialization
    # db.init_app(app)

    # blueprints
    from src.main.routes import main
    app.register_blueprint(main)

    return app