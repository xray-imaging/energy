TOP=../..

include $(TOP)/configure/CONFIG
#----------------------------------------
#  ADD MACRO DEFINITIONS BELOW HERE

# Build the IOC application
PROD_IOC = energyApp

# energyApp.dbd will be created and installed
DBD += energyApp.dbd

# test.dbd will include these files:
energyApp_DBD += base.dbd
energyApp_DBD += busySupport.dbd
energyApp_DBD += asSupport.dbd

# energyApp_registerRecordDeviceDriver.cpp derives from test.dbd
energyApp_SRCS += energyApp_registerRecordDeviceDriver.cpp

# Build the main IOC entry point where needed
energyApp_SRCS_DEFAULT += energyMain.cpp
energyApp_SRCS_vxWorks += -nil-

energyApp_LIBS += autosave
energyApp_LIBS += busy
#energyApp_LIBS += asyn

# Finally link IOC to the EPICS Base libraries
energyApp_LIBS += $(EPICS_BASE_IOC_LIBS)

include $(TOP)/configure/RULES
#----------------------------------------
#  ADD EXTRA GNUMAKE RULES BELOW HERE
