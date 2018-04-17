import routing

from main import print_status
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
        self.setup_vehicle_inputs(inflow)


    def setup_vehicle_inputs(self, inflow):
        weight_sum = 0.0
        for i in self.vissim.Net.VehicleInputs:
            weight_sum += i.AttValue('Volume (1)')

        multi = inflow / weight_sum
        for i in self.vissim.Net.VehicleInputs:
            curr = i.AttValue('Volume (1)')
            i.SetAttValue('Volume (1)', curr*multi)


    def run(self):
        self.vissim.Simulation.RunSingleStep()
        while self.vissim.Simulation.AttValue('IsRunning'):
            if self.use_congestion:
                current = self.vissim.Simulation.AttValue('SimSec')
                self.vissim.Simulation.SetAttValue('SimBreakAt', current+PATHFINDING_PERIOD)
                self.paths.update_congestion()
                self.paths.update_routes()
                print_status('= Continuing simulation')

            self.vissim.Simulation.RunContinuous()

