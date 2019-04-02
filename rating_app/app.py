from flask import Flask

from rating_app import api
from rating_app.extensions import db, migrate


def create_app(config=None, testing=False, cli=False):
    """Application factory, used to create application
    """
    app = Flask('rating_app')

    configure_app(app, testing)
    configure_extensions(app, cli)
    register_blueprints(app)

    return app


def configure_app(app, testing=False):
    """set configuration for application
    """
    # default configuration
    app.config.from_object('rating_app.config')

    if testing is True:
        # override with testing config
        app.config.from_object('rating_app.configtest')
    else:
        # override with env variable, fail silently if not set
        app.config.from_envvar("RATING_APP_CONFIG", silent=True)


def configure_extensions(app, cli):
    """configure flask extensions
    """
    db.init_app(app)

    if cli is True:
        migrate.init_app(app, db)


def register_blueprints(app):
    """register all blueprints for application
    """
    app.register_blueprint(api.views.blueprint)
