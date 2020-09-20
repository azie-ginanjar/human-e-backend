"""Default configuration

Use env var to override
"""
import os

basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = True
SECRET_KEY = "changeme"

SQLALCHEMY_DATABASE_URI = "postgresql://postgres@localhost/grocery_mart_api"
SQLALCHEMY_TRACK_MODIFICATIONS = False
