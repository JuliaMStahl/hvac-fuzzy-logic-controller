import os
import opyplus as op

eplus_dir_path = op.get_eplus_base_dir_path((24,2,0))
# eplus_dir_path = 'C:/Users/julia/EnergyPlus'

print(eplus_dir_path)

# idf path
idf_path = os.path.join(
    eplus_dir_path,
    "ExampleFiles",
    "1ZoneEvapCooler.idf"
)

# epw path
epw_path = os.path.join(
    eplus_dir_path,
    "WeatherData",
    "USA_CA_San.Francisco.Intl.AP.724940_TMY3.epw"
)

# run simulation
s = op.simulate(idf_path, epw_path, "my-first-simulation")