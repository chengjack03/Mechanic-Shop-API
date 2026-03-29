import os

class Config:
    # Use the password you provided: CTct2026
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:CTct2026@localhost/mechanic_shop_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'be_m2_assignment_secret_key_2026'
    TESTING = False

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True
    # Required for the assignment: Use SQLite in-memory for unit tests
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'