import os
import json

from importlib.resources import files

from dmm2bm import log

def load_preset():

    data_path = os.path.join(os.path.dirname(__file__), 'data', 'dmm.json')    

    log.info('Loading preset from: %s' % data_path)
    with open(data_path) as json_file:
        energy_lookup = json.load(json_file)

    return energy_lookup
