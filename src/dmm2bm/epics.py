import time

from epics import PV

from dmm2bm import log
from dmm2bm import util

ShutterA_Open_Value  = 1
ShutterA_Close_Value = 0
ShutterB_Open_Value  = 1
ShutterB_Close_Value = 0


def move(params):

    if params.force:
        pass
    else:
        if not util.yes_or_no('Confirm energy change?'):              
            log.info(' ')
            log.warning('   *** Energy not changed')
            return False

    log.info('move motors')

    energy_change_PVs = epics.init_energy_change_PVs(params)
    
    epics.close_shutters(energy_change_PVs, params)
    epics.move_filter(energy_change_PVs, params)
    epics.move_mirror(energy_change_PVs, params)

    if(params.mode=="Mono"):
        epics.move_dmm_y(energy_change_PVs, params)
        epics.move_dmm_arms(energy_change_PVs, params)
        epics.move_dmm_m2y(energy_change_PVs, params)
        epics.move_dmm_x(energy_change_PVs, params)
    elif(params.mode=="Pink" or params.mode=="White"):            
        epics.move_dmm_x(energy_change_PVs, params)
        epics.move_dmm_y(energy_change_PVs, params)        

    epics.move_table(energy_change_PVs, params)
    epics.move_flag(energy_change_PVs, params)

    epics.energy_pv(energy_change_PVs, params)

    log.info(' ')
    log.info('   *** Change Energy: Done!  *** ')
    return True
    

def init_energy_change_PVs(params):

    energy_change_PVs = {}

    log.info('     *** testing mode:  set PVs')
    log.warning('     *** energy PVs: %s' % (params.energyioc_prefix + 'Energy.VAL'))
    log.warning('     *** energy PVs: %s' % (params.energyioc_prefix + 'EnergyMode.VAL'))
    
    # 2-BM EPICS PVs
    energy_change_PVs['ShutterA_Open']            = PV('2bma:A_shutter:open.VAL')
    energy_change_PVs['ShutterA_Close']           = PV('2bma:A_shutter:close.VAL')
    energy_change_PVs['ShutterA_Move_Status']     = PV('PA:02BM:STA_A_FES_OPEN_PL')
    energy_change_PVs['ShutterB_Open']            = PV('2bma:B_shutter:open.VAL')
    energy_change_PVs['ShutterB_Close']           = PV('2bma:B_shutter:close.VAL')
    energy_change_PVs['ShutterB_Move_Status']     = PV('PA:02BM:STA_B_SBS_OPEN_PL')

    energy_change_PVs['filter']                   = PV('2bma:fltr1:select.VAL')
    energy_change_PVs['mirror_angle']             = PV('2bma:M1angl.VAL')
    energy_change_PVs['mirror_vertical_position'] = PV('2bma:M1avg.VAL')
    
    energy_change_PVs['dmm_usx']                  = PV('2bma:m25.VAL')
    energy_change_PVs['dmm_dsx']                  = PV('2bma:m28.VAL')
    energy_change_PVs['dmm_usy_ob']               = PV('2bma:m26.VAL')
    energy_change_PVs['dmm_usy_ib']               = PV('2bma:m27.VAL')
    energy_change_PVs['dmm_dsy']                  = PV('2bma:m29.VAL')
    energy_change_PVs['dmm_us_arm']               = PV('2bma:m30.VAL')
    energy_change_PVs['dmm_ds_arm']               = PV('2bma:m31.VAL')
    energy_change_PVs['dmm_m2y']                  = PV('2bma:m32.VAL')

    energy_change_PVs['table_y']                  = PV('2bmb:table3.Y')            
    energy_change_PVs['flag']                     = PV('2bma:m44.VAL')

    energy_change_PVs['Energy']                   = PV(params.energyioc_prefix + 'Energy.VAL')
    energy_change_PVs['Energy_Mode']              = PV(params.energyioc_prefix + 'EnergyMode.VAL')
 
    return energy_change_PVs

def energy_pv(energy_change_PVs, params):

    if params.testing:
        log.info('     *** testing mode:  set tomoScan energy and mode PVs')
    else:
        energy_change_PVs['Energy_Mode'].put(params.mode, wait=True)
        energy_change_PVs['Energy'].put(params.energy_value, wait=True)

def move_filter(energy_change_PVs, params):

    log.info(' ')
    log.info('     *** moving filters')

    if params.testing:
        log.warning('     *** testing mode:  set filter:  %s ' % params.filter)
    else:
        log.info('     *** Set filter:  %s ' % params.filter)
        energy_change_PVs['filter'].put(params.filter, wait=True)

