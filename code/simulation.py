import routing

from settings import *

class SimulationRound:
    vissim = None
    paths = None
    total_inflow = None
    use_congestion = False

    def __init__(self, vissim, paths, inflow, use_congestion):
        self.vissim = vissim
        self.paths = paths
        self.total_inflow = inflow
        self.use_congestion = use_congestion

        self.paths.update_routes()
        # TODO: initialize vehicle inputs and measurements


    def run(self):
        self.vissim.Simulation.RunSingleStep()
        while self.vissim.Simulation.AttValue('IsRunning'):
            if self.use_congestion:
                current = self.vissim.Simulation.AttValue('SimSec')
                self.vissim.Simulation.SetAttValue('SimBreakAt', current+PATHFINDING_PERIOD)
                self.paths.update_congestion()
                self.paths.update_routes()

            self.vissim.Simulation.RunContinuous()

