'''
Created on Sep 7, 2016

@author: Joel Blackthorne

AeroTracker, Copyright (C) 2016 Joel Blackthorne
This file is part of AeroTracker.

AeroTracker is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

AeroTracker is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with AeroTracker.  If not, see <http://www.gnu.org/licenses/>.
'''

import typing
import multiprocessing as mp
from aero_tracker.sensor.sensor_calibration_matrix import SensorCalibrationMatrix
from aero_tracker.params.at_sensor_cluster_params import ATSensorClusterParams


class RSSIToDistance(object):
    '''
    Loads calibration data, creates a curve, and then uses the curve to fit the RSSI value and calculate a distance.
    Then, this class loads the calibration values to the directory store.
    '''
    mp_lock = None
    _sensor_calib = None #SensorCalibrationMatrix
    _sensor_id = ''
    
    def calc_distance(self, rssi:float)->float:
        return self._sensor_calib.get_distance(rssi)

    def __init__(self, sensor_id, params:ATSensorClusterParams, dir_store):
        '''
        Constructor
        '''
        if (RSSIToDistance.mp_lock == None):
            RSSIToDistance.mp_lock = mp.Lock()
        RSSIToDistance.mp_lock.acquire()
        self._sensor_id = sensor_id
        sensor_calib_matrix = SensorCalibrationMatrix.get_instance(params)
        self._sensor_calib = sensor_calib_matrix.get_sensor(sensor_id)
        #Save the calibration data to the directory store
        dir_store.set_sensor_calib_data(sensor_id=sensor_id, calib_data=self._sensor_calib.matrix)
        RSSIToDistance.mp_lock.release()
        return
    
    
    
        