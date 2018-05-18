# Simulation code
This folder contains the code used for running the simulation as mentioned in the thesis. The code is shipped with the network file used in the thesis (see `data/helsinki.inpx`), but it should work with any Vissim network file with a defined dynamic demand matrix and any number of data collection points.

## Installation
The code uses the libraries listed in `requirements.txt`. They can be installed with the command `pip install -r requirements.txt`.

## Running
Start the simulation by running `python main.py`.

## Licensing
All the python code is licensed under the permissive MIT license (see `LICENSE`), so it can be liberally modified and used for open source, academic or commercial purposes as needed.
The Vissim network data (see `data/helsinki.inpx`) is based on OpenStreetMap open map data. Therefore it is a derivative work of the used data, and hence licensed under the ODC Open Database License (see `data/LICENSE`).
