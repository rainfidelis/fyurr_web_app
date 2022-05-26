import os
from decouple import config

SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
# DEBUG = True
DEBUG = False

# TODO IMPLEMENT DATABASE URL
# SQLALCHEMY_DATABASE_URI = config('DATABASE_URL')
SQLALCHEMY_DATABASE_URI = 'postgres://tfdifunehnugpr:674d906ea3e40d58d0dbbe19501739e541e9bd7cd30a07a06b6544f43fb4209f@ec2-54-204-56-171.compute-1.amazonaws.com:5432/d47lkklk22aqfk'
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Keep CSRF token till end of current session
WTF_CSRF_TIME_LIMIT = None
