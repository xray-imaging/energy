# This script creates an object of type Energy for doing energy save tasks
# To run this script type the following:
#     python -i start_energy.py
# The -i is needed to keep Python running, otherwise it will create the object and exit
from energy.epics_server import Energy
ts = Energy(["../../db/saveEnergy_settings.req", ], {"$(P)":"2bm:", "$(R)":"Energy:"})
