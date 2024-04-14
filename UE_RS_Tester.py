# -*- coding: utf-8 -*-
"""
Created on Fri Apr 24 15:44:56 2020

@author: Richard Canning
"""


import pyvisa

import numpy as np
import pandas as pd
from pandas import DataFrame
import socket
import time
from time import sleep
from time import *

from timeit import default_timer as timer
start = timer()



#initialize network connections to MiniCircuits RF switches
SW1HOST = '192.168.1.102'
SW1PORT = 23
sw1 =socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sw1.connect((SW1HOST, SW1PORT))
sw1.setblocking(0)
sw1.settimeout(5)

SW2HOST = '192.168.1.101'
SW2PORT = 23
sw2 =socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sw2.connect((SW2HOST, SW2PORT))
sw2.setblocking(0)
sw2.settimeout(5)

sw1.send(b"SP6TA:STATE:1\r\n")
sw1.send(b"SP6TB:STATE:1\r\n")
sw2.send(b"SP6TA:STATE:1\r\n")
sw2.send(b"SP6TB:STATE:1\r\n")

rm = pyvisa.ResourceManager()

#Connect to VSE SW with PyVISA
inst = rm.open_resource("TCPIP::DESKTOP-II6D250::inst0::INSTR")

inst.write(r"*RST")
sleep(3)

inst.write(r"MMEM:LOAD:STAT 1,'C:\Users\System_Tool_Kit\Desktop\LTE_BF_Setup_for_VSE'")

sleep(7)

FullRB =4

while FullRB >3:
    inst.write("DL:DEM:AUTO ON")
    sleep(0.5)
    inst.write(r"DL:FORM:PSCD PDCCH")
    sleep(0.5)
    inst.write("INIT:SEQ:SING")
    sleep(2)
    inst.write("INIT:CONT OFF")
    sleep(2)
    inst.write("INIT:BLOC:CONM")
    sleep(2)
    inst.write("DISP:WIND8:SUBW1:SEL")
    
    sleep (3)
    
    pwrvsrb1 = inst.query("TRACE8? TRACE1")
    sleep(2)
    pwrvsrb2 = inst.query("TRACE8? TRACE2")
    sleep(2)
    pwrvsrb3 = inst.query("TRACE8? TRACE3")
    sleep(2)
    pwrvsrb1 = pwrvsrb1.split(",",50)
    pwrvsrb2 = pwrvsrb2.split(",",50)
    pwrvsrb3 = pwrvsrb3.split(",",50)
    rbpwrcomp = DataFrame (pwrvsrb1,columns=['Average'])
    rbpwrcomp['Minimum'] = pwrvsrb2
    rbpwrcomp['Maximum'] = pwrvsrb3
    
    rbpwrcomp = rbpwrcomp.drop(rbpwrcomp.index[20:30])
    rbpwrcomp.drop(rbpwrcomp.index[-1])
    rbpwrcomp['Maximum'] = rbpwrcomp['Maximum'].astype(float)
    rbpwrcomp['Average'] = rbpwrcomp['Average'].astype(float)
    rbpwrcomp['DeltaAvMax'] = rbpwrcomp['Average'] - rbpwrcomp['Maximum']
    rbpwrcomp['DeltaAvMax'] = rbpwrcomp.DeltaAvMax.abs()
    FullRB = rbpwrcomp['DeltaAvMax'].max()
    print('looping...')
    
print('Full RBs!')  

#Set up Saved Beamforming config file

