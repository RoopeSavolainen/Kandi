import win32com.client as com
import os

from settings import *
import routing

def main():
    vissim = com.Dispatch(COM_NAME)
    base_path = os.path.dirname(os.path.abspath(__file__))
    vissim.LoadNet(base_path + FILENAME)
    
    use_congestion = False
    paths = routing.Pathfinder(vissim)
    
    vissim.Simulation.RunSingleStep()
    paths.update_routes()
    while vissim.Simulation.AttValue('IsRunning'):
        if vissim.Simulation.AttValue('SimSec') % PATHFINDING_PERIOD == 0 and use_congestion:
            paths.update_congestion()
            paths.update_routes()

        vissim.Simulation.RunSingleStep()


if __name__ == '__main__':
    main()
