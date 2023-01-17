import numpy as np

from dmm2bm import log

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
    value = "{0:4.2f}".format(array[idx])

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
                    log.error('  *** wait_pv(%s, %d, %5.2f reached max timeout. Return False',
                                  epics_pv.pvname, wait_val, timeout)
                    return False
            time.sleep(.01)
        else:
            return True

def interpolate(energy_select, energies, n_steps):

    interp_energies_dict = {}

    keys = list(energies.keys())

    # print(keys[0],                                                keys[1])                                    
    # print(energies[keys[0]]['mirror_angle'],             energies[keys[1]]['mirror_angle'])        
    # print(energies[keys[0]]['mirror_vertical_position'], energies[keys[1]]['mirror_vertical_position'])
    # print(energies[keys[0]]['dmm_usy_ob'],               energies[keys[1]]['dmm_usy_ob'])              
    # print(energies[keys[0]]['dmm_usy_ib'],               energies[keys[1]]['dmm_usy_ib'])              
    # print(energies[keys[0]]['dmm_dsy'],                  energies[keys[1]]['dmm_dsy'])                 
    # print(energies[keys[0]]['dmm_us_arm'],               energies[keys[1]]['dmm_us_arm'])              
    # print(energies[keys[0]]['dmm_ds_arm'],               energies[keys[1]]['dmm_ds_arm'])              
    # print(energies[keys[0]]['dmm_m2y'],                  energies[keys[1]]['dmm_m2y'])                 
    # print(energies[keys[0]]['dmm_usx'],                  energies[keys[1]]['dmm_usx'])                
    # print(energies[keys[0]]['dmm_dsx'],                  energies[keys[1]]['dmm_dsx'])                 
    # print(energies[keys[0]]['table_y'],                  energies[keys[1]]['table_y'])               
    # print(energies[keys[0]]['flag'],                     energies[keys[1]]['flag'])                   

    interp_energies                 = np.linspace(float(keys[0]),                                       float(keys[1]),                                       n_steps)
    interp_mirror_angle             = np.linspace(float(energies[keys[0]]['mirror_angle']),             float(energies[keys[1]]['mirror_angle']),             n_steps)
    interp_mirror_vertical_position = np.linspace(float(energies[keys[0]]['mirror_vertical_position']), float(energies[keys[1]]['mirror_vertical_position']), n_steps)
    interp_dmm_usy_ob               = np.linspace(float(energies[keys[0]]['dmm_usy_ob']),               float(energies[keys[1]]['dmm_usy_ob']),               n_steps)
    interp_dmm_usy_ib               = np.linspace(float(energies[keys[0]]['dmm_usy_ib']),               float(energies[keys[1]]['dmm_usy_ib']),               n_steps)
    interp_dmm_dsy                  = np.linspace(float(energies[keys[0]]['dmm_dsy']),                  float(energies[keys[1]]['dmm_dsy']),                  n_steps) 
    interp_dmm_us_arm               = np.linspace(float(energies[keys[0]]['dmm_us_arm']),               float(energies[keys[1]]['dmm_us_arm']),               n_steps)
    interp_dmm_ds_arm               = np.linspace(float(energies[keys[0]]['dmm_ds_arm']),               float(energies[keys[1]]['dmm_ds_arm']),               n_steps)
    interp_dmm_m2y                  = np.linspace(float(energies[keys[0]]['dmm_m2y']),                  float(energies[keys[1]]['dmm_m2y']),                  n_steps)
    interp_dmm_usx                  = np.linspace(float(energies[keys[0]]['dmm_usx']),                  float(energies[keys[1]]['dmm_usx']),                  n_steps)
    interp_dmm_dsx                  = np.linspace(float(energies[keys[0]]['dmm_dsx']),                  float(energies[keys[1]]['dmm_dsx']),                  n_steps)
    interp_table_y                  = np.linspace(float(energies[keys[0]]['table_y']),                  float(energies[keys[1]]['table_y']),                  n_steps)
    interp_flag                     = np.linspace(float(energies[keys[0]]['flag']),                     float(energies[keys[1]]['flag']),                     n_steps) 

    i = 0
    for energy in interp_energies:
        temp_dict = {}
        temp_dict['mirror_angle']             =  interp_mirror_angle[i]
        temp_dict['mirror_vertical_position'] =  interp_mirror_vertical_position[i]
        temp_dict['dmm_usy_ob']               =  interp_dmm_usy_ob[i]
        temp_dict['dmm_usy_ib']               =  interp_dmm_usy_ib[i]
        temp_dict['dmm_dsy']                  =  interp_dmm_dsy[i]
        temp_dict['dmm_us_arm']               =  interp_dmm_us_arm[i]
        temp_dict['dmm_ds_arm']               =  interp_dmm_ds_arm[i]
        temp_dict['dmm_m2y']                  =  interp_dmm_m2y[i]
        temp_dict['dmm_usx']                  =  interp_dmm_usx[i]
        temp_dict['dmm_dsx']                  =  interp_dmm_dsx[i]
        temp_dict['table_y']                  =  interp_table_y[i]
        temp_dict['flag']                     =  interp_flag[i]

        interp_energies_dict[str(energy)]     = temp_dict

        i += 1

    return interp_energies_dict

def merge(dict1, dict2):

    res = {**dict1, **dict2}

    return res

def closest_value(input_list, input_value):
 
    difference = lambda input_list : abs(float(input_list) - float(input_value))
    res = min(input_list, key=difference)
 
    return res