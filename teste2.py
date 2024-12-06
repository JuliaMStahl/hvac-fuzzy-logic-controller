 # add E-Plus directory to path to be able to import API
import sys
sys.path.insert(0, 'C:\\EnergyPlusV24-2-0') 
from pyenergyplus.api import EnergyPlusAPI
from pyenergyplus.plugin import EnergyPlusPlugin

coolingSch_hndl = 0
outdoorT_hndl = 0
indoorT_hndl = 0
handleDone = False
printCounter = 0

def my_callback_function(state):
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
    # exchange information with EnergyPlus
    month = api.exchange.month(state) 
    hour = api.exchange.hour(state)
    day_of_week = api.exchange.day_of_week(state)
    day_of_month = api.exchange.day_of_month(state)
    holiday = api.exchange.holiday_index(state)
    print(f"-------- BEGIN PRINTS COUNT {printCounter} ---------")
    print(f"Month: {month}")
    print(f"Hour: {hour}")
    print(f"Day of Week: {day_of_week}")
    print(f"Day of Month: {day_of_month}")
    print(f"Holiday Index: {holiday}")
        
    # read variables
    outdoor_temp = api.exchange.get_variable_value(state, outdoorT_hndl)
    indoor_temp = api.exchange.get_variable_value(state, indoorT_hndl)
    print(f"Outdoor Temperature: {outdoor_temp:.2f}°C")
    print(f"Indoor Temperature: {indoor_temp:.2f}°C")
    print(f"-------- END PRINTS COUNT {printCounter} ---------")
    printCounter += 1

# initialize EPlus
api = EnergyPlusAPI()

#instance of the simulation
state = api.state_manager.new_state() 

# energyplus model calling point, callback function
api.runtime.callback_begin_system_timestep_before_predictor(state , my_callback_function)

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