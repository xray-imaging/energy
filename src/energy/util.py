import re
import time

import numpy as np

from energy import log

EPSILON = 0.01

def positive_int(value):
    """Convert *value* to an integer and make sure it is positive."""
    result = int(value)
    if result < 0:
        raise argparse.ArgumentTypeError('Only positive integers are allowed')

    return result

def yes_or_no(question):
    answer = str(input(question + " (Y/N): ")).lower().strip()
    while not(answer == "y" or answer == "yes" or answer == "n" or answer == "no"):
        log.warning("Input yes or no")
        answer = str(input(question + "(Y/N): ")).lower().strip()
    if answer[0] == "y":
        return True
    else:
        return False

def find_nearest(array, value):

    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    value = "{0:4.3f}".format(array[idx])

    return value

def wait_pv(epics_pv, wait_val, timeout=-1):
    """Wait on a pv to be a value until max_timeout (default forever)
       delay for pv to change
    """

    time.sleep(.01)
    start_time = time.time()
    while True:
        pv_val = epics_pv.get()
        if isinstance(pv_val, float):
            if abs(pv_val - wait_val) < EPSILON:
                return True
        if pv_val != wait_val:
            if timeout > -1:
                current_time = time.time()
                diff_time = current_time - start_time
                if diff_time >= timeout:
                    log.error('  *** wait_pv(%s, %d, %5.3f reached max timeout. Return False',
                                  epics_pv.pvname, wait_val, timeout)
                    return False
            time.sleep(.01)
        else:
            return True

def interpolate(energy_select, energies):

    energy      = list(energies.keys())
    energy_low  = float(energy[0])
    energy_high = float(energy[1])

    temp_dict = {}
    interp_energy_dict = {}

    for key in energies[energy[0]]:
        if 'energy_move' in key:
             temp_dict[key] = energies[energy[0]][key] + ((energy_select - energy_low) / (energy_high - energy_low) * (energies[energy[1]][key] - energies[energy[0]][key]))
    
    interp_energy_dict["{:.3f}".format(energy_select)] = temp_dict

    return interp_energy_dict

def merge(dict1, dict2):

    res = {**dict1, **dict2}

    return res

def closest_value(input_list, input_value):
 
    difference = lambda input_list : abs(float(input_list) - float(input_value))
    res = min(input_list, key=difference)
 
    return res

def clean(s):

    # Remove all non-word characters (everything except numbers and letters)
    s = re.sub(r"[^\w\s]", '', s)

    # Replace all runs of whitespace with a single dash
    s = re.sub(r"\s+", '_', s)

    # lower case
    s = s.lower()
    return s