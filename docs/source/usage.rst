=====
Usage
=====

CLI
===

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



GUI
===

The beamline x-ray energy change is managed by the `energy cli <https://github.com/xray-imaging/energy>`_ python library. 

.. image:: img/energy_01.png 
   :width: 256px
   :align: center
   :alt: tomo_user

The energy change operates in two modes. The first uses pre-stored energy calibration files. To select this mode select use "Pre-set". Then you can select any available energy from the drop down list.

Once the desired energy is selected press the "Set" button to move the beamline to the pre-calibrated locations.

The second mode **interpolate** allows the enter an arbitrary energy value. In this case the new position for all the PVs listed in the **Energy Move** list will be calculated by interpolation between the two closest pre-calibrated positions. The PVs listed in the **Energy Position** list will not be used by the interpolation and these motors will not move.


