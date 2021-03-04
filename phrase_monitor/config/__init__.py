import os
import sys

from phrase_monitor.config.base import BaseConfig

env = os.environ.get('APP_ENV', 'DEFAULT')

if env in ('DEFAULT', 'dev'):
    config = BaseConfig
else:
    print("Unknown application environment: {0}".format(env))
    sys.exit(4)