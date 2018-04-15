import win32com.client as com
import os
from datetime import datetime

from settings import *
import routing

def main():
    vissim = com.Dispatch(COM_NAME)
    print_status('Vissim open')

    base_path = os.path.dirname(os.path.abspath(__file__))
    vissim.LoadNet(base_path + FILENAME)
    print_status('Net loaded')
    
    use_congestion = False
    paths = routing.Pathfinder(vissim)

    print_status('Pathfinding initialized')
    
    vissim.Simulation.RunSingleStep()
    paths.update_routes()
    while vissim.Simulation.AttValue('IsRunning'):
        if vissim.Simulation.AttValue('SimSec') % PATHFINDING_PERIOD == 0 and use_congestion:
            paths.update_congestion()
            paths.update_routes()
            print_status('Congestion data and pathfinding updated')

        vissim.Simulation.RunSingleStep()

    print_status('Simulation done')


def print_status(msg):
    t = datetime.now().strftime('%H:%M:%S')
    print('[%s]: %s' % (t, msg))

if __name__ == '__main__':
    main()

