import os
from app import create_app
from config import config

# 'FLASK_CONFIG' will be set to 'production' on Render
env = os.getenv('FLASK_CONFIG') or 'default'
app = create_app(config[env])

# Note: app.run() is removed because Gunicorn handles the process in the cloud. It's no longer Flask's responsibility to start the server directly.