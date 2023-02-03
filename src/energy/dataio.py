import os
import json
import pathlib
import platform

import numpy as np

from importlib.resources import files

from energy import log
from energy import pvs

DATA_PATH = pathlib.Path(pathlib.Path(__file__).parent, 'data')
DATA_PATH_LOCAL = pathlib.Path(pathlib.Path.home(), 'logs')

def init_preset(args):
    reset_default_to_local_preset(args)

def load_preset(args):

    run_time_data_file     = pathlib.Path(DATA_PATH_LOCAL, 'energy' + args.beamline + '.json')

    if run_time_data_file.exists():
        log.info('Loading preset from: %s' % run_time_data_file)
        with open(run_time_data_file) as json_file:
            energy_lookup = json.load(json_file)
    else:
        energy_lookup = reset_default_to_local_preset(args)
    return energy_lookup

def reset_default_to_local_preset(args):

    run_time_data_file     = pathlib.Path(DATA_PATH_LOCAL, 'energy' + args.beamline + '.json')
    install_time_data_file = pathlib.Path(DATA_PATH,       'energy' + args.beamline + '.json')

    log.info('Loading preset from: %s' % install_time_data_file)
    with open(install_time_data_file) as json_file:
        energy_lookup = json.load(json_file)
    log.info('Create local preset file: %s' % run_time_data_file)
    with open(run_time_data_file, "w") as outfile:
        json.dump(energy_lookup, outfile, indent=4)        

    return energy_lookup

def log_calibrated_energies(args):

    run_time_data_file     = pathlib.Path(DATA_PATH_LOCAL, 'energy' + args.beamline + '.json')

    if run_time_data_file.exists():
        log.info('Loading preset from: %s' % run_time_data_file)
        with open(run_time_data_file) as json_file:
            energy_lookup = json.load(json_file)
        log.info('Current calibrated energies:')
        log.info('  %s' % list(energy_lookup['Mono'].keys()))
    else:
        log.error("Missing preset energy file %s" % run_time_data_file) 
        log.error("Run: energy init")

def delete_energy_from_local_preset(args):

    run_time_data_file     = pathlib.Path(DATA_PATH_LOCAL, 'energy' + args.beamline + '.json')

    if run_time_data_file.exists():
        log.info('Loading preset from: %s' % run_time_data_file)
        with open(run_time_data_file) as json_file:
            energy_lookup = json.load(json_file)
        log.info('Current calibrated energies:')
        log.info('  %s' % list(energy_lookup['Mono'].keys()))
        found_energy = any(item in list(energy_lookup['Mono'].keys()) for item in list(energy_lookup['Mono'].keys()) if item == "{:.3f}".format(args.energy))
        if found_energy:
            log.info('%s keV found in the preset energies' % "{:.3f}".format(args.energy))
            energy_lookup['Mono'].pop("{:.3f}".format(args.energy))
            log.info('  %s' % list(energy_lookup['Mono'].keys()))

            log.info('Update local preset file: %s' % run_time_data_file)
            with open(run_time_data_file, "w") as outfile:
                json.dump(energy_lookup, outfile, indent=4)    
        else:
            if args.energy == -1:
                log.error('Please use the --energy option to remove an energy from: %s' % list(energy_lookup['Mono'].keys()))
                log.error('Example: energy delete --energy %s' % list(energy_lookup['Mono'].keys())[0])
            else:
                log.error('--energy %s in not in the current calibrated energy list' % "{:.3f}".format(args.energy))            
    else:
        log.error("Missing preset energy file %s" % run_time_data_file) 
        log.error("Run: energy init")
   

def add_pos_to_local_preset(args):

    if args.energy <= 0:
        log.error('Please use the --energy option to associate an energy value to the current motors position')
        log.error('Example: energy add --energy 22.5')
        return

    energy = str('{0:.3f}'.format(np.around(args.energy, decimals=3)))
    epics_pvs = pvs.init(args)

    run_time_data_file     = pathlib.Path(DATA_PATH_LOCAL, 'energy' + args.beamline + '.json')
    
    log.warning('add current beamline positions to local preset: %s:' % run_time_data_file)
    
    pos_energy_select = {}
    pos_energy_select['Mono'] = {}
    pos_energy_select['Mono'][energy] = {}

    for key in epics_pvs:
        if 'energy_move' in key or 'energy_pos' in key:
            if args.testing:
                pos_energy_select['Mono'][energy][key] = 0.0 
            else:
                pos_energy_select['Mono'][energy][key] = epics_pvs[key].get() 

    log.info('save energy positions: %s' % pos_energy_select)

    energy_lookup = load_preset(args)

    energy_list = []

    for key in energy_lookup['Mono']:
        energy_list.append(key)

    if energy in energy_list:
        log.warning('Energy %s keV is a pre-calibrated energy, update energy positions' % energy)
    else:
        log.info('Energy %s keV is not a pre-calibrated energy, add energy positions' % energy)

    energy_lookup['Mono'][energy] = pos_energy_select['Mono'][energy]

    sorted_list = list(map(float, list(energy_lookup['Mono'].keys())))
    sorted_numbers = sorted(sorted_list)
    sorted_strings = ['{:.3f}'.format(x) for x in sorted_numbers]

    energy_lookup_sorted = {}
    energy_lookup_sorted['Mono'] = {i: energy_lookup['Mono'][i] for i in sorted_strings}
    energy_lookup_sorted['Pink'] = {}
    energy_lookup_sorted['Pink']['30.000'] = energy_lookup['Pink']['30.000']
     
    log.info('Update local preset file: %s' % run_time_data_file)
    with open(run_time_data_file, "w") as outfile:
        json.dump(energy_lookup_sorted, outfile, indent=4)        
