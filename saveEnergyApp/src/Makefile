TOP=../..

include $(TOP)/configure/CONFIG
#----------------------------------------
#  ADD MACRO DEFINITIONS BELOW HERE

# Build the IOC application
PROD_IOC = saveEnergyApp

# saveEnergyApp.dbd will be created and installed
DBD += saveEnergyApp.dbd

# test.dbd will include these files:
saveEnergyApp_DBD += base.dbd
saveEnergyApp_DBD += busySupport.dbd
saveEnergyApp_DBD += asSupport.dbd

# saveEnergyApp_registerRecordDeviceDriver.cpp derives from test.dbd
saveEnergyApp_SRCS += saveEnergyApp_registerRecordDeviceDriver.cpp

# Build the main IOC entry point where needed
saveEnergyApp_SRCS_DEFAULT += saveEnergyMain.cpp
saveEnergyApp_SRCS_vxWorks += -nil-

saveEnergyApp_LIBS += autosave
saveEnergyApp_LIBS += busy
#saveEnergyApp_LIBS += asyn

# Finally link IOC to the EPICS Base libraries
saveEnergyApp_LIBS += $(EPICS_BASE_IOC_LIBS)

include $(TOP)/configure/RULES
#----------------------------------------
#  ADD EXTRA GNUMAKE RULES BELOW HERE
