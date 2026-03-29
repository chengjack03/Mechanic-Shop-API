import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Secret key for JWT/Sessions retrieved from environment
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-only'

class DevelopmentConfig(Config):
    # Your local MySQL database
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'mysql+mysqlconnector://root:your_password@localhost/mechanic_shop_db'

class ProductionConfig(Config):
    # Render provides DATABASE_URL for Postgres. 
    # We fix the prefix 'postgres://' to 'postgresql://' for SQLAlchemy compatibility.
    uri = os.environ.get("DATABASE_URL")
    if uri and uri.startswith("postgres://"):
        uri = uri.replace("postgres://", "postgresql://", 1)
    SQLALCHEMY_DATABASE_URI = uri

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}