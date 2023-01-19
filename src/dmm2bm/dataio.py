import os
import json
import pathlib
import platform

import numpy as np

from importlib.resources import files

from dmm2bm import log
from dmm2bm import epics

DATA_PATH = pathlib.Path(pathlib.Path(__file__).parent, 'data', 'dmm.json')
DATA_PATH_LOCAL = pathlib.Path(pathlib.Path.home(), 'logs', 'dmm.json')

def init_preset():
    reset_default_to_local_preset()

def load_preset():
    if DATA_PATH_LOCAL.exists():
        log.info('Loading preset from: %s' % DATA_PATH_LOCAL)
        with open(DATA_PATH_LOCAL) as json_file:
            energy_lookup = json.load(json_file)
    else:
        energy_lookup = reset_default_to_local_preset()
    return energy_lookup

def reset_default_to_local_preset():

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
        found_energy = any(item in list(energy_lookup['Mono'].keys()) for item in list(energy_lookup['Mono'].keys()) if item == "{:.2f}".format(args.energy))
        if found_energy:
            log.info('%s keV found in the preset energies' % "{:.2f}".format(args.energy))
            energy_lookup['Mono'].pop("{:.2f}".format(args.energy))
            log.info('  %s' % list(energy_lookup['Mono'].keys()))

            log.info('Update local preset file: %s' % DATA_PATH_LOCAL)
            with open(DATA_PATH_LOCAL, "w") as outfile:
                json.dump(energy_lookup, outfile, indent=4)    
        else:
            log.error('--energy %s in not in the current calibrated energy list' % "{:.2f}".format(args.energy))
    else:
        log.error("Missing preset energy file %s" % DATA_PATH_LOCAL) 
        log.error("Run: dmm init")
   

def add_pos_dmm_to_local_preset(args):

    if args.energy <= 0:
        log.error('--energy %.2f in not allowed' % args.energy)
        return

    energy = str('{0:.2f}'.format(np.around(args.energy, decimals=2)))
    epics_pvs = epics.init_epics_pvs(args)
    
    log.warning('add current beamline positions to local preset: %s:' % DATA_PATH_LOCAL)
    
    if args.testing:
        pos_mirror_angle               = 0.0
        pos_mirror_vertical_position   = 0.0
        pos_dmm_usy_ob                 = 0.0
        pos_dmm_usy_ib                 = 0.0
        pos_dmm_dsy                    = 0.0
        pos_dmm_us_arm                 = 0.0
        pos_dmm_ds_arm                 = 0.0
        pos_dmm_m2y                    = 0.0
        pos_dmm_usx                    = 0.0
        pos_dmm_dsx                    = 0.0
        pos_filter                     = 0.0
        pos_table_y                    = 0.0
        pos_flag                       = 0.0
    else:
        pos_mirror_angle               = epics_pvs['mirror_angle'].get()            
        pos_mirror_vertical_position   = epics_pvs['mirror_vertical_position'].get()
        pos_dmm_usy_ob                 = epics_pvs['dmm_usy_ob'].get()              
        pos_dmm_usy_ib                 = epics_pvs['dmm_usy_ib'].get()              
        pos_dmm_dsy                    = epics_pvs['dmm_dsy'].get()                 
        pos_dmm_us_arm                 = epics_pvs['dmm_us_arm'].get()              
        pos_dmm_ds_arm                 = epics_pvs['dmm_ds_arm'].get()              
        pos_dmm_m2y                    = epics_pvs['dmm_m2y'].get()                 
        pos_dmm_usx                    = epics_pvs['dmm_usx'].get()                 
        pos_dmm_dsx                    = epics_pvs['dmm_dsx'].get()                 
        pos_filter                     = epics_pvs['filter'].get()  
        pos_table_y                    = epics_pvs['table_y'].get()  
        pos_flag                       = epics_pvs['flag'].get()  

    pos_dmm_energy_select = {}
    pos_dmm_energy_select['Mono'] = {}
    pos_dmm_energy_select['Mono'][energy] = {}
    pos_dmm_energy_select['Mono'][energy]['mirror_angle']             = pos_mirror_angle            
    pos_dmm_energy_select['Mono'][energy]['mirror_vertical_position'] = pos_mirror_vertical_position
    pos_dmm_energy_select['Mono'][energy]['dmm_usy_ob']               = pos_dmm_usy_ob              
    pos_dmm_energy_select['Mono'][energy]['dmm_usy_ib']               = pos_dmm_usy_ib              
    pos_dmm_energy_select['Mono'][energy]['dmm_dsy']                  = pos_dmm_dsy                 
    pos_dmm_energy_select['Mono'][energy]['dmm_us_arm']               = pos_dmm_us_arm              
    pos_dmm_energy_select['Mono'][energy]['dmm_ds_arm']               = pos_dmm_ds_arm              
    pos_dmm_energy_select['Mono'][energy]['dmm_m2y']                  = pos_dmm_m2y                 
    pos_dmm_energy_select['Mono'][energy]['dmm_usx']                  = pos_dmm_usx                 
    pos_dmm_energy_select['Mono'][energy]['dmm_dsx']                  = pos_dmm_dsx                 
    pos_dmm_energy_select['Mono'][energy]['filter']                   = pos_filter                  
    pos_dmm_energy_select['Mono'][energy]['table_y']                  = pos_table_y                 
    pos_dmm_energy_select['Mono'][energy]['flag']                     = pos_flag                        

    log.info('save dmm positions: %s' % pos_dmm_energy_select)

    energy_lookup = load_preset()

    energy_list = []

    for key in energy_lookup['Mono']:
        energy_list.append(key)

    if energy in energy_list:
        log.warning('Energy %s keV is a pre-calibrated energy, update DMM positions' % energy)
    else:
        log.info('Energy %s keV is not a pre-calibrated energy, add DMM positions' % energy)

    energy_lookup['Mono'][energy] = pos_dmm_energy_select['Mono'][energy]

    myKeys = list(energy_lookup['Mono'].keys())
    myKeys.sort()
    energy_lookup_sorted = {}
    energy_lookup_sorted['Mono'] = {i: energy_lookup['Mono'][i] for i in myKeys}
    energy_lookup_sorted['Pink'] = {}
    energy_lookup_sorted['Pink']['30.00'] = energy_lookup['Pink']['30.00']
     
    log.info('Update local preset file: %s' % DATA_PATH_LOCAL)
    with open(DATA_PATH_LOCAL, "w") as outfile:
        json.dump(energy_lookup_sorted, outfile, indent=4)        

