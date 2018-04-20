import random

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
        data = json.load(result_file)
        result_file.close()

        for i in measurements.Count:
            pass # TODO: modify data

        result_file = open(RESULT_FILE, 'w')
        json.dump(data, result_file)
        result_file.close()

    
    def get_flow(self, n, entire_run=False):
        per = 'Avg' if entire_run else 'Last'
        res = self.vissim.Net.DataCollectionMeasurements.ItemByKey(n).AttValue('Vehs  (Current,%s,All)' % per)
        return res if res is not None else 0.0

    
    def get_speed(self, n, entire_run=False):
        per = 'Avg' if entire_run else 'Last'
        res = self.vissim.Net.DataCollectionMeasurements.ItemByKey(n).AttValue('SpeedAvgArith  (Current,%s,All)' % per)
        return res if res is not None else 0.0

    
    def get_density(self, n, entire_run=False):
        flow = self.get_flow(n, entire_run)
        if flow == 0:
            return 0.0
        spd = self.get_speed(n, entire_run)
        res = flow/spd
        return res if res is not None else 0.0

