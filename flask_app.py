import os
from app import create_app

# Get the environment from Render, default to 'development'
env = os.environ.get('FLASK_ENV', 'development')

# Map the environment names to the CLASS NAMES in config.py
config_map = {
    'development': 'DevelopmentConfig',
    'testing': 'TestingConfig',
    'production': 'ProductionConfig'
}

# Pass the STRING name (e.g., 'ProductionConfig') to create_app
app = create_app(config_map.get(env, 'DevelopmentConfig'))

if __name__ == '__main__':
    app.run()