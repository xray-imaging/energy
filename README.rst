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
        reset        Restore preset energy calibration file
        save         Associate the current beamline positions to an energy value
        status       Show status

Configuration File
------------------

The dmm status is stored in **~logs/dmm.conf**. You can create a template with::

    $ dmm init

**~logs/dmm.conf** is constantly updated to keep track of the last stored parameters, as initalized by **init** or modified by setting a new option value. For example to set the beamline to the last energy configuration ::

    $ dmm mono

to list of all **dmm save** options::

    $ dmm save -h
    
If the beamline has been manually optimized after setting a preset energy configuration, you can save the current beamline status with::  

    $ dmm save --energy 27


Testing mode
------------

In testing mode, the motor positions are printed but not actual motor motion occurs. To enable testing mode set:: 

    $ dmm set --testing

