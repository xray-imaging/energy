=====
About
=====


**energy** is an EPICS IOC hosting PVNames of two types "Move" and "Pos". Motors in the "Move" list will be moved for an energy change to a pre-calibrated and an interpolated position. A motor in the "Pos" list is only moved when selecting a pre-calibrated position. The difference is to be able to include in the pre-calibrated energy list motion control position like filters (Pos [1, 2, ...] or mirrors (Pos [In, Out]).

**energy** provides a GUI to move to pre-calibrated or arbitrary positions. When the energy selected is not in the list of pre-calibrated positions a subset of motors (Move) will move to interpolated positions.
**energy** provides a command line interface to move to pre-calibrated or arbitrary interpolated positions and to add/delete pre-calibrated positions.

