#!/usr/bin/python
#
# Start simple python web server with index.php for main page
#
from subprocess import call

call(["php", "-S", "127.0.0.1:8000"])