#
#Identifies the configuration according to the data in the PDCCH DCIs.
inst.write(r"DL:FORM:PSCD PDCCH")
##This command selects the precoding scheme of an allocation.
##inst.write(r"CONF:DL:SUBF0:ALL0:PREC:SCH BF")
##time.sleep(.5)
#inst.write(r"CONF:DL:SUBF0:ALL1:PREC:SCH BF")
#sleep(.5)
#inst.write(r"CONF:DL:SUBF0:ALL2:PREC:SCH BF")
sleep(.5)
inst.write(r"CONF:DL:SUBF1:ALL0:PREC:SCH BF")
sleep(.5)
inst.write(r"CONF:DL:SUBF2:ALL0:PREC:SCH BF")
sleep(.5)
inst.write(r"CONF:DL:SUBF3:ALL0:PREC:SCH BF")
sleep(.5)
inst.write(r"CONF:DL:SUBF4:ALL0:PREC:SCH BF")
sleep(.5)
#inst.write(r"CONF:DL:SUBF5:ALL1:PREC:SCH BF")
#sleep(.5)
inst.write(r"CONF:DL:SUBF6:ALL0:PREC:SCH BF")
sleep(.5)
inst.write(r"CONF:DL:SUBF7:ALL0:PREC:SCH BF")
sleep(.5)
inst.write(r"CONF:DL:SUBF8:ALL0:PREC:SCH BF")
sleep(.5)
inst.write(r"CONF:DL:SUBF9:ALL0:PREC:SCH BF")

inst.write("DL:DEM:AUTO OFF")
sleep(0.5)
inst.write(r"DL:FORM:PSCD OFF")

inst.write(r"CAL:PHAS:LOAD'C:\Users\System_Tool_Kit\Desktop\bf cal file_1234'")
print("1234")
sleep(1)
#While Loop to determine if the UE-RS can be measured, parses data for one run and calcs Std Dev, if SD is less than 5, then the loop breaks and the measu
#measurement happens, basically waiting for all of the SFs to be busied up
std_Phase = 6

while std_Phase >5:
#    Continuous off, capture 1 Frame
    inst.write("INIT:SEQ:SING")
    inst.write("INIT:CONT OFF")
    inst.write("INIT:BLOC:CONM")
    sleep(2)



    #Phase data from Antenna 1
    inst.write("DISP:WIND1:SUBW1:SEL")
    sleep(1)
    antennatest = inst.query("TRAC:DATA? TRACE1", delay = 1.0)
    sleep(4)
    print(inst.query("TRAC:DATA? TRACE1", delay = 1.0))
    sleep(2)
    
#    
    phase1 = antennatest.split(",",370)
#    testsplit1 = float(phase1[8])
#    testsplit2 = float(phase1[53])
#    testsplit3 = float(phase1[98])
#    testsplit4 = float(phase1[143])
#    testsplit5 = float(phase1[188])
#    testsplit6 = float(phase1[238])
#    testsplit7 = float(phase1[283])
#    testsplit8 = float(phase1[328])
# Parse data from Beamforming Summary
#    phase1 = antennatest.split(",",370)
    testsplit1 = float(phase1[13])
    testsplit2 = float(phase1[58])
    testsplit3 = float(phase1[103])
    testsplit4 = float(phase1[148])
    testsplit5 = float(phase1[198])
    testsplit6 = float(phase1[243])
    testsplit7 = float(phase1[288])
    testsplit8 = float(phase1[333])
# Alternate Parsing arrangement    
#    phase1 = antennatest.split(",",370)
#    testsplit1 = float(phase1[17])
#    testsplit2 = float(phase1[62])
#    testsplit3 = float(phase1[103])
#    testsplit4 = float(phase1[148])
#    testsplit5 = float(phase1[193])
#    testsplit6 = float(phase1[238])
#    testsplit7 = float(phase1[283])
#    testsplit8 = float(phase1[328])
    
# Build Data in DataFrame calc Std Dev to determine if the UE-RS can be measured   
    RF_Port_Data = {'Subframe':['SF2', 'SF3', 'SF4', 'SF6', 'SF7', 'SF8', 'SF9', 'SF10'], 'UE-RS Phase':[testsplit1, testsplit2, testsplit3, testsplit4, testsplit5, testsplit6, testsplit7, testsplit8]}
    RF_Port__Phases = pd.DataFrame(RF_Port_Data)
    std_Phase = RF_Port__Phases.loc[:,'UE-RS Phase'].std()
    print(std_Phase)


