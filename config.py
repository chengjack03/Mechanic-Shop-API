import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Secret key for JWT/Sessions retrieved from environment
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-123'

class DevelopmentConfig(Config):
    # This remains for your local MySQL testing
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'mysql+mysqlconnector://root:your_password@localhost/mechanic_shop_db'

class ProductionConfig(Config):
    # This pulls the PostgreSQL URL from Render's settings
    uri = os.environ.get("DATABASE_URL")
    # SQLAlchemy requires 'postgresql://' but Render sometimes provides 'postgres://'
    if uri and uri.startswith("postgres://"):
        uri = uri.replace("postgres://", "postgresql://", 1)
    SQLALCHEMY_DATABASE_URI = uri

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}