import time

from epics import PV

from energy import log
from energy import util
from energy import pvs

# OpenShutterValue  = 1
# CloseShutterValue = 0

def motors(pos_energy_select, params):

    move_status = False
    log.info('Moving motors to: %s %s' % (params.mode, pos_energy_select))

    if params.force:
        pass
    else:
        if (params.testing):
            log.warning('Testing mode is active. Nothing will move!')
        else:
            log.error('Beamline motors will move if you press Y!')

        if not util.yes_or_no('Confirm energy change?'):              
            log.info(' ')
            log.warning('   *** Energy not changed')
            return move_status

    epics_pvs = pvs.init(params)

    log.info('close shutter')
    if params.testing:
        log.warning('     *** testing mode: A-shutter will be closed during energy change')
    else:
        log.warning('closing A-shutter')
        # epics_pvs['CloseShutter'].put(1, wait=True)
        close_frontend_shutter(epics_pvs)
    
    log.info('move motors')
    energy = list(pos_energy_select.keys())[0]
    for key in epics_pvs:
        try:
            if 'energy_move' in key or 'energy_pos' in key:
                pos     = pos_energy_select[energy][key]
                pv_name = epics_pvs[key].pvname
                if (params.testing):
                    log.warning('     ***  testing mode:  set %s to %f' % (key.replace('energy_', ''), pos))
                    time.sleep(.1) 
                else:
                    move_status = True
                    log.info('move command: epics_pvs[%s].put(%s) sent to motor' % (key, pos))
                    epics_pvs[key].put(pos) # comment when testing
                    time.sleep(.1) 
        except KeyError: 
            log.error('PV associated to motor: %s is missing from the pre-set positon. This motor will not moved' % epics_pvs[key].pvname)
    
    log.info('     *** all move commands sent to motors')

    if move_status:
        epics_pvs['energy_mode'].put(params.mode, wait=True)
        epics_pvs['energy'].put(energy, wait=True)

    log.info('energy: waiting on motion to complete')
    if params.beamline == '2bm':
        while True:
            time.sleep(.3)
            if epics_pvs['AllDoneA'].get() and epics_pvs['AllDoneB'].get():
                break
    log.info('motion completed')
    log.info('open shutter')
    if params.testing:
        log.warning('     *** testing mode: shutter will be open at the end of the energy change')
    else:
        log.warning('opening shutter')
        open_frontend_shutter(epics_pvs)

    return move_status


def open_frontend_shutter(epics_pvs):
    """Opens the shutters.

    This does the following:

    - Checks if we are in testing mode. If we are, do nothing else opens the shutter.
    """
    if not epics_pvs['OpenShutter'] is None:
        pv = epics_pvs['OpenShutter']
        value = epics_pvs['OpenShutterValue'].get(as_string=True)

        status = epics_pvs['ShutterStatus'].get(as_string=True)
        log.info('shutter status: %s' % status)
        log.info('open shutter: %s, value: %s' % (pv, value))
        epics_pvs['OpenShutter'].put(value, wait=True)
        wait_frontend_shutter_open(epics_pvs)
        # wait_pv(epics_pvs['ShutterStatus'], 1)
        status = epics_pvs['ShutterStatus'].get(as_string=True)
        log.info('shutter status: %s' % status)



def wait_frontend_shutter_open(epics_pvs, timeout=-1):
    """Waits for the front end shutter to open, or for ``abort_scan()`` to be called.

    While waiting this method periodically tries to open the shutter..

    Parameters
    ----------
    timeout : float
        The maximum number of seconds to wait before raising a ShutterTimeoutError exception.
    """
    start_time = time.time()
    pv = epics_pvs['OpenShutter']
    value = epics_pvs['OpenShutterValue'].get(as_string=True)
    value = epics_pvs['OpenShutterValue'].get(as_string=True)

    log.info('open shutter: %s, value: %s' % (pv, value))
    elapsed_time = 0
    while True:
        if epics_pvs['ShutterStatus'].get() == int(value):
            log.warning("Shutter is open in %f s" % elapsed_time)
            return
        value = epics_pvs['OpenShutterValue'].get()
        time.sleep(1.0)
        current_time = time.time()
        elapsed_time = current_time - start_time
        log.warning("Waiting on shutter to open: %f s" % elapsed_time)
        epics_pvs['OpenShutter'].put(value, wait=True)
        if timeout > 0:
            if elapsed_time >= timeout:
               exit()

def close_frontend_shutter(epics_pvs):
    """Closes the shutters.
    This does the following:

    - Checks if we are in testing mode. If we are, do nothing else closes the shutter.
    """
    if not epics_pvs['CloseShutter'] is None:
        pv = epics_pvs['CloseShutter']
        value = epics_pvs['CloseShutterValue'].get(as_string=True)
        status = epics_pvs['ShutterStatus'].get(as_string=True)
        log.info('shutter status: %s'% status)
        log.info('close shutter: %s, value: %s'% (pv, value))
        epics_pvs['CloseShutter'].put(value, wait=True)
        util.wait_pv(epics_pvs['ShutterStatus'], 0)
        status = epics_pvs['ShutterStatus'].get(as_string=True)
        log.info('shutter status: %s' % status)
