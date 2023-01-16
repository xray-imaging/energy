import time

from epics import PV

from dmm2bm import log
from dmm2bm import util

ShutterA_Open_Value  = 1
ShutterA_Close_Value = 0
ShutterB_Open_Value  = 1
ShutterB_Close_Value = 0


def move(pos_dmm_energy_select, params):

    log.info('Moving DMM to: %s' % pos_dmm_energy_select)

    if params.force:
        pass
    else:
        if not util.yes_or_no('Confirm energy change?'):              
            log.info(' ')
            log.warning('   *** Energy not changed')
            return False

    log.info('move motors')

    epics_pvs = init_epics_pvs(params)
    
    close_shutters(pos_dmm_energy_select, epics_pvs, params)
    move_filter(pos_dmm_energy_select, epics_pvs, params)
    move_mirror(pos_dmm_energy_select, epics_pvs, params)

    if(params.mode=="Mono"):
        move_dmm_y(pos_dmm_energy_select, epics_pvs, params)
        move_dmm_arms(pos_dmm_energy_select, epics_pvs, params)
        move_dmm_m2y(pos_dmm_energy_select, epics_pvs, params)
        move_dmm_x(pos_dmm_energy_select, epics_pvs, params)
    elif(params.mode=="Pink" or params.mode=="White"):            
        move_dmm_x(pos_dmm_energy_select, epics_pvs, params)
        move_dmm_y(pos_dmm_energy_select, epics_pvs, params)        

    move_table(pos_dmm_energy_select, epics_pvs, params)
    move_flag(pos_dmm_energy_select, epics_pvs, params)

    energy_pv(pos_dmm_energy_select, epics_pvs, params)

    log.info(' ')
    log.info('   *** Change Energy: Done!  *** ')

    return not params.testing
    

def init_epics_pvs(params):

    epics_pvs = {}

    # 2-BM EPICS PVs
    epics_pvs['ShutterA_Open']            = PV('2bma:A_shutter:open.VAL')
    epics_pvs['ShutterA_Close']           = PV('2bma:A_shutter:close.VAL')
    epics_pvs['ShutterA_Move_Status']     = PV('PA:02BM:STA_A_FES_OPEN_PL')
    epics_pvs['ShutterB_Open']            = PV('2bma:B_shutter:open.VAL')
    epics_pvs['ShutterB_Close']           = PV('2bma:B_shutter:close.VAL')
    epics_pvs['ShutterB_Move_Status']     = PV('PA:02BM:STA_B_SBS_OPEN_PL')

    epics_pvs['filter']                   = PV('2bma:fltr1:select.VAL')
    epics_pvs['mirror_angle']             = PV('2bma:M1angl.VAL')
    epics_pvs['mirror_vertical_position'] = PV('2bma:M1avg.VAL')
    
    epics_pvs['dmm_usx']                  = PV('2bma:m25.VAL')
    epics_pvs['dmm_dsx']                  = PV('2bma:m28.VAL')
    epics_pvs['dmm_usy_ob']               = PV('2bma:m26.VAL')
    epics_pvs['dmm_usy_ib']               = PV('2bma:m27.VAL')
    epics_pvs['dmm_dsy']                  = PV('2bma:m29.VAL')
    epics_pvs['dmm_us_arm']               = PV('2bma:m30.VAL')
    epics_pvs['dmm_ds_arm']               = PV('2bma:m31.VAL')
    epics_pvs['dmm_m2y']                  = PV('2bma:m32.VAL')

    epics_pvs['table_y']                  = PV('2bmb:table3.Y')            
    epics_pvs['flag']                     = PV('2bma:m44.VAL')

    epics_pvs['Energy']                   = PV(params.energyioc_prefix + 'Energy.VAL')
    epics_pvs['Energy_Mode']              = PV(params.energyioc_prefix + 'EnergyMode.VAL')
 
    return epics_pvs


