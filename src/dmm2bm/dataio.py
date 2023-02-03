import os
import json
import pathlib
import platform

import numpy as np

from importlib.resources import files

from dmm2bm import log
from dmm2bm import pvs

DATA_PATH = pathlib.Path(pathlib.Path(__file__).parent, 'data', 'dmm2bm.json')
DATA_PATH_LOCAL = pathlib.Path(pathlib.Path.home(), 'logs', 'dmm2bm.json')

def init_preset(args):
    reset_default_to_local_preset(args)

def load_preset(args):
    if DATA_PATH_LOCAL.exists():
        log.info('Loading preset from: %s' % DATA_PATH_LOCAL)
        with open(DATA_PATH_LOCAL) as json_file:
            energy_lookup = json.load(json_file)
    else:
        energy_lookup = reset_default_to_local_preset()
    return energy_lookup

def reset_default_to_local_preset(args):

    log.info('Loading preset from: %s' % DATA_PATH)
    with open(DATA_PATH) as json_file:
        energy_lookup = json.load(json_file)
    log.info('Create local preset file: %s' % DATA_PATH_LOCAL)
    with open(DATA_PATH_LOCAL, "w") as outfile:
        json.dump(energy_lookup, outfile, indent=4)        

    return energy_lookup

def log_calibrated_energies(args):

    if DATA_PATH_LOCAL.exists():
        log.info('Loading preset from: %s' % DATA_PATH_LOCAL)
        with open(DATA_PATH_LOCAL) as json_file:
            energy_lookup = json.load(json_file)
        log.info('Current calibrated energies:')
        log.info('  %s' % list(energy_lookup['Mono'].keys()))
    else:
        log.error("Missing preset energy file %s" % DATA_PATH_LOCAL) 
        log.error("Run: dmm init")

def delete_energy_from_local_preset(args):

    if DATA_PATH_LOCAL.exists():
        log.info('Loading preset from: %s' % DATA_PATH_LOCAL)
        with open(DATA_PATH_LOCAL) as json_file:
            energy_lookup = json.load(json_file)
        log.info('Current calibrated energies:')
        log.info('  %s' % list(energy_lookup['Mono'].keys()))
        found_energy = any(item in list(energy_lookup['Mono'].keys()) for item in list(energy_lookup['Mono'].keys()) if item == "{:.3f}".format(args.energy))
        if found_energy:
            log.info('%s keV found in the preset energies' % "{:.3f}".format(args.energy))
            energy_lookup['Mono'].pop("{:.3f}".format(args.energy))
            log.info('  %s' % list(energy_lookup['Mono'].keys()))

            log.info('Update local preset file: %s' % DATA_PATH_LOCAL)
            with open(DATA_PATH_LOCAL, "w") as outfile:
                json.dump(energy_lookup, outfile, indent=4)    
        else:
            if args.energy == -1:
                log.error('Please use the --energy option to remove an energy from: %s' % list(energy_lookup['Mono'].keys()))
                log.error('Example: dmm delete --energy %s' % list(energy_lookup['Mono'].keys())[0])
            else:
                log.error('--energy %s in not in the current calibrated energy list' % "{:.3f}".format(args.energy))            
    else:
        log.error("Missing preset energy file %s" % DATA_PATH_LOCAL) 
        log.error("Run: dmm init")
   

def add_pos_dmm_to_local_preset(args):

    if args.energy <= 0:
        log.error('Please use the --energy option to associate an energy value to the current DMM position')
        log.error('Example: dmm add --energy 22.5')
        return

    energy = str('{0:.3f}'.format(np.around(args.energy, decimals=3)))
    epics_pvs = pvs.init(args)
    
    log.warning('add current beamline positions to local preset: %s:' % DATA_PATH_LOCAL)
    
    pos_dmm_energy_select = {}
    pos_dmm_energy_select['Mono'] = {}
    pos_dmm_energy_select['Mono'][energy] = {}

    for key in epics_pvs:
        if 'energy_move' in key or 'energy_pos' in key:
            if args.testing:
                pos_dmm_energy_select['Mono'][energy][key] = 0.0 
            else:
                pos_dmm_energy_select['Mono'][energy][key] = epics_pvs[key].get() 

    log.info('save dmm positions: %s' % pos_dmm_energy_select)

    energy_lookup = load_preset(args)

    energy_list = []

    for key in energy_lookup['Mono']:
        energy_list.append(key)

    if energy in energy_list:
        log.warning('Energy %s keV is a pre-calibrated energy, update DMM positions' % energy)
    else:
        log.info('Energy %s keV is not a pre-calibrated energy, add DMM positions' % energy)

    energy_lookup['Mono'][energy] = pos_dmm_energy_select['Mono'][energy]

    sorted_list = list(map(float, list(energy_lookup['Mono'].keys())))
    sorted_numbers = sorted(sorted_list)
    sorted_strings = ['{:.3f}'.format(x) for x in sorted_numbers]

    energy_lookup_sorted = {}
    energy_lookup_sorted['Mono'] = {i: energy_lookup['Mono'][i] for i in sorted_strings}
    energy_lookup_sorted['Pink'] = {}
    energy_lookup_sorted['Pink']['30.000'] = energy_lookup['Pink']['30.000']
     
    log.info('Update local preset file: %s' % DATA_PATH_LOCAL)
    with open(DATA_PATH_LOCAL, "w") as outfile:
        json.dump(energy_lookup_sorted, outfile, indent=4)        
