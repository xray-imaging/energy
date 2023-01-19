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

Save energy
-----------

To save the beamline motor positions and associate them to an energy to be used at a later time::

    $ dmm save --energy 28.32

The above will add 28.32 to the pre-calibrated energy list or, if already exists, update the beamline motor positions. 
To restore it::

    $ dmm mono --energy 28.32 

to list of all available options::

    $ energy -h
    usage: dmm [-h] [--config FILE] [--version]  ...

    optional arguments:
      -h, --help     show this help message and exit
      --config FILE  File name of configuration file
      --version      show program's version number and exit

    Commands:
      
        init         Create configuration file
        mono         Set DMM energy
        pink         Set the beamline to pink mode
        add          Associate the current beamline positions to --energy value
        delete       Remove --energy value from the preset energy calibration file
        reset        Restore preset energy calibration file
        status       Show status

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
