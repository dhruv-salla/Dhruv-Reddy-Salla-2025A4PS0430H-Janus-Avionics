import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from scipy.signal import savgol_filter
from scipy.ndimage import gaussian_filter1d


# inputs

# user input for framerate
framerate = float(input("Enter Framerate (Hz): "))

# reading csv
flight_data = pd.read_csv("Raw_Test_Flight_Data_25 - Sheet1.csv")
flight_data.rename(columns= {"Pressure (Pa)": "Data"}, inplace= True)
flight_data.index.name = "Time (s)"


# processing data

# turning raw data into numpy numbers
flight_data["Pressure (Pa)"] = pd.to_numeric(flight_data["Data"], errors='coerce')

# function to convert pressure to altitude
def pressure_to_altitude(pressure):
    g = 9.81
    air_density = 1.225
    pressure_at_ground_level = flight_data["Pressure (Pa)"][0]
    delta_pressure = pressure_at_ground_level - pressure
    altitude = delta_pressure / (g * air_density)
    return altitude

# filter to detect and replace bad data points
def outlier_filter(prev_val, cur_val, next_val):
    true_avg = (prev_val + next_val) / 2
    val_range = np.abs(next_val - prev_val)
    lower_bound = true_avg - (val_range * 0.95)
    upper_bound = true_avg + (val_range * 0.95)
    if lower_bound < cur_val < upper_bound:
        return False
    else:
        return True

# removing errors
# step 1: handling corrupted pressure values with interpolation
flight_data["Pressure (Pa)"] = flight_data["Pressure (Pa)"].interpolate(method= 'linear', limit= 3, limit_area= 'inside')
# step 2: replacing strong outliers with local average (low resolution)
for i in range(1, len(flight_data["Pressure (Pa)"]) - 1):
    if outlier_filter(flight_data.loc[i - 1, "Pressure (Pa)"], flight_data.loc[i, "Pressure (Pa)"], flight_data.loc[i + 1, "Pressure (Pa)"]):
        flight_data.loc[i, "Pressure (Pa)"] = (flight_data.loc[i - 1, "Pressure (Pa)"] + flight_data.loc[i + 1, "Pressure (Pa)"]) / 2
# step 3: smoothing data further with local averaging (high resolution) ---
for i in range(1, len(flight_data["Pressure (Pa)"]) - 1):
    flight_data.loc[i, "Pressure (Pa)"] = (flight_data.loc[i - 1, "Pressure (Pa)"] + flight_data.loc[i, "Pressure (Pa)"] + flight_data.loc[i + 1, "Pressure (Pa)"]) / 3

# adding and smmothing altitude data
flight_data["raw Altitude (m)"] = flight_data["Pressure (Pa)"].apply(pressure_to_altitude)
flight_data["Altitude (m)"] = flight_data["raw Altitude (m)"].rolling(window= 7, center= True, min_periods= 1).mean()
flight_data["Altitude (m)"] = savgol_filter(flight_data["Altitude (m)"], window_length= 5, polyorder= 3, mode= 'nearest')

# calculating and smoothing velocity
flight_data["Altitude (m)"] = flight_data["Altitude (m)"].to_numpy()
flight_data["Velocity (m/s)"] = gaussian_filter1d(flight_data["Altitude (m)"], sigma=1.0, order=1, mode='reflect')

# detecting launch (when velocity > 1) and apogee (when velocity changes sign)
t_launch = np.argmax(flight_data["Velocity (m/s)"] > 1)
for i in range(t_launch, len(flight_data)-1):  
    if flight_data.loc[i, "Velocity (m/s)"] > 0 and flight_data.loc[i + 1, "Velocity (m/s)"] < 0:
        slope = flight_data.loc[i, "Velocity (m/s)"] / (flight_data.loc[i, "Velocity (m/s)"] - flight_data.loc[i + 1, "Velocity (m/s)"])  
        t_apogee = i + slope 
        h = flight_data["Altitude (m)"][i] + slope * (flight_data["Altitude (m)"][i+1] - flight_data["Altitude (m)"][i])  
        raw_apogee = flight_data["Altitude (m)"].max()
        raw_apogee_time = flight_data.index[flight_data["Altitude (m)"] == raw_apogee][0]
        if raw_apogee - 1 < h < raw_apogee + 1:
            alt_apogee = h
        break;


# graphs

# graph setup
plt.style.use('dark_background')
fig, ax1 = plt.subplots(figsize= (6,5))
ax2 = ax1.twinx()
ax1.set_facecolor("black")
ax1.set_xlabel("Time (s)", color="white")
ax1.set_ylabel("Altitude (m)", color="white")
ax2.set_ylabel("Velocity (m/s)", color="white")
ax1.grid(color= 'gray', alpha= 0.3)
ax1.set_xlim(0, flight_data.index.max())
ax1.set_ylim(-150, (flight_data["Altitude (m)"].max()) * 1.1)
ax2.set_ylim((flight_data["Velocity (m/s)"].min() * 3) + 50, (flight_data["Velocity (m/s)"].max() * 3) + 50)
for spine in ax1.spines.values():
    spine.set_visible(False)
for spine in ax2.spines.values():
    spine.set_visible(False)

# masks for flight phases
end = len(flight_data) - 1
mask_ascent = (flight_data.index >= t_launch) & (flight_data.index <= raw_apogee_time - 1)
mask_descent = (flight_data.index >= raw_apogee_time + 1) & (flight_data.index <= end)
mask_apogee = (raw_apogee_time - 1 <= flight_data.index) & (flight_data.index <= raw_apogee_time + 1)
mask_prelaunch = (flight_data.index <= t_launch)

