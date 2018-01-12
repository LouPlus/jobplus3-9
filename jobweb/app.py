from jobweb.config import configs
from flask import Flask
from jobweb.models import db

def register_blueprints(app):
    from .handlers import admin, front, users
    app.register_blueprint(admin)
    app.register_blueprint(front)
    app.register_blueprint(users)

def create_app(config):
    app = Flask(__name__)
    app.config.from_object(configs.get(config))
    db.init_app(app)
    register_blueprints(app)
    return app
