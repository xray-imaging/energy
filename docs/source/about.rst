=====
About
=====

The **energy** is an EPICS IOC tool that allows users to select an X-ray energy and automatically adjust all relevant beamline components accordingly. It supports both pre-calibrated energy values and intermediate values located between two pre-calibrated points. For intermediate values, a subset of motors determines their positions through linear interpolation. Meanwhile, other components, such as filters or table positions, will move to pre-set positions without interpolation.


The **energy** tool manages beamline component positioning by organizing motion control PVNames into two categories: "Move" and "Pos". 

- **Move**: Motors in this list are adjusted with every energy change. They move to either pre-calibrated positions or interpolated positions when a non-calibrated energy value is selected.
- **Pos**: Motors in this list are only moved when selecting a pre-calibrated position. This allows for controlling components like filters (e.g., Pos [1, 2, ...]) or mirrors (e.g., Pos [In, Out]) that do not require interpolation.

The **energy** tool also supports listing "Sync" and "Store" PVs:

- **Sync**: PVs in this list are set to 1 (i.e., processed) at the end of any motor motion. This is useful for components like slits or tables, which may be moved either directly or via device-level virtual motors.
- **Store**: PVs in this list are not involved in motion control. Their values are simply recorded in the energy configuration JSON file—for example, timestamps or other contextual metadata.

