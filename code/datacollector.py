import random

from settings import *

class DataCollector:
    vissim = None

    def __init__(self, vissim):
        self.vissim = vissim
        self.vissim.Evaluation.SetAttValue('DataCollCollectData', True)
        self.vissim.Evaluation.SetAttValue('DataCollInterval', DATACOLLECTION_INTERVAL)


    def create_measurement_points(self, connectors):
        points = self.vissim.Net.DataCollectionPoints
        measurements = self.vissim.Net.DataCollectionMeasurements
        for conn in connectors:
            lane = conn.Lanes.ItemByKey(1)
            p = points.AddDataCollectionPoint(points.Count+1, lane, 0.0)
            m = measurements.AddDataCollectionMeasurement(measurements.Count+1)
            m.SetAttValue('DataCollectionPoints', points.Count)

    
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

