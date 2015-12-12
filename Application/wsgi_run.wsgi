import sys

#Expand Python classes path with app's main path
sys.path.insert(0, "APPLICATION PATH HERE")

from Application import app

#Initialize WSGI application objects
application = app