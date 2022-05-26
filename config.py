import os
from decouple import config

SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.

DEBUG = config('DEBUG')

# TODO IMPLEMENT DATABASE URL
SQLALCHEMY_DATABASE_URI = config('DATABASE_URL')
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Keep CSRF token till end of current session
WTF_CSRF_TIME_LIMIT = None
