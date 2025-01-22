# HVAC Fuzzy Logic Controller

This repository contains a Heating, Ventilation, and Air Conditioning (HVAC) controller implemented using fuzzy logic principles. The controller is designed to simulate energy consumption by interfacing with the EnergyPlus simulation software through its Python API.

## Overview

Fuzzy logic provides a way to model control systems that handle the inherent uncertainty and imprecision associated with real-world environments. In this project, fuzzy logic is applied to manage HVAC operations, aiming to optimize energy consumption while maintaining desired comfort levels.

## Features

- **Fuzzy Logic Control**: Utilizes fuzzy inference systems to determine HVAC operational states based on input variables such as temperature and humidity.
- **EnergyPlus Integration**: Interfaces with EnergyPlus, a comprehensive building energy simulation program, to simulate and analyze energy consumption.
- **Python Implementation**: Leverages Python for scripting and controlling the simulation process, facilitating customization and extension.

## Repository Structure

- `1ZoneCoolingHVAC.idf`: An EnergyPlus input data file defining a single-zone cooling HVAC system.
- `1ZoneCoolingHVAC_FuzzyLogicController.py`: Python script implementing the fuzzy logic controller and managing the interaction with EnergyPlus API.
- `fortaleza.idf`: An EnergyPlus input data file tailored for the climate conditions of Fortaleza, Brazil.
- `weather/`: Directory containing weather data files required for the simulations.
- `references_idf/`: Directory with additional EnergyPlus input data files referenced by the main simulation files.
- `.gitignore`: Specifies files and directories to be ignored by Git.

## Getting Started

To replicate the simulations and utilize the fuzzy logic controller, follow these steps:

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/JuliaMStahl/hvac-fuzzy-logic-controller.git
   cd hvac-fuzzy-logic-controller

2. **Install Dependencies**: Ensure that Python and the necessary packages are installed. You can install the required Python packages using:
    ```bash
    pip install 

3. **Install EnergyPlus**: Download and install EnergyPlus from the official website. Ensure that the EnergyPlus executable is accessible in your system's PATH.

4. **Run the Simulation**: Execute the Python script to start the simulation:

    ```bash
    python 1ZoneCoolingHVAC_FuzzyLogicController.py

The script will initialize the fuzzy logic controller, set up the simulation environment, and run EnergyPlus with the specified input data files.

## Customization
You can modify the input data files (.idf) and the Python script to adapt the controller to different building configurations, climate conditions, or control strategies. Refer to the EnergyPlus documentation for details on input data file structure and available features.

## References
1. EnergyPlus: A whole building energy simulation program. More information and downloads are available at: https://energyplus.net

## License
This project is licensed under the MIT License. See the LICENSE file for details.