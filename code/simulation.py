from main import print_status
from settings import *

class SimulationRound:
    vissim = None
    total_inflow = None

    def __init__(self, vissim, inflow):
        self.vissim = vissim
        self.total_inflow = inflow


    def setup_vehicle_inputs(self, inflow):
        return # TODO: redo this
        weight_sum = 0.0
        for i in self.vissim.Net.VehicleInputs:
            weight_sum += i.AttValue('Volume (1)')

        multi = inflow / weight_sum
        for i in self.vissim.Net.VehicleInputs:
            curr = i.AttValue('Volume (1)')
            i.SetAttValue('Volume (1)', curr*multi)


    def run(self):
        self.vissim.Simulation.RunContinuous()
        pass # TODO: collect data

