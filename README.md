# Beamforming-tester
Beamforming tester for TM7 LTE Base station using VSE and RTO Oscilloscope

Using an RTO Oscilloscope, and R&S Vector Signal Explorer software I built a measurement system to measure the phase relationships of the UE-RS transmitted by each of the 8 RF paths of the base station.

Steps to Success:
1. St up the RTO and VSE to attach to the base station by loading a pre-built config file (to be turned into SCPI commands later)
2. Set up the UE to attach to the Base station, provide the UE with a simulated location via the Orolia GPS simulator that will place it in one of the 13 TM 7 beams of the Base station
3.
4. Set the SP4T switches to measure antenna ports 1,2,3, and 4
5. Calibration file for antenna ports 1,2,3,4 is configured in VSE
6. Attach the UE to the base station
7. Using iPerf, run a high rate data session to "busy up" the Downlink LTE channel with PDSCH and UE-RS
8. The "FullRB" function will loop until the PDSCH allocation is full in 1 subframe
9. A while loop runs that pulls the UE RS phase angles and stores them to a variable each
10. steps 4-9 are run for the configurations of antenna ports 1,5,6, and 7 along with antenna ports 1 and 8
11. Calibration factors are applied
12. Unit circle errors are accounted for
13. UE-RS phases are written to HTML file.
14. 
