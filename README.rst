==========
energy-cli
==========

**energy-cli** a general purpose commad-line-interface that allows to move a set of motors using a list of preselected/calibrated positions stored in a lookup table. The list of motor positions is labeled with an energy value. When the enegy selected is not in the list of calibrated positions a subset of motors can be moved to interplatate positions.

Installation
============

::

    $ git clone https://github.com/xray-imaging/energy.git
    $ cd energy
    $ pip install .

in a prepared virtualenv or as root for system-wide installation.

Requirements
------------

This python tool box relies on the following EPICS PVs served by a different IOC:


::

    $(P)$(R)EnergyMoveXPVName (X=0, 1 ...) 

hosting the PV name of motors that will be used to move to interpolated positions. The motor position for **"$(P)$(R)EnergyMoveXPVName"** 
must be present in both lookup table entries for the energy below/above the selected value, if one of the values is missing the motor will not be moved.  

::

    $(P)$(R)EnergyPosXPVName (X=0, 1 ...) 

PV hosting the shutter PV Open/Close/Status PV names formatted as:

::

    $(P)$(R)OpenShutterPVName
    $(P)$(R)CloseShutterPVName
    $(P)$(R)ShutterStatusPVName

PV hosting the value to Open/Close the shutter;

::

    $(P)$(R)CloseShutterValue
    $(P)$(R)OpenShutterValue


PVs to store the energy value and the energy mode:

::

    $(P)$(R)Energy.VAL
    $(P)$(R)EnergyMode.VAL


Optional PVs to store the motion all done:

::

    $(P)$(R)AllDoneA
    $(P)$(R)AllDoneB

These are only used before the opening the front end shutter to confirm all motors are done moving.

If these PVs are not avaialable from an EPICS IOC, you can simply hardcode the motor PV names in the **src/energy/pvs.py** file

Usage
=====

Set energy
----------

To set the beamline energy to 20 keV::

    $ energy set --energy 20 

If the selected energy is not included in the pre-calibrated energy list, **energy** will interpolate all motor positions using the values
of the closest calibrated energies.

To set the beamline for pink beam with 30keV cut off:

::

    $ energy --mode Pink --energy 30

Add energy
----------

To save the beamline motor positions and associate them to an energy to be used at a later time::

    $ energy add --energy 28.32

The above will add 28.32 to the pre-calibrated energy list or, if already exists, update the beamline motor positions. 
To restore it::

    $ energy set --energy 28.32 


Add/Remove precalibrated energies
---------------------------------

To associate the current beamline positions to new energy value or update and existing one:

::

    $ energy add --energy 28.32

the newly added energy will be used as start/end of the intepolation interval

To remove an energy value from the list of calibrated energies:

::

    $ energy delete --energy 28.32

To list of all available options::

    $ energy -h
    usage: energy [-h] [--config FILE] [--version]  ...

    optional arguments:
      -h, --help     show this help message and exit
      --config FILE  File name of configuration file
      --version      show program's version number and exit

    Commands:
      
        init         Usage: energy init - Create configuration file and restore the original preset energy calibration file
        set          Usage: energy set --energy 20 - Set the beamline to the --energy value using a precalibrated list or, if missing,
                     a linear interpolation point between the two closest calibrared values
        add          Usage: energy add --energy 20 - Associate the current beamline positions to --energy value
        delete       Usage: energy delete --energy 20 - Remove --energy value from the preset energy calibration file
        restore      Usage: energy restore - Restore original preset energy calibration file.
        status       Usage: energy status - Show status

to list of all **energy set** options::

    $ energy set -h


Testing mode
------------

In testing mode, the motor positions are printed but not actual motor motion occurs. To enable testing mode set:: 

    $ energy set --testing


Configuration File
------------------

The energy status is stored in **~/logs/energy.conf**. You can create a template with::

    $ energy init

**~/logs/energy.conf** is constantly updated to keep track of the last stored parameters, as initalized by **init** or modified by setting a new option value. 
For example to set the beamline to the last energy configuration ::

    $ energy set
