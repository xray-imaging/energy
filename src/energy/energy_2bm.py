"""Software to save beamline positions for a specific energy with EPICS

   Classes
   -------
   Energy
     Base class for energy save with EPICS.
"""
import time
import threading
import subprocess

from epics import PV

from energy import log
from energy.energy import Energy


class Energy2BM(Energy):
    """Derived class used for tomography scanning with EPICS at APS beamline 2-BM

    Parameters
    ----------
    pv_files : list of str
        List of files containing EPICS pvNames to be used.
    macros : dict
        Dictionary of macro definitions to be substituted when
        reading the pv_files
    """

    def __init__(self, pv_files, macros):
        super().__init__(pv_files, macros)

    def energy_change(self):

        if self.epics_pvs['EnergyStatus'].get(as_string=True) != 'Done' or self.epics_pvs['EnergyBusy'].get() == 1:
            return
            
        if (self.epics_pvs["EnergyTesting"].get()):
            self.epics_pvs['EnergyStatus'].put('Changing energy testing')
        else:
            self.epics_pvs['EnergyStatus'].put('Changing energy')

        self.epics_pvs['EnergyBusy'].put(1)

        energy_choice_min = float(PV(self.epics_pvs["EnergyChoice"].pvname + '.ONST').get().split(' ')[1])
        energy_choice_max = float(PV(self.epics_pvs["EnergyChoice"].pvname + '.NIST').get().split(' ')[1])

        if self.epics_pvs["EnergyCalibrationUse"].get(as_string=True) == "Pre-set":
            self.epics_pvs['EnergyStatus'].put('Changing energy: using presets')

            energy_choice_index = str(self.epics_pvs["EnergyChoice"].get())
            energy_choice       = self.epics_pvs["EnergyChoice"].get(as_string=True)
            energy_choice_list  = energy_choice.split(' ')
            log.info("Energy: energy choice = %s" % energy_choice)
            if energy_choice_list[0] == 'Pink':
                command = 'energy pink --force'
            else: # Mono
                command = 'energy set --energy ' + energy_choice_list[1] + ' --force'
        else:
            energy_arbitrary = self.epics_pvs['EnergyArbitrary'].get()
            if  (energy_arbitrary >= energy_choice_min) & (energy_arbitrary < energy_choice_max):
                command = 'energy set --energy ' + str(self.epics_pvs['EnergyArbitrary'].get()) + ' --force'
                self.epics_pvs['EnergyInRange'].put(1)
            else:
                self.epics_pvs['EnergyStatus'].put('Error: energy out of range')
                self.epics_pvs['EnergyInRange'].put(0)
                time.sleep(2) # for testing
                self.epics_pvs['EnergyStatus'].put('Done')
                self.epics_pvs['EnergyBusy'].put(0)   
                self.epics_pvs['EnergyMove'].put(0)
                return
        if (self.epics_pvs["EnergyTesting"].get()):
            command =  command + ' --testing' 
        
        log.error(command)
        subprocess.Popen(command, shell=True)        

        time.sleep(10)
        log.info('Energy: waiting on motion to complete')
        while True:
            time.sleep(.3)
            if PV('2bma:alldone').get() and PV('2bmb:alldone').get():
                break
        log.info('motion completed')

        time.sleep(2) # for testing
        self.epics_pvs['EnergyStatus'].put('Done')
        self.epics_pvs['EnergyBusy'].put(0)   
        self.epics_pvs['EnergyMove'].put(0)   

    def energy_in_range(self):

        if self.epics_pvs['EnergyStatus'].get(as_string=True) != 'Done' or self.epics_pvs['EnergyBusy'].get() == 1:
            return

        energy_choice_min = float(PV(self.epics_pvs["EnergyChoice"].pvname + '.ONST').get().split(' ')[1])
        energy_choice_max = float(PV(self.epics_pvs["EnergyChoice"].pvname + '.NIST').get().split(' ')[1])

        energy_arbitrary = self.epics_pvs['EnergyArbitrary'].get()
        if  (energy_arbitrary >= energy_choice_min) & (energy_arbitrary < energy_choice_max):
            command = 'energy set --energy ' + str(self.epics_pvs['EnergyArbitrary'].get()) + ' --force'
            self.epics_pvs['EnergyInRange'].put(1)
        else:
            self.epics_pvs['EnergyStatus'].put('Error: energy out of range')
            self.epics_pvs['EnergyInRange'].put(0)
 
        time.sleep(2) # for testing
        self.epics_pvs['EnergyStatus'].put('Done')
        self.epics_pvs['EnergyBusy'].put(0)   
        self.epics_pvs['EnergyMove'].put(0)   

