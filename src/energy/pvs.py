import time

from epics import PV

from energy import log
from energy import util

def init(params):

    log.info("Inizializing epics PVs")
    

    epics_pvs = {}
    # This python tool box relies on the following EPICS PVs served by a different IOC:
    # $(P)$(R)EnergyMoveXPVName (X=0, 1 ...) hosting the PV name of motors that will be used to move to interpolated positions.
    # The motor position for $(P)$(R)EnergyMoveXPVName must be present in both lookup table entries for the energy below/above the selected value,
    # if one of the values is missing the motor will not be moved.  
    epics_move_pvs = init_pvs(params, 'EnergyMove', 'energy move ', n=16)
    # $(P)$(R)EnergyPosXPVName (X=0, 1 ...) hosting the PV name of motors that will NOT be used to move to interpolated positions
    # These motors will move only when a pre-calibrated energy is selected
    epics_pos_pvs  = init_pvs(params, 'EnergyPos',  'energy pos ',  n=40)

    epics_pvs = {**epics_move_pvs, **epics_pos_pvs}

    # PV hosting the shutter PV Open/Close/Status PV names
    epics_pvs['OpenShutter']       = PV(PV(params.energyioc_prefix + 'OpenShutter'    + 'PVName').get())
    epics_pvs['CloseShutter']      = PV(PV(params.energyioc_prefix + 'CloseShutter'   + 'PVName').get())
    epics_pvs['ShutterStatus']     = PV(PV(params.energyioc_prefix + 'ShutterStatus'  + 'PVName').get())
    
    # PV hosting the value to Open/Close the shutter
    epics_pvs['CloseShutterValue'] = PV(params.energyioc_prefix    + 'CloseShutter'   + 'Value' )
    epics_pvs['OpenShutterValue']  = PV(params.energyioc_prefix    + 'OpenShutter'    + 'Value' )

    # PVs to store the energy value and the energy mode
    epics_pvs['energy']                   = PV(params.energyioc_prefix + 'Energy.VAL')
    epics_pvs['energy_mode']              = PV(params.energyioc_prefix + 'EnergyMode.VAL')


    # These are optional PV to store the motion all done. 
    # These are only used before the open_frontend_shutter() to confirm all motors are done moving
    # Temporary hardcoded. 
    epics_pvs['AllDoneA']                 = PV('2bma:alldone')
    epics_pvs['AllDoneB']                 = PV('2bmb:alldone')

    # Wait 1 second for all PVs to connect
    time.sleep(1)
    
    return epics_pvs

def init_pvs(params, pv_prefix='EnergyMove', label='energy move ', n=16):

    # this python toolbox relies on epics PVs provided by an external IOC.
    # These PV host 
    # pv_name = {}
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
                    s = ''
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
