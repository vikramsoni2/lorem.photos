activate_this = "/home/ubuntu/lorem/venv/bin/activate_this.py"
with open(activate_this) as f:
    exec(f.read(), dict(__file__=activate_this))

import sys, os
import logging

logging.basicConfig(stream=sys.stderr)
os.chdir('/var/www/html/lorem/')
sys.path.insert(0, "/var/www/html/lorem/")

from app import app as application
