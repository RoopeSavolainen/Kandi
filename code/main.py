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
    data = datacollector.DataCollector(vissim)

    path = os.path.dirname(os.path.abspath(__file__)) + FILENAME
    pre_path = path[0:-5] + '-pre.inpx'

    print_status('Loading network')
    if os.path.isfile(pre_path):
        print_status('Pre-processed network found')
        vissim.LoadNet(pre_path)
        paths = routing.Pathfinder(vissim, data, False)
    else:
        vissim.LoadNet(path)

        print_status('Initializing pathfinding')
        paths = routing.Pathfinder(vissim, data)

        print_status('Saving as pre-processed network')
        vissim.SaveNetAs(pre_path)

    if DISABLE_GUI:
        vissim.SuspendUpdateGUI()

    vissim.Simulation.SetAttValue('SimPeriod', SIMULATION_LENGTH)
    
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

