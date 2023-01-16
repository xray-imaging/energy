import os
import sys
import shutil
import pathlib
import argparse
import configparser
import numpy as np
from pathlib import Path

from collections import OrderedDict
from datetime import datetime

from dmm2bm import log
from dmm2bm import util
from dmm2bm import epics
from dmm2bm import __version__

LOGS_HOME = os.path.join(str(pathlib.Path.home()), 'logs')
CONFIG_FILE_NAME = os.path.join(str(pathlib.Path.home()), 'logs/dmm.conf')

data_path = Path(__file__).parent / 'data'

SECTIONS = OrderedDict()

SECTIONS['general'] = {
    'config': {
        'default': CONFIG_FILE_NAME,
        'type': str,
        'help': "File name of configuration file",
        'metavar': 'FILE'},
    'logs-home': {
        'default': LOGS_HOME,
        'type': str,
        'help': "Log file directory",
        'metavar': 'FILE'},
    'verbose': {
        'default': False,
        'help': 'Verbose output',
        'action': 'store_true'},
    'testing': {
        'default': False,
        'help': 'Enable test mode to show DMM new motor positions. The DMM motors will not move',
        'action': 'store_true'},
    'force': {
        'default': False,
        'help': 'When set the enegy change will occurs without a confirmation request',
        'action': 'store_true'},
        }

SECTIONS['energy'] = {
    'energy': {
        'default': -1,
        'type': float,
        'help': "Desired double crystal multilayer (DMM) monochromator energy. Default (-1) = Pink beam"},
        }


SECTIONS['energyioc'] = {
    'energyioc-prefix':{
        'default': '2bm:MCTOptics:',
        'type': str,
        'help': "The epics IOC hosting the Energy PV, i.e.'2bm:MCTOptics:' "},
    }

MONO_PARAMS = ('energy', 'energyioc')
PINK_PARAMS = ('energyioc', )

NICE_NAMES = ('General', 'DMM Energy', 'Energy IOC')


def get_config_name():
    """Get the command line --config option."""
    name = CONFIG_FILE_NAME
    for i, arg in enumerate(sys.argv):
        if arg.startswith('--config'):
            if arg == '--config':
                return sys.argv[i + 1]
            else:
                name = sys.argv[i].split('--config')[1]
                if name[0] == '=':
                    name = name[1:]
                return name
    return name

def parse_known_args(parser, subparser=False):
    """
    Parse arguments from file and then override by the ones specified on the
    command line. Use *parser* for parsing and is *subparser* is True take into
    account that there is a value on the command line specifying the subparser.
    """
    if len(sys.argv) > 1:
        subparser_value = [sys.argv[1]] if subparser else []
        config_values = config_to_list(config_name=get_config_name())
        values = subparser_value + config_values + sys.argv[1:]
        #print(subparser_value, config_values, values)
    else:
        values = ""

    return parser.parse_known_args(values)[0]

def config_to_list(config_name=CONFIG_FILE_NAME):
    """
    Read arguments from config file and convert them to a list of keys and
    values as sys.argv does when they are specified on the command line.
    *config_name* is the file name of the config file.
    """
    result = []
    config = configparser.ConfigParser()

    if not config.read([config_name]):
        return []

    for section in SECTIONS:
        for name, opts in ((n, o) for n, o in SECTIONS[section].items() if config.has_option(section, n)):
            value = config.get(section, name)

            if value != '' and value != 'None':
                action = opts.get('action', None)

                if action == 'store_true' and value == 'True':
                    # Only the key is on the command line for this action
                    result.append('--{}'.format(name))

                if not action == 'store_true':
                    if opts.get('nargs', None) == '+':
                        result.append('--{}'.format(name))
                        result.extend((v.strip() for v in value.split(',')))
                    else:
                        result.append('--{}={}'.format(name, value))

    return result
  
class Params(object):
    def __init__(self, sections=()):
        self.sections = sections + ('general', )

    def add_parser_args(self, parser):
        for section in self.sections:
            for name in sorted(SECTIONS[section]):
                opts = SECTIONS[section][name]
                parser.add_argument('--{}'.format(name), **opts)

    def add_arguments(self, parser):
        self.add_parser_args(parser)
        return parser

    def get_defaults(self):
        parser = argparse.ArgumentParser()
        self.add_arguments(parser)

        return parser.parse_args('')

def write(config_file, args=None, sections=None):
    """
    Write *config_file* with values from *args* if they are specified,
    otherwise use the defaults. If *sections* are specified, write values from
    *args* only to those sections, use the defaults on the remaining ones.
    """
    config = configparser.ConfigParser()
    for section in SECTIONS:
        config.add_section(section)
        for name, opts in SECTIONS[section].items():
            if args and sections and section in sections and hasattr(args, name.replace('-', '_')):
                value = getattr(args, name.replace('-', '_'))
                if isinstance(value, list):
                    # print(type(value), value)
                    value = ', '.join(value)
            else:
                value = opts['default'] if opts['default'] is not None else ''

            prefix = '# ' if value == '' else ''

            if name != 'config':
                config.set(section, prefix + name, str(value))
    #print(args.energy_value)
    with open(config_file, 'w') as f:        
        config.write(f)

