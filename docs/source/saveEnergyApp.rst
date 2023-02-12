===============================
saveEnergyApp EPICS application
===============================

.. 
   toctree::
   :hidden:

   saveEnergy.template
   saveEnergy_settings.req
   saveEnergy.substitutions


saveEnergy includes a complete example EPICS application, including:

- A database file and corresponding autosave request file that contain the PVs required by the saveEnergy.py base class.
- OPI screens for medm
- An example IOC application that can be used to run the above databases.
  The databases are loaded in the IOC with the example substitutions file, 
  :doc:`saveEnergy.substitutions`.


Base class files
================
The following tables list all of the records in the saveEnergy.template file.
These records are used by the saveEnergy base class and so are required.

saveEnergy.template
-------------------

This is the database file that contains only the PVs required by the saveEnergy.py base class
:doc:`saveEnergy.template`.


    
medm files
----------

saveEnergy.adl
^^^^^^^^^^^^^^

The following is the MEDM screen :download:`saveEnergy.adl <../../saveEnergyApp/op/adl/saveEnergy.adl>` during a scan. 
The status information is updating.

.. image:: img/energy_01.png
    :width: 75%
    :align: center

saveEnergyEPICS_PVs.adl
^^^^^^^^^^^^^^^^^^^^^^^

The following is the MEDM screen :download:`saveEnergyEPICS_PVs.adl <../../saveEnergyApp/op/adl/saveEnergyEPICS_PVs.adl>`. 

If these PVs are changed tomoscan must be restarted.

.. image:: img/saveEnergyEPICS_PVs.png
    :width: 75%
    :align: center

