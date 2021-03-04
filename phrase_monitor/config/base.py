import os


class BaseConfig(object):
    # Enabling development environment
    DEBUG = True

    # Application PORT
    PORT = 7000

    # Application Host
    HOST = '0.0.0.0'

    # Logging Configuration
    EVENT_LOG_PATH = 'logs/access.log'
    ERROR_LOG_PATH = 'logs/error.log'

    # Postgres Config
    DATABASE_URL = os.environ.get('DATABASE_URL', 'postgres://postgres:postgres@localhost/twitter_streamer_db')

    # SESSION_TYPE
    SESSION_TYPE = "filesystem"
    SESSION_PERMANENT = False