# initializing line objects for each flight phase
line11, = ax1.plot([],[], 'gray', lw=2, label= "altitude prelaunch")
line12, = ax1.plot([],[], 'lime', lw=2, label= "altitude ascent")
line13, = ax1.plot([],[], 'yellow', lw=2, label= "altitude apogee")
line14, = ax1.plot([],[], 'red', lw=2, label= "altitude descent")

# liftoff and apogee annotatations
ann1 = ax1.annotate(f'Liftoff \nT + 00:00:{t_launch}', 
                    xy= (t_launch, flight_data["Altitude (m)"][t_launch]), 
                    xytext= (t_launch - 15, flight_data["Altitude (m)"][t_launch] + 50), 
                    arrowprops= dict(arrowstyle= '-', color= 'white', connectionstyle= "arc3,rad=0.3"), 
                    bbox= dict(boxstyle= 'round,pad=0.3', fc= 'white', ec= 'none'), 
                    color= 'black')
ann1.set_visible(False)

ann2 = ax1.annotate(f'Apogee \nT + 00:00:{round(t_apogee, 2)}\n{round(alt_apogee, 2)}m', 
                    xy= (raw_apogee_time, raw_apogee), 
                    xytext= (raw_apogee_time - 27, raw_apogee - 100), 
                    arrowprops= dict(arrowstyle= '-', color= 'white', connectionstyle= "arc3,rad=-0.15"), 
                    bbox=dict(boxstyle= 'round,pad=0.3', fc= 'white', ec= 'none'), 
                    color= 'black')
ann2.set_visible(False)

# scatter dots for liftoff and apogee markers
dot1 = ax1.scatter([t_launch], [flight_data["Altitude (m)"][t_launch]], color="white", s=40, zorder=5)
dot1.set_visible(False)

dot2 = ax1.scatter([raw_apogee_time], [raw_apogee], color="white", s=40, zorder=5)
dot2.set_visible(False)


# animation

# animation init function
def init():
    line11.set_data([],[])
    line12.set_data([],[])
    line13.set_data([],[])
    line14.set_data([],[])
    return line11, line12, line13, line14

# animation update function
def update(frame):
    # update altitude lines for each phase
    line11.set_data(flight_data.index[:frame][mask_prelaunch[:frame]], flight_data["Altitude (m)"][:frame][mask_prelaunch[:frame]])
    line12.set_data(flight_data.index[:frame][mask_ascent[:frame]], flight_data["Altitude (m)"][:frame][mask_ascent[:frame]])
    line13.set_data(flight_data.index[:frame][mask_apogee[:frame]], flight_data["Altitude (m)"][:frame][mask_apogee[:frame]])
    line14.set_data(flight_data.index[:frame][mask_descent[:frame]], flight_data["Altitude (m)"][:frame][mask_descent[:frame]])

    # fill areas under altitude curve
    fill11 = ax1.fill_between(flight_data.index[:frame][mask_prelaunch[:frame]], -150, flight_data["Altitude (m)"][:frame][mask_prelaunch[:frame]], color= 'gray', alpha= 0.2)
    fill12 = ax1.fill_between(flight_data.index[:frame][mask_ascent[:frame]], -150, flight_data["Altitude (m)"][:frame][mask_ascent[:frame]], color= 'lime', alpha= 0.2)
    fill13 = ax1.fill_between(flight_data.index[:frame][mask_apogee[:frame]], -150, flight_data["Altitude (m)"][:frame][mask_apogee[:frame]], color= 'yellow', alpha= 0.2)
    fill14 = ax1.fill_between(flight_data.index[:frame][mask_descent[:frame]], -150, flight_data["Altitude (m)"][:frame][mask_descent[:frame]], color= 'red', alpha= 0.2)

    # fill areas under velocity curve
    fill21 = ax2.fill_between(flight_data.index[:frame][mask_prelaunch[:frame]], 0, flight_data["Velocity (m/s)"][:frame][mask_prelaunch[:frame]], color= 'gray', alpha= 0.4)
    fill22 = ax2.fill_between(flight_data.index[:frame][mask_ascent[:frame]], 0, flight_data["Velocity (m/s)"][:frame][mask_ascent[:frame]], color= 'lime', alpha= 0.4)
    fill23 = ax2.fill_between(flight_data.index[:frame][mask_apogee[:frame]], 0, flight_data["Velocity (m/s)"][:frame][mask_apogee[:frame]], color= 'yellow', alpha= 0.4)
    fill24 = ax2.fill_between(flight_data.index[:frame][mask_descent[:frame]], 0, flight_data["Velocity (m/s)"][:frame][mask_descent[:frame]], color= 'red', alpha= 0.440)

    # reveal liftoff marker once past launch
    if (frame > t_launch):
        ann1.set_visible(True)
        dot1.set_visible(True)

    # reveal apogee marker once past apogee
    if (frame > t_apogee):
        ann2.set_visible(True)
        dot2.set_visible(True)

    return line11, line12, line13, line14, fill11, fill12, fill13, fill14, fill21, fill22, fill23, fill24, ann1, ann2, dot1, dot2

# running animation
ani = animation.FuncAnimation(fig, update, frames= range(1, len(flight_data.index)), init_func= init, interval= (1000/framerate), blit= True, repeat= False)

# final plot formatting
plt.title("Flight Profile", color="white", fontsize=14)
plt.show()