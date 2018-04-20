import random
import math

from settings import *
import json

class DataCollector:
    vissim = None

    def __init__(self, vissim):
        self.vissim = vissim
        self.vissim.Evaluation.SetAttValue('DataCollCollectData', True)
        self.vissim.Evaluation.SetAttValue('DataCollInterval', DATACOLLECTION_INTERVAL)


    def save_measurements(self):
        measurements = self.vissim.Net.DataCollectionMeasurements
        result_file = open(RESULT_FILE, 'r')
        try:
            data = json.load(result_file)
        except ValueError:
            data = json.loads('{}')
        result_file.close()

        num_periods = int(math.ceil(self.vissim.Simulation.AttValue('SimPeriod') / self.vissim.Evaluation.AttValue('DataCollInterval')))
        for m in measurements:
            name = m.AttValue('Name')
            for n in range(num_periods):
                flw = self.get_flow(m, n+1)
                spd = self.get_speed(m, n+1)
                dns = self.get_density(m, n+1)

                if name not in data:
                    data[name] = []
                data[name].append((flw, spd, dns))


        result_file = open(RESULT_FILE, 'w')
        json.dump(data, result_file)
        result_file.close()

    
    def get_flow(self, meas, period):
        res = meas.AttValue('Vehs  (Current,%d,All)' % period)
        res *= 60 / DATACOLLECTION_INTERVAL  # Conversion to vehicles/min
        return res if res is not None else 0.0

    
    def get_speed(self, meas, period):
        res = meas.AttValue('SpeedAvgArith  (Current,%d,All)' % period)
        return res if res is not None else 0.0

    
    def get_density(self, meas, period):
        flow = self.get_flow(meas, period)
        if flow == 0:
            return 0.0
        spd = self.get_speed(meas, period) * 16.67  # Conversion to m/min
        res = flow/spd
        return res if res is not None else 0.0

