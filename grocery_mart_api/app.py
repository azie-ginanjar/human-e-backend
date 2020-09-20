from flask import Flask
from flask_cors import CORS
from grocery_mart_api import auth, api
from grocery_mart_api.extensions import db, jwt, migrate
import os

PRODUCTION = 'production'
STAGING = 'staging'


def create_app(testing=False, cli=False):
    """Application factory, used to create application
    """
    app = Flask('grocery_mart_api')

    configure_app(app, testing)
    configure_extensions(app, cli)
    register_blueprints(app)

    return app


def configure_app(app, testing=False):
    environment = os.environ.get('ENVIRONMENT')

    # default configuration
    app.config.from_object('grocery_mart_api.config')
    if testing is True:
        # override with testing config
        app.config.from_object('grocery_mart_api.configtest')
    else:
        if environment == PRODUCTION:
            app.config.from_object('grocery_mart_api.configprod')
        elif environment == STAGING:
            app.config.from_object('grocery_mart_api.configstaging')


def configure_extensions(app, cli):
    """configure flask extensions
    """
    db.init_app(app)
    jwt.init_app(app)
    CORS(app)

    if cli is True:
        migrate.init_app(app, db)


def register_blueprints(app):
    """register all blueprints for application
    """
    app.register_blueprint(auth.views.blueprint)
    app.register_blueprint(api.views.blueprint)
