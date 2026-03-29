import os
from app import create_app
from config import config

# Determine if we are in 'production' or 'development'
env = os.getenv('FLASK_CONFIG') or 'default'
app = create_app(config[env])

# No app.run() here. Gunicorn will look for the 'app' object in this file. It's no longer Flask's built-in server, so we don't call app.run(). Instead, Gunicorn will handle starting the server and will use the 'app' object we created.