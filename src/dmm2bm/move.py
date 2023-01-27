import time

from epics import PV

from dmm2bm import log
from dmm2bm import util
from dmm2bm import pvs

ShutterA_Open_Value  = 1
ShutterA_Close_Value = 0

def aps2bm(pos_dmm_energy_select, params):

    log.info('Moving DMM to: %s %s' % (params.mode, pos_dmm_energy_select))

    if params.force:
        pass
    else:
        if (params.testing):
            log.warning('Testing mode is active. Nothing will move!')
        else:
            log.error('DMM motors will move if you press Y!')

        if not util.yes_or_no('Confirm energy change?'):              
            log.info(' ')
            log.warning('   *** Energy not changed')
            return False

    epics_pvs = pvs.init(params)

    log.info('close shutter')
    if params.testing:
        log.warning('     *** testing mode: A-shutter will be closed during energy change')
    else:
        log.warning('closing A-shutter')
        epics_pvs['ShutterA_Close'].put(1, wait=True)
        # uncomment and test with beam:
        # util.wait_pv(epics_pvs['ShutterA_Move_Status'], ShutterA_Close_Value)
        log.info('     *** close_shutter A: Done!')

    log.info('move motors')

    energy = list(pos_dmm_energy_select.keys())[0]
    for key in epics_pvs:
        try:
            if 'energy_move' in key or 'energy_pos' in key:
                pos     = pos_dmm_energy_select[energy][key]
                pv_name = epics_pvs[key].pvname
                if (params.testing):
                    log.warning('     *** testing mode:  set %s to %s' % (key.replace('energy_', ''), pos))
                else:
                    log.error('>>> moving command: epics_pvs[%s].put(%s)' % (key, pos))
                    # commented for testing
                    # epics_pvs[key].put(pos)
        except KeyError: 
            log.error('When using an intepolated position the PV associated to motor: %s is not moved' % epics_pvs[key].pvname)
    log.info('     *** move motors: Done!')