def move_mirror(energy_change_PVs, params):

    log.info(' ')
    log.info('     *** moving mirror')

    if params.testing:
        log.warning('     *** testing mode:  set mirror vertical position %s mm' % params.mirror_vertical_position)
        log.warning('     *** testing mode:  set mirror angle %s mrad' % params.mirror_angle)
    else:
        log.info('     *** mirror_vertical_position %s mm' % params.mirror_vertical_position)
        energy_change_PVs['mirror_vertical_position'].put(params.mirror_vertical_position, wait=True)
        time.sleep(1) 
        log.info('     *** mirror_angle %s mrad' % params.mirror_angle)
        energy_change_PVs['mirror_angle'].put(params.mirror_angle, wait=True)
        time.sleep(1) 

def move_dmm_y(energy_change_PVs, params):

    log.info(' ')
    log.info('     *** moving dmm y')

    if params.testing:
        log.warning('     *** testing mode:  set dmm usy ob %s mm' % params.dmm_usy_ob) 
        log.warning('     *** testing mode:  set dmm usy ib %s mm' % params.dmm_usy_ib)    
        log.warning('     *** testing mode:  set dmm dsy %s mm' % params.dmm_dsy)        
    else:
        log.info('     *** dmm usy ob %s mm' % params.dmm_usy_ob) 
        energy_change_PVs['dmm_usy_ob'].put(params.dmm_usy_ob, wait=False)
        log.info('     *** dmm usy ib %s mm' % params.dmm_usy_ib)    
        energy_change_PVs['dmm_usy_ib'].put(params.dmm_usy_ib, wait=False)
        log.info('     *** dmm_dsy %s mm' % params.dmm_dsy)        
        energy_change_PVs['dmm_dsy'].put(params.dmm_dsy, wait=True)
        time.sleep(3) 

def move_dmm_arms(energy_change_PVs, params):

    log.info(' ')
    log.info('     *** moving dmm arms')

    if params.testing:
        log.warning('     *** testing mode:  set DMM dmm_us_arm %s mm' % params.dmm_us_arm) 
        log.warning('     *** testing mode:  set DMM dmm_ds_arm %s mm' % params.dmm_ds_arm) 
    else:    
        log.info('     *** moving dmm us arm %s mm' % params.dmm_us_arm) 
        energy_change_PVs['dmm_us_arm'].put(params.dmm_us_arm, wait=False, timeout=1000.0)
        log.info('     *** moving dmm ds arm %s mm' % params.dmm_ds_arm) 
        energy_change_PVs['dmm_ds_arm'].put(params.dmm_ds_arm, wait=True, timeout=1000.0)
        time.sleep(3)

def move_dmm_m2y(energy_change_PVs, params):    

    log.info(' ')
    log.info('     *** moving dmm m2y')

    if params.testing:
        log.warning('     *** testing mode:  set dmm m2y %s mm' % params.dmm_m2y) 
    else:
        log.info('     *** moving  dmm m2y %s mm' % params.dmm_m2y) 
        energy_change_PVs['dmm_m2y'].put(params.dmm_m2y, wait=True, timeout=1000.0)

def move_dmm_x(energy_change_PVs, params):

    log.info(' ')
    log.info('     *** moving dmm x')

    if params.testing:
        log.warning('     *** testing mode:  set dmm usx %s mm' % params.dmm_usx)
        log.warning('     *** testing mode:  set dmm dsx %s mm' % params.dmm_dsx)
    else:
        log.info('     *** moving dmm usx %s mm' % params.dmm_usx)
        energy_change_PVs['dmm_usx'].put(params.dmm_usx, wait=False)
        log.info('     *** moving dmm dsx %s mm' % params.dmm_dsx)
        energy_change_PVs['dmm_dsx'].put(params.dmm_dsx, wait=True)
        time.sleep(3) 

def move_table(energy_change_PVs, params):

    log.info(' ')
    log.info('     *** moving Table Y')

    if params.testing:
        log.warning('     *** testing mode:  set Table Y in station B %s mm' % params.table_y) 
    else:
        if params.table_y==0 and params.flag==0:
            log.warning('Ignore moving Table Y and Flag since they have not been initialized')
            return

        log.info('     *** moving Table Y in station B  %s mm' % params.table_y) 
        energy_change_PVs['table_y'].put(params.table_y, wait=True)

def move_flag(energy_change_PVs, params):

    log.info(' ')
    log.info('     *** moving Flag')

    if params.testing:
        log.warning('     *** testing mode:  set Flag y %s mm' % params.flag) 
    else:
        if params.flag==0:
            log.warning('Ignore moving Flag since they have not been initialized')
            return

        log.info('     *** moving Flag %s mm'  % params.flag) 
        energy_change_PVs['flag'].put(params.flag, wait=True)

def close_shutters(energy_change_PVs, params):

    log.info(' ')
    log.info('     *** close_shutters')
    if params.testing:
        log.warning('     *** testing mode - A-shutter will be closed during energy change')
    else:
        log.warning('     *** closing A-shutter')
        energy_change_PVs['ShutterA_Close'].put(1, wait=True)
        # uncomment and test with beam:
        # util.wait_pv(energy_change_PVs['ShutterA_Move_Status'], ShutterA_Close_Value)
        log.info('     *** close_shutter A: Done!')