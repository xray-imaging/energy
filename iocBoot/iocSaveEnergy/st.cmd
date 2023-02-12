< envPaths

epicsEnvSet("P", "2bm:")
epicsEnvSet("R", "Energy:")

## Register all support components

# Use these lines to run the locally built saveEnergyApp
dbLoadDatabase "../../dbd/saveEnergyApp.dbd"
saveEnergyApp_registerRecordDeviceDriver pdbbase



dbLoadTemplate("saveEnergy.substitutions")

< save_restore.cmd
save_restoreSet_status_prefix($(P))
dbLoadRecords("$(AUTOSAVE)/asApp/Db/save_restoreStatus.db", "P=$(P)")

iocInit

create_monitor_set("auto_settings.req", 30, "P=$(P),R=$(R)")
