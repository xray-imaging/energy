import os
import json
import pathlib

import numpy as np

from importlib.resources import files

from dmm2bm import log
from dmm2bm import epics

def load_preset():

    data_path = pathlib.Path(pathlib.Path(__file__).parent, 'data', 'dmm.json')    
    data_path_local = pathlib.Path(pathlib.Path.home(), 'logs', 'dmm.json')
    
    if data_path_local.exists():
        log.info('Local preset file exists: %s' % data_path_local)
        log.info('Loading preset from: %s' % data_path_local)
        with open(data_path_local) as json_file:
            energy_lookup = json.load(json_file)
    else:
        energy_lookup = reset_preset_to_local()
    return energy_lookup

def reset_preset_to_local():

    data_path = pathlib.Path(pathlib.Path(__file__).parent, 'data', 'dmm.json')    
    data_path_local = pathlib.Path(pathlib.Path.home(), 'logs', 'dmm.json')

    log.info('Using preset file: %s' % data_path)
    log.info('Loading preset from: %s' % data_path)
    with open(data_path) as json_file:
        energy_lookup = json.load(json_file)
    log.info('Create local preset file: %s' % data_path_local)
    with open(data_path_local, "w") as outfile:
        json.dump(energy_lookup, outfile, indent=4)        

    return energy_lookup

def add_pos_dmm_to_local_preset(args):

    if args.energy <= 0:
        log.error('--energy %.2f in not allowed' % args.energy)
        return

    energy = str('{0:.2f}'.format(np.around(args.energy, decimals=2)))
    epics_pvs = epics.init_epics_pvs(args)
    
    data_path_local = pathlib.Path(pathlib.Path.home(), 'logs', 'dmm.json')

    log.warning('add current beamline positions to local preset: %s:' % data_path_local)
    
    if args.testing:
        pos_mirror_angle               = 15.0
        pos_mirror_vertical_position   = 15.0
        pos_dmm_usy_ob                 = 15.0
        pos_dmm_usy_ib                 = 15.0
        pos_dmm_dsy                    = 15.0
        pos_dmm_us_arm                 = 15.0
        pos_dmm_ds_arm                 = 15.0
        pos_dmm_m2y                    = 15.0
        pos_dmm_usx                    = 15.0
        pos_dmm_dsx                    = 15.0
        pos_filter                     = 15.0
        pos_table_y                    = 15.0
        pos_flag                       = 15.0
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
     
    log.info('Update local preset file: %s' % data_path_local)
    with open(data_path_local, "w") as outfile:
        json.dump(energy_lookup_sorted, outfile, indent=4)        