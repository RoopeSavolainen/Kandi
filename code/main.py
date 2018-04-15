import win32com.client as com
import os
import sys
from datetime import datetime

from settings import *
import simulation
import routing
import datacollector

def main():
    print_status('Opening Vissim')
    vissim = com.Dispatch(COM_NAME)

    print_status('Loading network')
    base_path = os.path.dirname(os.path.abspath(__file__))
    vissim.LoadNet(base_path + FILENAME)
    
    data = datacollector.DataCollector(vissim)

    print_status('Initializing pathfinding')
    paths = routing.Pathfinder(vissim, data)

    if DISABLE_GUI:
        vissim.SuspendUpdateGUI()
    
    for inflow in INFLOW_VALUES:
        print_status('Running simulations with total vehicle inflow %d' % inflow)

        print_status('Starting non-congestion run')
        sim = simulation.SimulationRound(vissim, paths, inflow, False)
        sim.run()

        print_status('Starting congestion run')
        sim = simulation.SimulationRound(vissim, paths, inflow, True)
        sim.run()

    print_status('All simulations done')


def print_status(msg):
    t = datetime.now().strftime('%H:%M:%S')
    print('[%s] %s' % (t, msg))
    sys.stdout.flush()

if __name__ == '__main__':
    main()

