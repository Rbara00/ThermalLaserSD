# ThermalLaserSD
Code for Dr Michel Lemay's computerized laser diode system that can measure the withdrawal time to a heat stimulus applied to the plantar 
surface of the foot in a large animal model of spinal cord injury. The system provides automatic measurement of the paw withdrawal latency
time and stores the values for later export.

Clone the repo using the following,
    git clone https://github.com/Rbara00/ThermalLaserSD.git

"requirements.txt" contains all requirements needed to run the program. The program uses default Python3 libraries with the exception of 
openpyxl. Additionally, this can be simply installed using
    pip install openpyxl

There are two versions of the program, one containing a GUI under the "GUI" folder for maximum user friendliness, which is ran by, 
    Python3 laser_test_GUI.py       or      ./laser_test_GUI.py

or a no GUI, terminal-based version of the program under the "noGUI" folder, ran by
    Python3 laser_test.py       or      ./laser_test.py

Additionally, Solidworks Files are uploaded incase the Lens is damaged or should be modified, as well as the lid for the enclosure.

The Final Presentation for the goup may be found here, which contains thorough information about the design process as well as a video demonstration of the system at 18:10 
https://www.youtube.com/watch?v=Gu6zqBxIRyg&feature=youtu.be

Final Paper will be uploaded upon completion to act as manual for the system.
