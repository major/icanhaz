import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, '/var/www/html/icanhaz-app/icanhaz')
from icanhaz import app as application