def close_shutters(pos_dmm_energy_select, epics_pvs, params):

    log.info(' ')
    log.info('     *** close_shutters')
    if params.testing:
        log.warning('     *** testing mode - A-shutter will be closed during energy change')
    else:
        log.warning('     *** closing A-shutter')
        epics_pvs['ShutterA_Close'].put(1, wait=True)
        # uncomment and test with beam:
        # util.wait_pv(epics_pvs['ShutterA_Move_Status'], ShutterA_Close_Value)
        log.info('     *** close_shutter A: Done!')

def move_filter(pos_dmm_energy_select, epics_pvs, params):

    log.info(' ')
    log.info('     *** moving filters')

    energy = list(pos_dmm_energy_select.keys())[0]

    try:
        pos_filter = pos_dmm_energy_select[energy]['filter']
        if params.testing:
            log.warning('     *** testing mode:  set filter:  %s ' % pos_filter)
        else:
            log.info('     *** Set filter:  %s ' % pos_filter)
            epics_pvs['filter'].put(pos_filter, wait=True)
    except KeyError:
        log.error('     *** energy positions are intepolated: filter is not moved')


def move_mirror(pos_dmm_energy_select, epics_pvs, params):

    log.info(' ')
    log.info('     *** moving mirror')

    energy = list(pos_dmm_energy_select.keys())[0]
    pos_mirror_vertical_position = pos_dmm_energy_select[energy]['mirror_vertical_position']
    pos_mirror_angle = pos_dmm_energy_select[energy]['mirror_angle']

    if params.testing:
        log.warning('     *** testing mode:  set mirror vertical position %s mm' % pos_mirror_vertical_position)
        log.warning('     *** testing mode:  set mirror angle %s mrad' % pos_mirror_angle)
    else:
        log.info('     *** mirror_vertical_position %s mm' % pos_mirror_vertical_position)
        epics_pvs['mirror_vertical_position'].put(pos_mirror_vertical_position, wait=True)
        time.sleep(1) 
        log.info('     *** mirror_angle %s mrad' % pos_mirror_angle)
        epics_pvs['mirror_angle'].put(pos_mirror_angle, wait=True)
        time.sleep(1) 

def move_dmm_y(pos_dmm_energy_select, epics_pvs, params):

    log.info(' ')
    log.info('     *** moving dmm y')

    energy = list(pos_dmm_energy_select.keys())[0]

    pos_dmm_usy_ob = pos_dmm_energy_select[energy]['dmm_usy_ob']
    pos_dmm_usy_ib = pos_dmm_energy_select[energy]['dmm_usy_ib']
    pos_dmm_dsy    = pos_dmm_energy_select[energy]['dmm_dsy']

    if params.testing:
        log.warning('     *** testing mode:  set dmm usy ob %s mm' % pos_dmm_usy_ob) 
        log.warning('     *** testing mode:  set dmm usy ib %s mm' % pos_dmm_usy_ib)    
        log.warning('     *** testing mode:  set dmm dsy %s mm' % pos_dmm_dsy)        
    else:
        log.info('     *** dmm usy ob %s mm' % pos_dmm_usy_ob) 
        epics_pvs['dmm_usy_ob'].put(pos_dmm_usy_ob, wait=False)
        log.info('     *** dmm usy ib %s mm' % pos_dmm_usy_ib)    
        epics_pvs['dmm_usy_ib'].put(pos_dmm_usy_ib, wait=False)
        log.info('     *** dmm_dsy %s mm' % pos_dmm_dsy)        
        epics_pvs['dmm_dsy'].put(pos_dmm_dsy, wait=True)
        time.sleep(3) 

def move_dmm_arms(pos_dmm_energy_select, epics_pvs, params):

    log.info(' ')
    log.info('     *** moving dmm arms')

    energy = list(pos_dmm_energy_select.keys())[0]

    pos_dmm_us_arm = pos_dmm_energy_select[energy]['dmm_us_arm']
    pos_dmm_ds_arm = pos_dmm_energy_select[energy]['dmm_ds_arm']

    if params.testing:
        log.warning('     *** testing mode:  set DMM dmm_us_arm %s mm' % pos_dmm_us_arm) 
        log.warning('     *** testing mode:  set DMM dmm_ds_arm %s mm' % pos_dmm_ds_arm) 
    else:    
        log.info('     *** moving dmm us arm %s mm' % pos_dmm_us_arm) 
        epics_pvs['dmm_us_arm'].put(pos_dmm_us_arm, wait=False, timeout=1000.0)
        log.info('     *** moving dmm ds arm %s mm' % pos_dmm_ds_arm) 
        epics_pvs['dmm_ds_arm'].put(pos_dmm_ds_arm, wait=True, timeout=1000.0)
        time.sleep(3)

