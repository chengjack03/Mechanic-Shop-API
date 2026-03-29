import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    DEBUG = True
    # Uses local environment variable for development
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL')

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    DEBUG = True

class ProductionConfig(Config):
    # This pulls the DATABASE_URL you set in Render's Environment tab
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')

# --- MODULE ATTRIBUTES ---
# These lines allow app.config.from_object('config.production') to work
development = DevelopmentConfig
testing = TestingConfig
production = ProductionConfig
default = DevelopmentConfig

# --- DICTIONARY MAPPING ---
# Keeping this for backward compatibility with any other parts of your app
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}