< envPaths

epicsEnvSet("P", "2bm:")
epicsEnvSet("R", "Energy:")

## Register all support components

# Use these lines to run the locally built energyApp
dbLoadDatabase "../../dbd/energyApp.dbd"
energyApp_registerRecordDeviceDriver pdbbase



dbLoadTemplate("energy.substitutions")

< save_restore.cmd
save_restoreSet_status_prefix($(P))
dbLoadRecords("$(AUTOSAVE)/asApp/Db/save_restoreStatus.db", "P=$(P)")

iocInit

create_monitor_set("auto_settings.req", 30, "P=$(P),R=$(R)")

# Force default values after autosave restore
dbpf("2bm:Energy:EnergyCalibrationUse", 0)
# Force default values after autosave restore
dbpf("2bm:Energy:EnergyTesting", 1)
