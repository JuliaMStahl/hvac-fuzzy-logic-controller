 # add E-Plus directory to path to be able to import API
import sys
sys.path.insert(0, 'C:\\EnergyPlusV24-2-0') 
from pyenergyplus.api import EnergyPlusAPI # type: ignore
from pyenergyplus.plugin import EnergyPlusPlugin # type: ignore
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt

coolingSch_hndl = 0
outdoorT_hndl = 0
indoorT_hndl = 0
handleDone = False
printCounter = 0

# 1. Definition of input and output variables
external_temp = ctrl.Antecedent(np.arange(0, 46, 1), 'external_temp')  # 0 to 45°C
internal_temp = ctrl.Antecedent(np.arange(0, 46, 1), 'internal_temp')  # 0 to 45°C
power = ctrl.Consequent(np.arange(0, 4.1, 0.1), 'power')               # 0 to 4

# 2. Definition of fuzzy sets
# External temperature
external_temp['low'] = fuzz.trimf(external_temp.universe, [0, 0, 18])
external_temp['medium'] = fuzz.trimf(external_temp.universe, [15, 25, 35])
external_temp['high'] = fuzz.trimf(external_temp.universe, [30, 45, 45])

# Internal temperature
internal_temp['cold'] = fuzz.trimf(internal_temp.universe, [0, 0, 18])
internal_temp['comfortable'] = fuzz.trimf(internal_temp.universe, [16, 22, 28])
internal_temp['hot'] = fuzz.trimf(internal_temp.universe, [25, 45, 45])

# Air conditioner power
power['off'] = fuzz.trimf(power.universe, [0, 0, 1])
power['low'] = fuzz.trimf(power.universe, [0, 1, 2])
power['medium'] = fuzz.trimf(power.universe, [1.5, 2.5, 3.5])
power['high'] = fuzz.trimf(power.universe, [3, 4, 4])

# 3. Fuzzy rules
rule1 = ctrl.Rule(external_temp['low'] & internal_temp['cold'], power['off'])
rule2 = ctrl.Rule(external_temp['low'] & internal_temp['comfortable'], power['off'])
rule3 = ctrl.Rule(external_temp['medium'] & internal_temp['comfortable'], power['low'])
rule4 = ctrl.Rule(external_temp['high'] & internal_temp['hot'], power['high'])
rule5 = ctrl.Rule(external_temp['medium'] & internal_temp['hot'], power['medium'])
rule6 = ctrl.Rule(external_temp['high'] & internal_temp['comfortable'], power['medium'])
rule7 = ctrl.Rule(external_temp['high'] & internal_temp['cold'], power['low'])

# 4. Creation of the control system
power_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7])
power_simulator = ctrl.ControlSystemSimulation(power_ctrl)

# 5. Simulation
def simulate(ext_temp, int_temp):
    power_simulator.input['external_temp'] = ext_temp
    power_simulator.input['internal_temp'] = int_temp
    power_simulator.compute()
    result = power_simulator.output['power']
    return result

def actuate(state, x):
    api.exchange.set_actuator_value(state, coolingSch_hndl, x)

def fuzzy_logic_callback_function(state):
     # global variables are necessary as the callback function takes only one input: state
    global coolingSch_hndl, coolingSP_hndl, outdoorT_hndl, indoorT_hndl, handleDone, printCounter
    # get handles
    if not handleDone:
        # Check data exchange API is ready
        if api.exchange.api_data_fully_ready(state):
            # Get handles
            coolingSch_hndl = api.exchange.get_actuator_handle(state, "Schedule:Compact", "Schedule Value", "TZ-1 Thermostat Schedule")
            outdoorT_hndl = api.exchange.get_variable_handle(state,'Site Outdoor Air Drybulb Temperature', 'Environment')
            indoorT_hndl = api.exchange.get_variable_handle(state,'Zone Mean Air Temperature', 'TZ-1')
            # Check if got all handles
            if -1 in [coolingSch_hndl, indoorT_hndl,outdoorT_hndl]:
                print(f"Error: Failed to retrieve one or more handles:")
                print(f"  coolingSch_hndl: {coolingSch_hndl}")
                print(f"  outdoorT_hndl: {outdoorT_hndl}")
                print(f"  indoorT_hndl: {indoorT_hndl}")
                sys.exit(1)
            handleDone = True
        else:
            return
    
    # read variables
    outdoor_temp = api.exchange.get_variable_value(state, outdoorT_hndl)
    indoor_temp = api.exchange.get_variable_value(state, indoorT_hndl)

    result = simulate(outdoor_temp, indoor_temp)
    actuate(state, result)

# initialize EPlus
api = EnergyPlusAPI()

#instance of the simulation
state = api.state_manager.new_state() 

# energyplus model calling point, callback function
api.runtime.callback_begin_system_timestep_before_predictor(state , fuzzy_logic_callback_function)

# run EPlus
epwFile = 'BRA_Salvador.832290_SWERA.epw'
idfFile =  'teste1.idf'
output_folder = 'out'
# -x short form to run expandobjects for HVACtemplates. see EnergyPlusEssentials.pdf p16
cmd_args = ['-w',epwFile, '-d', output_folder,'-x',idfFile]
api.runtime.run_energyplus(state,cmd_args)

# delete state after simulation to free the memory
api.state_manager.delete_state(state)

print("Handles done: {}".format(handleDone))