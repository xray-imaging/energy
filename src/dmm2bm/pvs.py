import time

from epics import PV

from dmm2bm import log

def init(params):

    epics_pvs = {}
    log.info("Inizializing epics PVs")

    # 2-BM control PVs (with 0-1 positions, will not be used by interpolation, will not be saved in status)
    epics_pvs['ShutterA_Open']            = PV('2bma:A_shutter:open.VAL')
    epics_pvs['ShutterA_Close']           = PV('2bma:A_shutter:close.VAL')
    epics_pvs['ShutterA_Move_Status']     = PV('PA:02BM:STA_A_FES_OPEN_PL')

    # 2-BM control PVs (with discrete positions, will not be used by interpolation, will be saved in status)
    epics_pvs['filter']                   = PV('2bma:fltr1:select.VAL')

    # 2-BM motion PVs (will be used to interpolate positions)
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

    # 2-BM output PVs
    epics_pvs['energy']                   = PV(params.energyioc_prefix + 'Energy.VAL')
    epics_pvs['energy_mode']              = PV(params.energyioc_prefix + 'EnergyMode.VAL')
 
    return epics_pvs


