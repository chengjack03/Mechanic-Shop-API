import os
from app import create_app

# 1. Get the config name from your Render Environment Variable (FLASK_CONFIG)
# It will default to 'development' if not found
env = os.environ.get('FLASK_CONFIG', 'development')

# 2. Create the app by passing the environment string ('production' or 'development')
# Your app/__init__.py is already set up to turn this into 'config.production'
app = create_app(env)

if __name__ == '__main__':
    # This remains for local testing; Render will use Gunicorn to run the 'app' object
    app.run()