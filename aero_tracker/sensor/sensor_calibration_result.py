'''
Created on Sep 4, 2016

@author: Joel Blackthorne
'''

class SensorCalibrationResult(object):
    '''
    Result of sensor calibration at a specified X,Y,Z coordinate for a single sensor.
    '''
    
    sensor_id = ""
    X = 0.0
    Y = 0.0
    Z = 0.0
    rssi = 0


    def __init__(self, sensor_id, X, Y, Z, rssi):
        '''
        Constructor
        '''
        self.sensor_id = sensor_id
        self.X = X
        self.Y = Y
        self.Z = Z
        self.rssi = rssi
        return
        