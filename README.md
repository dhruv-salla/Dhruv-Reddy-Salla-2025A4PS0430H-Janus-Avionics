# Dhruv-Reddy-Salla-2025A4PS0430H-Janus-Avionics


# Task 1
About:  
This program retrieves pressure data from a .csv file and processes it to extract altitude (P=rho.g.h) and velocity (differentiating using guassian filter) data of the rocket. This information is displayed on a single animated graph (velocity below alitude).

Intructions:  
On running, the program asks the user to input framerate (Hz). The graph is animated based on this value because I was extremely annoyed repeatedly playing a 1fps animation and I'm sure you are too.

How the graph is drawn:  
The graph is color coded for each phases of the flight (prelaunch, ascent, apogee, and descent). This is done by drawning 4 separate objects corresponding to each phase. The limits for the object are set using masks.

Libraries used:  
pandas  
numpy  
matplotlib.pyplot  
matplotlib.animation  
scipy.signal  
scipy.ndimage  

What the code does:  
[Gets data from csv]  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|  
[Removes errors and smooths data]  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|  
[Converts pressure to altitude (P=rho.g.h)]  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|  
[Differentiates altitude to get velocity]  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|  
[Detects launch and apogee]  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|  
[Sets up graph limits and parameters]  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|  
[Creates a mask for each flight phase]  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|  
[Intializes lines for each flight phase]  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|  
[Creates invisible annotations for launch and apogee]  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|  
[Sets up empty lines]  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|  
[Fills the space below the lines]  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|  
[Fills the space to create velocity graph]  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|  
[Makes annotations visible at the right time]  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|  
[Runs the animation]  


# Task 2
About:  
This circuit + program combination collects data on atmospheric force and processes it to extract altitude (P=rho*g*h) and velocity (differentiating using finite difference method) data of the rocket. This information is used to find the flight phase of the rocket and indicate it using LEDs (green = ascent, yellow = apogee, red = descent, no color = prelaunch). 

Instructions:  
To initiate the program, set the force to the highest possible value (10N). Since this setup only measures atmospheric force, maximum force corresponds to lowest altitude and vice versa. 

How force is measured:  
The force sensor is essentially a variable resistor that redirects current (corresponding to force applied) away from a fixed resistance. Since this arrangement gives a non_linear mapping of force to sensor output, the signal recieved has to be processed (exponetial curve fit) to mimic a linear map. Here, max force has been mapped to ground level and min force (-10N) has been mapped to ~80m (resembles real atmospheric force).

How sensor errors are handled:  
To deal with erroneous sensor readings, data is collected every 20ms and the median of 5 readings is taken as the accurate reading giving a data point ever 0.1s.

What the code does:  
[Initialises IO pins and Serial]  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|  
[Sets all LEDs to off]  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|  
[Checks if max force is being applied before running the program]  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|  
[Gets ground pressure]  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|  
[Runs loop()]  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|  
[Gets pressure]  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|  
[Smooths pressure]  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|  
[Converts pressure to altitude]  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|  
[Differentiates altitude to get velocity]  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|  
[Checks launch condition and output]  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|  
[Checks ascent condition and output]  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|  
[Checks apogee condition and output]  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|  
[Checks descent condition and output]  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|  
[Give output on Serial]
