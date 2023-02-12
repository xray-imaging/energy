=====
About
=====


**energy** is an EPICS IOC hosting motion control PVNames of two types "Move" and "Pos". Motors in the "Move" list will be moved for an energy change to a pre-calibrated and an interpolated positions. Motors in the "Pos" list are only moved when selecting a pre-calirated position. The difference is to be able to include motion control position like filters (Pos [1, 2, ...] or mirrors (Pos [In, Out]).

**energy** provides a GUI to move to pre-calibrated or arbitrary positions. When the energy selected is not in the list of pre-calibrated positions a subset of motors (Move) will move to interplatate positions.
**energy** provides a commnad line interface to move to pre-calibrated or arbitrary interpolated positions and to add/delete pre-calibrated positions.