def move_dmm_m2y(pos_dmm_energy_select, epics_pvs, params):    

    log.info(' ')
    log.info('     *** moving dmm m2y')

    energy = list(pos_dmm_energy_select.keys())[0]

    pos_dmm_m2y = pos_dmm_energy_select[energy]['dmm_m2y']

    if params.testing:
        log.warning('     *** testing mode:  set dmm m2y %s mm' % pos_dmm_m2y) 
    else:
        log.info('     *** moving  dmm m2y %s mm' % pos_dmm_m2y) 
        epics_pvs['dmm_m2y'].put(pos_dmm_m2y, wait=True, timeout=1000.0)

def move_dmm_x(pos_dmm_energy_select, epics_pvs, params):

    log.info(' ')
    log.info('     *** moving dmm x')

    energy = list(pos_dmm_energy_select.keys())[0]

    pos_dmm_usx = pos_dmm_energy_select[energy]['dmm_usx']
    pos_dmm_dsx = pos_dmm_energy_select[energy]['dmm_dsx']

    if params.testing:
        log.warning('     *** testing mode:  set dmm usx %s mm' % pos_dmm_usx)
        log.warning('     *** testing mode:  set dmm dsx %s mm' % pos_dmm_dsx)
    else:
        log.info('     *** moving dmm usx %s mm' % pos_dmm_usx)
        epics_pvs['dmm_usx'].put(pos_dmm_usx, wait=False)
        log.info('     *** moving dmm dsx %s mm' % pos_dmm_dsx)
        epics_pvs['dmm_dsx'].put(pos_dmm_dsx, wait=True)
        time.sleep(3) 

def move_table(pos_dmm_energy_select, epics_pvs, params):

    log.info(' ')
    log.info('     *** moving Table Y')

    energy = list(pos_dmm_energy_select.keys())[0]

    pos_table_y = pos_dmm_energy_select[energy]['table_y']

    if params.testing:
        log.warning('     *** testing mode:  set Table Y in station B %s mm' % pos_table_y) 
    else:
        log.info('     *** moving Table Y in station B  %s mm' % pos_table_y) 
        epics_pvs['table_y'].put(pos_table_y, wait=True)

def move_flag(pos_dmm_energy_select, epics_pvs, params):

    log.info(' ')
    log.info('     *** moving Flag')

    energy = list(pos_dmm_energy_select.keys())[0]

    pos_flag = pos_dmm_energy_select[energy]['flag']

    if params.testing:
        log.warning('     *** testing mode:  set Flag y %s mm' % pos_flag) 
    else:
        if pos_flag==0:
            log.warning('Ignore moving Flag since they have not been initialized')
            return

        log.info('     *** moving Flag %s mm'  % pos_flag) 
        epics_pvs['flag'].put(pos_flag, wait=True)

def energy_pv(pos_dmm_energy_select, epics_pvs, params):

    mode   = params.mode
    energy = list(pos_dmm_energy_select.keys())[0]

    log.info(' ')
    log.info('     *** set energy energy and mode PVs')
    log.info('     *** energy PV:      %s' % (params.energyioc_prefix + 'Energy.VAL'))
    log.info('     *** energy Mode PV: %s' % (params.energyioc_prefix + 'EnergyMode.VAL'))

    if params.testing:
        log.warning('     *** testing mode:  set mode   PV: %s' % mode)
        log.warning('     *** testing mode:  set energy PVs %s keV' % energy)
    else:
        log.info('     *** set mode   PV: %s' % mode)
        log.info('     *** set energy PV: %s keV' % energy)
        epics_pvs['Energy_Mode'].put(mode, wait=True)
        epics_pvs['Energy'].put(energy, wait=True)
