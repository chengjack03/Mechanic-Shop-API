# config.py
class DevelopmentConfig:
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = (
        "mysql+mysqlconnector://root:YOUR_PASSWORD@localhost/mechanic_shop_db"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "your-secret-key"
