==================
Install directions
==================

EPICS Server
============

Build EPICS base
----------------

.. warning:: Make sure the disk partition hosting ~/epics is not larger than 2 TB. See `tech talk <https://epics.anl.gov/tech-talk/2017/msg00046.php>`_ and  `Diamond Data Storage <https://epics.anl.gov/meetings/2012-10/program/1023-A3_Diamond_Data_Storage.pdf>`_ document.

::

    $ mkdir ~/epics
    $ cd epics
    

- Download EPICS base latest release, i.e. 7.0.3.1., from https://github.com/epics-base/epics-base::

    $ git clone https://github.com/epics-base/epics-base.git
    $ cd epics-base
    $ git submodule init
    $ git submodule update
    $ make distclean (do this in case there was an OS update)
    $ make -sj
    

Build a minimal synApps
-----------------------

To build a minimal synApp::

    $ cd ~/epics

- Download in ~/epics `assemble_synApps <https://github.com/EPICS-synApps/assemble_synApps/blob/18fff37055bb78bc40a87d3818777adda83c69f9/assemble_synApps>`_.sh
- Edit the assemble_synApps.sh script to include only::
    
    $modules{'ASYN'} = 'R4-44-2';
    $modules{'AUTOSAVE'} = 'R5-11';
    $modules{'BUSY'} = 'R1-7-4';
    $modules{'XXX'} = 'R6-3';

You can comment out all of the other modules (ALLENBRADLEY, ALIVE, etc.)

- Run::

    $ cd ~/epics
    $ ./assemble_synApps.sh --dir=synApps --base=/home/beams/FAST/epics/epics-base

.. warning:: Replace /home/beams/FAST/ to the full path to your home directory

- This will create a synApps/support directory::

    $ cd synApps/support/

- Clone the energy module into synApps/support::
    
    $ git clone https://github.com/tomography/energy.git

.. warning:: If you are a energy developer you should clone your fork.

- Edit configure/RELEASE add this line to the end::
    
    ENERGY=$(SUPPORT)/energy

- Verify that synApps/support/energy/configure/RELEASE::

    EPICS_BASE=/home/beams/FAST/epics/epics-base
    SUPPORT=/home/beams/FAST/epics/synApps/support

are set to the correct EPICS_BASE and SUPPORT directories and that::

    BUSY
    AUTOSAVE
    ASYN
    XXX

point to the version installed.


- Run the following commands::

    $ make release
    $ make -sj

Testing the installation
------------------------

- Start the epics ioc and associated medm screen with::

    $ cd ~/epics/synApps/support/energy/iocBoot/iocEnergy
    $ start_IOC
    $ start_medm


Python Server
=============

**energy-cli** a commad-line-interface that allows to move a set of motors using a list of preselected/calibrated positions stored in a lookup table. The list of motor positions is labeled with an energy value. When the enegy selected is not in the list of calibrated positions a subset of motors can be moved to interplatate positions.

Installation
------------

::

    $ git clone https://github.com/xray-imaging/energy.git
    $ cd energy
    $ pip install .

in a prepared virtualenv or as root for system-wide installation.


Testing the installation
------------------------

- Start python server with::

    $ cd ~/epics/synApps/support/energy/iocBoot/iocEnergy
    $ python -i start_energy.py