sleep(4)

#Phase data from Antenna 1
inst.write("DISP:WIND1:SUBW1:SEL")
sleep(1)
antenna1 = inst.query("TRAC:DATA? TRACE1", delay = 1.0)
sleep(4)
print(inst.query("TRAC:DATA? TRACE1", delay = 1.0))
sleep(2)
#Write to DF
#Phase data from Antenna 2
inst.write("DISP:WIND1:SUBW2:SEL")
sleep(1)
antenna2 = inst.query("TRAC:DATA? TRACE1", delay = 1.0)
sleep(4)
print(inst.query("TRAC:DATA? TRACE1", delay = 1.0))
sleep(2)
#Write to DF
#Phase data from Antenna 3
inst.write("DISP:WIND1:SUBW3:SEL")
sleep(1)
antenna3 = inst.query("TRAC:DATA? TRACE1", delay = 1.0)
sleep(4)
print(inst.query("TRAC:DATA? TRACE1", delay = 1.0))
sleep(2)
#Write to DF
#Phase data from Antenna 4
inst.write("DISP:WIND1:SUBW4:SEL")
sleep(1)
antenna4 =  inst.query("TRAC:DATA? TRACE1", delay = 1.0)
sleep(4)
print(inst.query("TRAC:DATA? TRACE1", delay = 1.0))
sleep(2)
#Write to DF

#Back to Local
inst.write("@LOC")


phase1 = antenna1.split(",",17)
split1 = phase1[13]
phase2 = antenna2.split(",",17)
split2 = phase2[13]
phase3 = antenna3.split(",",17)
split3 = phase3[13]
phase4 = antenna4.split(",",17)
split4 = phase4[13]
sleep(2)

#phaseangle2 = float(split2)-float(split1)
#phaseangle3 = float(split3)-float(split1)
#phaseangle4 = float(split4)-float(split1)

#Change switch positions for 5678
sw1.send(b"SP6TA:STATE:1\r\n")
sw1.send(b"SP6TB:STATE:2\r\n")
sw2.send(b"SP6TA:STATE:2\r\n")
sw2.send(b"SP6TB:STATE:2\r\n")
sleep(1)


inst.write(r"CAL:PHAS:LOAD'C:\Users\System_Tool_Kit\Desktop\bf cal file_1567'")
inst.write("@LOC")
print("Done 1to4!!")


inst.write(r"CAL:PHAS:LOAD'C:\Users\System_Tool_Kit\Desktop\bf cal file_1567'")
sleep(1)
print("1567")
sleep(2)
#
std_Phase = 6

while std_Phase >5:
#    Continuous off, capture 1 Frame
    inst.write("INIT:SEQ:SING")
    inst.write("INIT:CONT OFF")
    inst.write("INIT:BLOC:CONM")
    sleep(2)



    #Phase data from Antenna 1
    inst.write("DISP:WIND1:SUBW1:SEL")
    sleep(1)
    antenna1 = inst.query("TRAC:DATA? TRACE1", delay = 1.0)
    sleep(4)
    print(inst.query("TRAC:DATA? TRACE1", delay = 1.0))
    sleep(2)
    
    
    phase1 = antenna1.split(",",370)
    testsplit1 = float(phase1[13])
    testsplit2 = float(phase1[58])
    testsplit3 = float(phase1[103])
    testsplit4 = float(phase1[148])
    testsplit5 = float(phase1[198])
    testsplit6 = float(phase1[243])
    testsplit7 = float(phase1[288])
    testsplit8 = float(phase1[333])
    
    RF_Port_Data = {'Subframe':['SF2', 'SF3', 'SF4', 'SF6', 'SF7', 'SF8', 'SF9', 'SF10'], 'UE-RS Phase':[testsplit1, testsplit2, testsplit3, testsplit4, testsplit5, testsplit6, testsplit7, testsplit8]}
    RF_Port__Phases = pd.DataFrame(RF_Port_Data)
    std_Phase = RF_Port__Phases.loc[:,'UE-RS Phase'].std()
    print(std_Phase)





