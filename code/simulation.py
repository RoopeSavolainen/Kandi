from main import print_status
import datacollector
from settings import *

class SimulationRound:
    vissim = None
    inflow = None
    data = None

    original = []

    def __init__(self, vissim, inflow, data):
        self.vissim = vissim
        self.inflow = inflow
        self.data = data


    def setup_vehicle_inputs(self):
        m = self.vissim.Net.DynamicAssignment.DynAssignDemands.ItemByKey(1).Matrix
        self.original = [0] * m.RowCount * m.ColCount
        for i in range(m.RowCount):
            for j in range(m.ColCount):
                val = m.GetValue(i+1, j+1)
                self.original[i*m.ColCount + j] = val
                m.SetValue(i+1, j+1, val*self.inflow)


    def run(self):
        self.vissim.Simulation.SetAttValue('NumRuns', 1)
        self.vissim.Simulation.RunContinuous()

        self.data.save_measurements()
        
        m = self.vissim.Net.DynamicAssignment.DynAssignDemands.ItemByKey(1).Matrix
        for i in range(m.RowCount):  # Reset demand matrix
            for j in range(m.ColCount):
                val = self.original[i*m.ColCount + j]
                m.SetValue(i+1, j+1, val)

