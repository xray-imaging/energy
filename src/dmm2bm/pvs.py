import time

from epics import PV

from dmm2bm import log
from dmm2bm import util

def init(params):

    log.info("Inizializing epics PVs")
    
    epics_pvs = {}
    # 2-BM motion PVs (will be used to interpolate positions)
    epics_move_pvs = init_pvs(params, 'EnergyMove', 'energy move ', n=16)
    # 2-BM control PVs (with 0-1 positions, will not be used by interpolation, will not be saved in status)
    epics_pos_pvs  = init_pvs(params, 'EnergyPos',  'energy pos ',  n=3)

    epics_pvs = {**epics_move_pvs, **epics_pos_pvs}

    # 2-BM shutter control PVs
    epics_pvs['ShutterA_Open']            = PV('2bma:A_shutter:open.VAL')
    epics_pvs['ShutterA_Close']           = PV('2bma:A_shutter:close.VAL')
    epics_pvs['ShutterA_Move_Status']     = PV('PA:02BM:STA_A_FES_OPEN_PL')

    # 2-BM output PVs
    epics_pvs['energy']                   = PV(params.energyioc_prefix + 'Energy.VAL')
    epics_pvs['energy_mode']              = PV(params.energyioc_prefix + 'EnergyMode.VAL')

    return epics_pvs

def init_pvs(params, pv_prefix='EnergyMove', label='energy move ', n=16):

    pv_name = {}
    epics_pvs = {}
    s = ''
    for i in range(n):
        pv_pv_desc = params.energyioc_prefix + pv_prefix + str(i) + 'PVDesc'
        pv_pv_name = params.energyioc_prefix + pv_prefix + str(i) + 'PVName'
        pv_name    = PV(pv_pv_name).get()
        if (pv_name != '') and pv_name != None:
            pv_desc = PV(pv_name + '.DESC').get()
            if pv_desc != None:
                if pv_desc == '' or 'table' in pv_name:
                    a_list = pv_name.split(':')
                    del a_list[0]
                    s = s.join(a_list)
                    pv_key = util.clean(label + s)
                else:
                    pv_key = util.clean(label + pv_desc)
                log.info('>>> %s connected to PV: %s' % (pv_key, pv_name))
                PV(pv_pv_desc).put(pv_key.replace('energy_move_', '').replace('energy_pos_', ''))
                pv_val = PV(pv_name + '.VAL')
                epics_pvs[pv_key] = pv_val
            else:
                log.error('>>> Cannot connect to: %s' % pv_name)
        else:
            if pv_name == '':
                log.warning('>>> PV %s: is not set' % (pv_pv_name))
                PV(pv_pv_desc).put('')
            else:
                log.error('>>> Cannot connect to: %s: %s' % (pv_pv_name, pv_name))
    return epics_pvs