#Phase data from Antenna 1
inst.write("DISP:WIND1:SUBW1:SEL")
sleep(1)
antenna11 = inst.query("TRAC:DATA? TRACE1", delay = 1.0)
sleep(4)
print(inst.query("TRAC:DATA? TRACE1", delay = 1.0))
sleep(2)
#Write to DF
#Phase data from Antenna 2
inst.write("DISP:WIND1:SUBW2:SEL")
sleep(1)
antenna5 = inst.query("TRAC:DATA? TRACE1", delay = 1.0)
sleep(4)
print(inst.query("TRAC:DATA? TRACE1", delay = 1.0))
sleep(2)
#Write to DF
#Phase data from Antenna 3
inst.write("DISP:WIND1:SUBW3:SEL")
sleep(1)
antenna6 = inst.query("TRAC:DATA? TRACE1", delay = 1.0)
sleep(4)
print(inst.query("TRAC:DATA? TRACE1", delay = 1.0))
sleep(2)
#Write to DF
#Phase data from Antenna 4
inst.write("DISP:WIND1:SUBW4:SEL")
sleep(1)
antenna7 = inst.query("TRAC:DATA? TRACE1", delay = 1.0)
sleep(4)
print(inst.query("TRAC:DATA? TRACE1", delay = 1.0))
sleep(2)
#Write to DF

#Back to Local
inst.write("@LOC")

phase11 = antenna11.split(",",17)
split11 = phase11[13]
phase5 = antenna5.split(",",17)
split5 = phase5[13]
phase6 = antenna6.split(",",17)
split6 = phase6[13]
phase7 = antenna7.split(",",17)
split7 = phase7[13]


#Change switch positions for 5678
sw1.send(b"SP6TA:STATE:1\r\n")
sw1.send(b"SP6TB:STATE:3\r\n")
sleep(1)


#inst.write(r"CAL:PHAS:LOAD'C:\Users\System_Tool_Kit\Desktop\bf cal file_18'")
#inst.write("@LOC")
print("Done5to7!!")

inst.write(r"CAL:PHAS:LOAD'C:\Users\System_Tool_Kit\Desktop\bf cal file_18'")

print("18")
sleep(1)

std_Phase = 6

while std_Phase >5:
#    Continuous off, capture 1 Frame
    inst.write("INIT:SEQ:SING")
    inst.write("INIT:CONT OFF")
    inst.write("INIT:BLOC:CONM")
    sleep(2)



    #Phase data from Antenna 1
    inst.write("DISP:WIND1:SUBW1:SEL")
    sleep(1)
    antenna1 = inst.query("TRAC:DATA? TRACE1", delay = 1.0)
    sleep(4)
    print(inst.query("TRAC:DATA? TRACE1", delay = 1.0))
    sleep(2)
    
    
    phase1 = antenna1.split(",",370)
    testsplit1 = float(phase1[13])
    testsplit2 = float(phase1[58])
    testsplit3 = float(phase1[103])
    testsplit4 = float(phase1[148])
    testsplit5 = float(phase1[198])
    testsplit6 = float(phase1[243])
    testsplit7 = float(phase1[288])
    testsplit8 = float(phase1[333])
    
    RF_Port_Data = {'Subframe':['SF2', 'SF3', 'SF4', 'SF6', 'SF7', 'SF8', 'SF9', 'SF10'], 'UE-RS Phase':[testsplit1, testsplit2, testsplit3, testsplit4, testsplit5, testsplit6, testsplit7, testsplit8]}
    RF_Port__Phases = pd.DataFrame(RF_Port_Data)
    std_Phase = RF_Port__Phases.loc[:,'UE-RS Phase'].std()
    print(std_Phase)




