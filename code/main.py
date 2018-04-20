import win32com.client as com
import os
import sys
from datetime import datetime

from settings import *
import simulation
import datacollector
import figure

def main():
    print_status('Opening Vissim')
    vissim = com.Dispatch(COM_NAME)
    data = datacollector.DataCollector(vissim)

    print_status('Loading network')
    path = os.path.dirname(os.path.abspath(__file__)) + FILENAME
    vissim.LoadNet(path)

    if DISABLE_GUI:
        vissim.SuspendUpdateGUI()

    for inflow in INFLOW_VALUES:
        print_status('Running simulation with inflow multiplier %f' % inflow)

        sim = simulation.SimulationRound(vissim, inflow, data)
        sim.setup_vehicle_inputs()
        sim.run()

    print_status('All simulations done')
    fig = figure.Figures('graphs\\')
    fig.generate_graphs()


def print_status(msg):
    t = datetime.now().strftime('%H:%M:%S')
    print('[%s] %s' % (t, msg))
    sys.stdout.flush()

if __name__ == '__main__':
    main()

