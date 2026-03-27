# app/__init__.py
from flask import Flask
from .extensions import db, ma, limiter, cache
from config import DevelopmentConfig


def create_app():
    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig)

    db.init_app(app)
    ma.init_app(app)
    limiter.init_app(app)
    cache.init_app(app, config={"CACHE_TYPE": "SimpleCache"})

    from .blueprints.customers import customers_bp
    from .blueprints.mechanics import mechanics_bp
    from .blueprints.service_tickets import service_tickets_bp
    from .blueprints.inventory import inventory_bp

    app.register_blueprint(customers_bp, url_prefix='/customers')
    app.register_blueprint(mechanics_bp, url_prefix='/mechanics')
    app.register_blueprint(service_tickets_bp, url_prefix='/service-tickets')
    app.register_blueprint(inventory_bp, url_prefix='/inventory')

    with app.app_context():
        from . import models
        db.create_all()

    return app
