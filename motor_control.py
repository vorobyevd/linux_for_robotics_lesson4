#!/bin/python3

# imports
import numpy as np
from matplotlib import pyplot as plt
from motor_control.filter import LowpassFilter
from motor_control.regulator import PI_Regulator

# ************************************* Main application ******************************************

def main():
    
    # ********** Filter init **********

    # Parameters
    sampling_freq = 100 # sampling frequency Hz
    pass_freq = 2.5 # bandpass frequency

    # Init
    feedback_filter = LowpassFilter(pass_freq, sampling_freq)

    
    # ********* Regulator init ********

    # Parameters

    Kp = 5 # proportional gain
    Ki = 0.03 # integral gain
    max_action = 48 # max control action
    min_action = -48 # min control action
    
    # Init 
    speed_reg = PI_Regulator(Kp, Ki, min_action, max_action)

    # *********** Model init **********

    t_stop = 20 # simulation time
    t_model = np.linspace(0,t_stop,t_stop*sampling_freq) # time array
    k = 0.5  # model gain
    y0 = 0 # initial condition
    y = y0
    dt = 1/sampling_freq # time step
    control = 0 # initial control action
 
    # Simulation data buffers
    y_vals = []
    y_filtered_vals  = []
    control_vals = []
    setpoint_vals = []

    # Simulate model
    for t in t_model:

        # Setpoint profile generation
        if t > 2 and t < 5:
            setpoint = 5
        elif t > 5 and t < 10:
            setpoint = 10
        elif t > 10 and t < 15:
            setpoint = 5
        else:
            setpoint = 0
                

        # Model calculation
        dydt = -k*y + control      # Model differential equation
        y = y + dydt*dt            # Integrate 

        # Add feedback noize
        y_noize = 0.01 * np.random.normal()
        y = y + y_noize

        #Filter noisy feedback signal
        y_filtered = feedback_filter.calculate_out(y)
               
        # Calculate control action
        control = speed_reg.calculate(setpoint, y_filtered)

        # Collect simulation data
        control_vals.append(control)
        y_vals.append(y)           
        y_filtered_vals.append(y_filtered)
        setpoint_vals.append(setpoint)

    # ****** Plot simulation results ********

    fig,ax  = plt.subplots(2, 1)
    fig.tight_layout(pad=2.0)
    ax[0].plot(t_model,setpoint_vals, label = "Reference value")
    ax[0].plot(t_model,y_filtered_vals, label = "Actual value")
    ax[0].set_xlabel("Time (s)")
    ax[0].set_ylabel("Reference value")
    ax[0].set_title("Tracking reference value")
    ax[0].legend()
    ax[1].plot(t_model,control_vals, label = "Control")
    ax[1].set_xlabel("Time(s)")
    ax[1].set_ylabel("Control action (V)")
    ax[1].set_title("Regulator output")
    ax[1].legend()
    plt.show()

  
# Execute main application

if __name__ == "__main__":
    main()

    