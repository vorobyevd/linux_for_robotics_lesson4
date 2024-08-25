#!/bin/python3

# imports
import numpy as np
from matplotlib import pyplot as plt
from motor_control_module.filter import LowpassFilter
from motor_control_module.regulator import PI_Regulator
import yaml

# ************************************* Main application ******************************************

def main():
    
    # ******* Read configuration ******
    
    # Read application configuration from yaml file
    with open("config.yaml") as f:
        app_config = yaml.load(f, Loader=yaml.FullLoader)

    
    # ********** Filter init **********

    # Read configuration
    sampling_freq   = app_config['general_params']['sampling_frequency']#100 # sampling frequency Hz
    pass_freq       = app_config['feedback_filter_params']['pass_frequency']#2.5 # bandpass frequency

    # Init
    feedback_filter = LowpassFilter(pass_freq, sampling_freq)

    
    # ********* Regulator init ********

    # Parameters

    # Read configuration
    Kp         = app_config['regulator_params']['Kp'] # 5 # proportional gain
    Ki         = app_config['regulator_params']['Ki'] # 0.03 # integral gain
    max_action = app_config['regulator_params']['max_action'] # 48 # max control action
    min_action = app_config['regulator_params']['min_action'] # -48 # min control action
    
    # Init 
    speed_reg = PI_Regulator(Kp, Ki, min_action, max_action)

    # *********** Model init **********

    # Read configuration
    t_stop      = app_config['general_params']['T_stop'] # 20 # simulation time
    k           = app_config['imitation_model_params']['Gain'] # 0.5  # model gain
    y0          = app_config['imitation_model_params']['Initial_cond'] # initial condition
    noise_amp   = app_config['imitation_model_params']['Noise_amplitude']
    
    y = y0
    dt = 1/sampling_freq # time step
    control = 0 # initial control action
    t_model     = np.linspace(0,t_stop,t_stop*sampling_freq) # time array

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
        y_noize = noise_amp * np.random.normal()
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

    