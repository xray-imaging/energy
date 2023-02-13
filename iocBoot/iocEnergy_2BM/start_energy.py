# This script creates an object of type Energy for doing energy save tasks
# To run this script type the following:
#     python -i start_energy.py
# The -i is needed to keep Python running, otherwise it will create the object and exit
from energy.energy_2bm import Energy2BM
ts = Energy2BM(["../../db/energy_settings.req",
			 "../../db/energy_2BM_settings.req"], 
                {"$(P)":"2bm:", "$(R)":"Energy:"})
