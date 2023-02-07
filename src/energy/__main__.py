#!/usr/bin/env python

import os
import re
import sys
import argparse
import logging
import time
import shutil
import pathlib
from datetime import datetime
import json 
import numpy as np
import platform

from energy import config
from energy import __version__
from energy import log
from energy import util
from energy import dataio
from energy import move
from energy import pvs

from importlib.resources import files


def init(args):
    if not os.path.exists(str(args.config)):
        config.write(args.config)
        # dataio.init_preset(args)
    else:
        log.error("{0} already exists".format(args.config))

def set_mono(args):

    config.log_values(args)
    args.mode = "Mono"
    energy_select = np.around(args.energy, decimals=3) 
    energy_lookup = dataio.load_preset(args)
    energy_list = []

    for key in energy_lookup['Mono']:
        energy_list.append(key)

    log.info('Selected energy: %4.3f keV'  %  energy_select)
    log.info('Pre-calibrated energies: %s keV' %  energy_list)

    pos_energy_select = {}

    if "{:.3f}".format(energy_select) in energy_list:
        pos_energy_select["{:.3f}".format(energy_select)] = energy_lookup['Mono']["{:.3f}".format(energy_select)]
        log.info('Energy %s keV is a pre-calibrated energy, using lookup table positions' % energy_select)
        if move.motors(pos_energy_select, args):
            config.save_params_to_config(args)
    elif energy_select == -1:
        log.error('Please use the --energy option to select an energy value to move to')
        log.error('Example: energy mono --energy 22.5')
    else:
        log.warning('Energy %s keV is not a pre-calibrated energy, using interpolation' % energy_select)
        energies_str = np.array(energy_list)
        energies_flt = [float(i) for i in  energies_str]
        energy_max = np.max(energies_flt)
        energy_min = np.min(energies_flt)

        if energy_select < energy_max and energy_select >= energy_min:
            energy_calibrated = util.find_nearest(energies_flt, energy_select)
            
            log.info('   ***   Selected energy %s keV; Nearest calibrated: %s keV' % (energy_select, energy_calibrated))

            energy_closer_index  = np.where(energies_str == str(energy_calibrated))[0][0]

            if energy_select >= float(energy_calibrated):
                energy_low  = np.around(float(energies_str[energy_closer_index]), decimals=3)
                energy_high = np.around(float(energies_str[energy_closer_index+1]), decimals=3)
            else:
                energy_low  = np.around(float(energies_str[energy_closer_index-1]), decimals=3)
                energy_high = np.around(float(energies_str[energy_closer_index]), decimals=3)
               
            log.info("   ***   Calibrated range [%4.3f, %4.3f] keV" % (energy_low, energy_high))

            pos_energy_start = {}
            pos_energy_end = {}
            pos_energy_start["{:.3f}".format(energy_low)] = energy_lookup['Mono']["{:.3f}".format(energy_low)]
            pos_energy_end["{:.3f}".format(energy_high)] = energy_lookup['Mono']["{:.3f}".format(energy_high)]
            pos_start_end_energies = util.merge(pos_energy_start, pos_energy_end)
      
            interp_positions = util.interpolate(energy_select, pos_start_end_energies)
            if move.motors(interp_positions, args):
                config.save_params_to_config(args)
        else:
            log.error('Error: energy selected %4.3f is outside the calibrated range [%4.3f, %4.3f]' %(energy_select, energy_min, energy_max))

def run_pink(args):

    config.log_values(args)
    args.mode = "Pink"

    energy_lookup = dataio.load_preset(args)
    pos_energy_select = energy_lookup[args.mode]

    if move.motors(pos_energy_select, args):
        config.save_params_to_config(args)

def run_restore(args):

    if args.force:
        pass
    else:
        if not util.yes_or_no('Confirm restore original preset energy calibration file ?'):              
            log.warning('   *** Original preset energy calibration file NOT restored')
            return
        else:
            log.info(' ')
            log.info('   *** Restoring original preset energy calibration file ...')
    
    dataio.reset_default_to_local_preset()

def run_add(args):

    if args.force:
        pass
    else:
        if not util.yes_or_no('Confirm associate the current beamline positions to --energy ' + str(args.energy) + ' ?'):              
            log.warning('   *** Beamlie position NOT asociated with --energy value ' + str(args.energy))
            return
        else:
            log.info(' ')
            log.info('   *** Beamlie position associated with --energy value ' + str(args.energy))

    dataio.add_pos_to_local_preset(args)

def run_delete(args):

    if args.force:
        pass
    else:
        if not util.yes_or_no('Confirm delete --energy ' + str(args.energy) + ' from the preset energy calibration file ?'):              
            log.warning('   *** --energy %s NOT deleted' % args.energy)
            return
        else:
            log.info(' ')
            log.info('   *** --energy %s deleted' % args.energy)

    dataio.delete_energy_from_local_preset(args)


def run_status(args):

    config.log_values(args)
    dataio.log_calibrated_energies(args)
    pvs.init(args)
    # update energy.conf
    sections = config.MONO_PARAMS
    config.write(args.config, args=args, sections=sections)

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('--config', **config.SECTIONS['general']['config'])
    parser.add_argument('--version', action='version',
                        version='%(prog)s {}'.format(__version__))

    mono_params = config.MONO_PARAMS    
    pink_params = config.PINK_PARAMS    
    
    cmd_parsers = [
        ('init',        init,           (),           "Usage: energy init                - Create configuration file and restore the original preset energy calibration file"),
        ('set',         set_mono,       mono_params,  "Usage: energy set    --energy 20  - Set the beamline to the --energy value using a precalibrated list or, if missing, a linear interpolation point between the two closest calibrared values"),
        ('pink',        run_pink,       pink_params,  "Usage: energy pink                - Set the beamline to pink mode "),
        ('add',         run_add,        mono_params,  "Usage: energy add    --energy 20  - Associate the current beamline positions to --energy value"),             
        ('delete',      run_delete,     mono_params,  "Usage: energy delete --energy 20  - Delete --energy value from the preset energy calibration file"),             
        ('restore',     run_restore,    mono_params,  "Usage: energy restore             - Restore original preset energy calibration file. "),
        ('status',      run_status,     mono_params,  "Usage: energy status              - Show status"),
    ]

    subparsers = parser.add_subparsers(title="Commands", metavar='')

    for cmd, func, sections, text in cmd_parsers:
        cmd_params = config.Params(sections=sections)
        cmd_parser = subparsers.add_parser(cmd, help=text, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
        cmd_parser = cmd_params.add_arguments(cmd_parser)
        cmd_parser.set_defaults(_func=func)

    args = config.parse_known_args(parser, subparser=True)
    print('***************************')
    print('***************************')
    print(args)
    print('***************************')
    print('***************************')
    # create logger
    logs_home = args.logs_home

    # make sure logs directory exists
    if not os.path.exists(logs_home):
        os.makedirs(logs_home)

    lfname = os.path.join(logs_home, 'energy_' + datetime.strftime(datetime.now(), "%Y-%m-%d_%H_%M_%S") + '.log')
 
    log.setup_custom_logger(lfname)
    log.info("Saving log at %s" % lfname)

    try:
        args._func(args)
    except RuntimeError as e:
        log.error(str(e))
        sys.exit(1)

if __name__ == '__main__':
    main()