def log_values(args):
    """Log all values set in the args namespace.

    Arguments are grouped according to their section and logged alphabetically
    using the DEBUG log level thus --verbose is required.
    """
    args = args.__dict__

    log.warning('energy status start')
    for section, name in zip(SECTIONS, NICE_NAMES):
        entries = sorted((k for k in args.keys() if k.replace('_', '-') in SECTIONS[section]))

        # print('log_values', section, name, entries)
        if entries:
            log.info(name)

            for entry in entries:
                value = args[entry] if args[entry] is not None else "-"
                if (value == 'none'):
                    log.warning("  {:<16} {}".format(entry, value))
                elif (value is not False):
                    log.info("  {:<16} {}".format(entry, value))
                elif (value is False):
                    log.warning("  {:<16} {}".format(entry, value))

    log.warning('energy status end')

def save_params_to_config(args):

    # Update current status in default config file.
    # The default confign file name is set in CONFIG_FILE_NAME
    sections = MONO_PARAMS
    write(CONFIG_FILE_NAME, args=args, sections=sections)
    log.info('  *** saved to %s ' % (CONFIG_FILE_NAME))
    
def save_current_positions_to_config(args):

    energy_change_PVs = epics.init_energy_change_PVs(args)
    log.warning('save current beamline positions to config')
    args.mirror_angle               = energy_change_PVs['mirror_angle'].get()            
    args.mirror_vertical_position   = energy_change_PVs['mirror_vertical_position'].get()
    args.dmm_usy_ob                 = energy_change_PVs['dmm_usy_ob'].get()              
    args.dmm_usy_ib                 = energy_change_PVs['dmm_usy_ib'].get()              
    args.dmm_dsy                    = energy_change_PVs['dmm_dsy'].get()                 
    args.dmm_us_arm                 = energy_change_PVs['dmm_us_arm'].get()              
    args.dmm_ds_arm                 = energy_change_PVs['dmm_ds_arm'].get()              
    args.dmm_m2y                    = energy_change_PVs['dmm_m2y'].get()                 
    args.dmm_usx                    = energy_change_PVs['dmm_usx'].get()                 
    args.dmm_dsx                    = energy_change_PVs['dmm_dsx'].get()                 
    args.filter                     = energy_change_PVs['filter'].get()  
    args.table_y                    = energy_change_PVs['table_y'].get()  
    args.flag                       = energy_change_PVs['flag'].get()  

    # Store status in a unique config file for later re-use. 
    # The unique file name is:
    # energy2bm_mode_energy_yyyy-mm-dd_hh_mm_ss.conf
    sections = MONO_PARAMS
    head, tail = os.path.splitext(args.config)
    now = datetime.strftime(datetime.now(), "%Y-%m-%d_%H_%M_%S")

    config_name_energy = head + '_' + args.mode +'_' + str(args.energy_value) + '_' + now + tail
    write(config_name_energy, args=args, sections=sections)
    log.info('  *** saved to %s ' % (config_name_energy))

def set_default_config(params):
    log.info('set default motor values')
    # Load DMM lookup table from the JSON file
    with open(os.path.join(data_path, 'dmm.json')) as json_file:
        lookup = json.load(json_file)
    energies_str = np.array(list(lookup[params.mode].keys())[:])
    energies_flt = [float(i) for i in  energies_str]
    energy_calibrated = util.find_nearest(energies_flt, params.energy_value)
    if float(params.energy_value) != float(energy_calibrated):
        log.warning('   *** Energy requested is %s keV, the closest calibrated energy is %s' % (params.energy_value, energy_calibrated))
        log.info('   *** Options are %s keV' % (energies_str))
        log.info('   *** Energy is set at %s keV' % params.energy_value)   
        log.info('   *** Move to %s keV instead of %s?' % (energy_calibrated, params.energy_value))  
    log.info('   *** Change Energy for %s as %s *** ' % (params.mode, energy_calibrated) )

    params.energy_value = energy_calibrated

    # set dmm motor and beamline positons
    params.mirror_angle = lookup[params.mode][energy_calibrated]["mirror_angle"]
    params.mirror_vertical_position = lookup[params.mode][energy_calibrated]["mirror_vertical_position"]
    params.dmm_usy_ob = lookup[params.mode][energy_calibrated]["dmm_usy_ob"] 
    params.dmm_usy_ib = lookup[params.mode][energy_calibrated]["dmm_usy_ib"]
    params.dmm_dsy = lookup[params.mode][energy_calibrated]["dmm_dsy"]

    if(params.mode=="Mono"):
        params.dmm_us_arm = lookup[params.mode][energy_calibrated]["dmm_us_arm"]                
        params.dmm_ds_arm = lookup[params.mode][energy_calibrated]["dmm_ds_arm"]
        params.dmm_m2y = lookup[params.mode][energy_calibrated]["dmm_m2y"]

    params.dmm_usx = lookup[params.mode][energy_calibrated]["dmm_usx"]
    params.dmm_dsx = lookup[params.mode][energy_calibrated]["dmm_dsx"]
    params.filter = lookup[params.mode][energy_calibrated]["filter"]   
    params.table_y = lookup[params.mode][energy_calibrated]["table_y"]   
    params.flag = lookup[params.mode][energy_calibrated]["flag"]   
    return 0