#Phase data from Antenna 1
inst.write("DISP:WIND1:SUBW1:SEL")
sleep(1)
antenna111 = inst.query("TRAC:DATA? TRACE1", delay = 1.0)
sleep(4)
print(inst.query("TRAC:DATA? TRACE1", delay = 1.0))
sleep(2)
#Write to DF
#Phase data from Antenna 2
inst.write("DISP:WIND1:SUBW2:SEL")
sleep(1)
antenna8 = inst.query("TRAC:DATA? TRACE1", delay = 1.0)
sleep(4)
print(inst.query("TRAC:DATA? TRACE1", delay = 1.0))
sleep(2)
#Write to DF

#Back to Local
inst.write("@LOC")

phase111 = antenna111.split(",",17)
split111 = phase111[13]
phase8 = antenna8.split(",",17)
split8 = phase8[13]


phaseangle2 = float(split2)-float(split1)
phaseangle3 = float(split3)-float(split1)
phaseangle4 = float(split4)-float(split1)
phaseangle5 = float(split5)-float(split11)
phaseangle6 = float(split6)-float(split11)
phaseangle7 = float(split7)-float(split11)
phaseangle8 = float(split8)-float(split111)

sw1.send(b"SP6TA:STATE:1\r\n")
sw1.send(b"SP6TB:STATE:1\r\n")
sw2.send(b"SP6TA:STATE:1\r\n")
sw2.send(b"SP6TB:STATE:1\r\n")

inst.write(r"CAL:PHAS:LOAD'C:\Users\System_Tool_Kit\Desktop\bf cal file_1234'")

#
#Calibration values for cable and switch angle skew (degrees)
CompAngle2 = -22
CompAngle3 = -8.8
CompAngle4 = -101.5
CompAngle5 = -90.5
CompAngle6 = 7.9
CompAngle7 = -40.4
CompAngle8 = -61.8


#Phase adjustment values

phaseadjustment2 = float(split2)-float(split1)
phaseadjustment3 = float(split3)-float(split1)
phaseadjustment4 = float(split4)-float(split1)
phaseadjustment5 = float(split5)-float(split11)
phaseadjustment6 = float(split6)-float(split11)
phaseadjustment7 = float(split7)-float(split11)
phaseadjustment8 = float(split8)-float(split111)
inst.write("@LOC")

#Build DF for measured Angle Values
RF_Phase_Data = {'Subframe':['Port2', 'Port3', 'Port4', 'Port5', 'Port6', 'Port7', 'Port8'], 'UE_RS_Phase':[phaseadjustment2, phaseadjustment3, phaseadjustment4, phaseadjustment5, phaseadjustment6, phaseadjustment7, phaseadjustment8]}
UE_RS__Phases = pd.DataFrame(RF_Phase_Data)

#Unit circle errors can cause wild errors, if there are unit circle errors, then this function will apply the required correction (+- 360deg)
def Unit_Circle_adjust(UE_RS_Phase):
    if UE_RS_Phase>180:
        return (UE_RS_Phase-360)
    if UE_RS_Phase<-180:
        return (UE_RS_Phase+360)
    else:
        return (UE_RS_Phase)
#lambda function applies to measurement data
UE_RS__Phases['Unit Circle Adjust'] = UE_RS__Phases.apply(lambda x:Unit_Circle_adjust(x['UE_RS_Phase']),axis=1)

UE_RS__Phases['Sw_Ph_Adj'] = [CompAngle2, CompAngle3, CompAngle4, CompAngle5, CompAngle6, CompAngle7, CompAngle8,]

#Dataframe that wraps up all of the calculations
UE_RS__Phases['UE_RS_Phase_Angle'] = UE_RS__Phases['Sw_Ph_Adj'] - UE_RS__Phases['Unit Circle Adjust']



end = timer()
print(round(end - start,3)) # Time in seconds, e.g. 5.380

print("Done8!!")
print('\a')

UE_RS__Phases.to_html('output.html')