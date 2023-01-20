=======
dmm-cli
=======

**dmm-cli** is commad-line-interface to select the energy of the double crystal monochromator (DMM) installed at 
beamline `2bm <https://docs2bm.readthedocs.io>`_.

Installation
============

::

    $ git clone https://github.com/xray-imaging/dmm.git
    $ cd dmm
    $ pip install .

in a prepared virtualenv or as root for system-wide installation.


Usage
=====

Set energy
----------

To set the beamline energy to 20 keV::

    $ dmm mono --energy 20 

If the selected energy is not included in the pre-calibrated energy list, **dmm** will interpolate all motor positions using the values
of the closest calibrated energies.

To set pink beam:

::

    $ dmm pink

Save energy
-----------

To save the beamline motor positions and associate them to an energy to be used at a later time::

    $ dmm save --energy 28.32

The above will add 28.32 to the pre-calibrated energy list or, if already exists, update the beamline motor positions. 
To restore it::

    $ dmm mono --energy 28.32 


Add/Remove precalibrated energies
---------------------------------

To associate the current beamline positions to new energy value or update and existing one:

::

    $ dmm add --energy 28.32

the newly added energy will be used as start/end of the intepolation interval

To remove an energy value from the list of calibrated energies:

::

    $ dmm delete --energy 28.32

To list of all available options::

    $ energy -h
    usage: dmm [-h] [--config FILE] [--version]  ...

    optional arguments:
      -h, --help     show this help message and exit
      --config FILE  File name of configuration file
      --version      show program's version number and exit

    Commands:
      
        init         Usage: dmm init - Create configuration file and restore the original preset energy 
                            calibration file
        mono         Usage: dmm mono --energy 20 - Set the beamline to the --energy value using a 
                            precalibrated list or, if missing, a linear interpolation between the two 
                            closest calibrared values
        pink         Usage: dmm pink - Set the beamline to pink mode
        add          Usage: dmm add --energy 20 - Associate the current beamline positions to --energy value
        delete       Usage: dmm delete --energy 20 - Remove --energy value from the preset energy calibration file
        reset        Usage: dmm reset - Restore original preset energy calibration file.
        status       Usage: dmm status - Show status

to list of all **dmm save** options::

    $ dmm save -h


Testing mode
------------

In testing mode, the motor positions are printed but not actual motor motion occurs. To enable testing mode set:: 

    $ dmm set --testing


Configuration File
------------------

The dmm status is stored in **~/logs/dmm.conf**. You can create a template with::

    $ dmm init

**~/logs/dmm.conf** is constantly updated to keep track of the last stored parameters, as initalized by **init** or modified by setting a new option value. 
For example to set the beamline to the last energy configuration ::

    $ dmm mono
