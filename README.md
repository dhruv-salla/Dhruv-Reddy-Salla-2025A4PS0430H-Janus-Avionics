# Dhruv-Reddy-Salla-2025A4PS0430H-Janus-Avionics


# Task 1
About:
This program retrieves pressure data from a .csv file and processes it to extract altitude (P=rho*g*h) and velocity (differentiating using guassian filter) data of the rocket. This information is displayed on a single animated graph (velocity below alitude).

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
        |
[Removes errors and smooths data]
        |
[Converts pressure to altitude (P=rho*g*h)]
        |
[Differentiates altitude to get velocity]
        |
[Detects launch and apogee]
        |
[Sets up graph limits and parameters]
        |
[Creates a mask for each flight phase]
        |
[Intializes lines for each flight phase]
        |
[Creates invisible annotations for launch and apogee]
        |
[Sets up empty lines]
        |
[Fills the space below the lines]
        |
[Fills the space to create velocity graph]
        |
[Makes annotations visible at the right time]
        |
[Runs the animation]


# Task 2
About:
This circuit + program combination collects data on atmospheric force and processes it to extract altitude (P=rho*g*h) and velocity (differentiating using finite difference method) data of the rocket. This information is used to find the flight phase of the rocket and indicate it using LEDs (green = ascent, yellow = apogee, red = descent, no color = prelaunch). 

Instructions:
To initiate the program, set the force to the highest possible value (10N). Since this setup only measures atmospheric force, maximum force corresponds to lowest altitude and vice versa. 

How force is measured:
The force sensor is essentially a variable resistor that redirects current (corresponding to force applied) away from a fixed resistance. Since this arrangement gives a non_linear mapping of force to sensor output, the signal recieved has to be processed (exponetial curve fit) to mimic a linear map. Here, max force has been mapped to ground level and min force (-10N) has been mapped to ~80m (resembles real atmospheric force).

What the code does:
[Gets data from sensor]

