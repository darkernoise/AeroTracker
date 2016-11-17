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

import scipy
import scipy.signal
import filterpy.kalman as kf
import typing
import bisect
import numpy as np
import multiprocessing as mp
from aero_tracker.params.at_sensor_cluster_params import ATSensorClusterParams

class SensorCalibrationItem(object):
    '''
    Memory resident sensor calibration matrix item.
    '''
    
    _sensor_id = ""
    _matrix = [] # [rssi,distance,rssi_delta,distance_delta]
    _sensor_device = None
    _device_coord = None
    _params = None
    _key_list = []
    
    @property
    def sensor_id(self):
        return self._sensor_id
    
    @property
    def matrix(self):
        return self._matrix
    
    def sort_matrix(self):
        self._matrix.sort(key=lambda r: r[0])
        self._key_list = []
        for val in self._matrix:
            self._key_list.append(val[0])
        return
    
    def get_distance(self, rssi):
        dist = 0
        if (self._key_list == None) or (len(self._key_list)==0):
            self.sort_matrix()
        if (self._key_list == None) or (len(self._key_list)==0):
            print('self._key_list == None')
            return dist
        right_indx = bisect.bisect_right(a=self._key_list, x=rssi)
        rssi_delta, dist_delta = self._get_deltas(right_indx)
        
        if (right_indx <= 0):
            #Value is less than first calibration
            rssi_inc = rssi
            ratio = rssi_inc / rssi_delta
            dist = dist_delta * ratio
        else:
            left_val = self._matrix[right_indx - 1]
            rssi_inc = rssi - left_val[0]
            ratio = rssi_inc / rssi_delta
            dist = left_val[1] + (dist_delta * ratio)

        return dist
    
    def add_calibration(self, xyz:typing.Tuple, rssi:float):
        try:
            coord = np.array([float(xyz[0]),float(xyz[1]),float(xyz[2])])
            dist = np.linalg.norm(self._device_coord - coord)
            if (not self._val_exists(rssi)):
                matrix = self._matrix
                matrix.append([rssi,dist])
        except Exception as ex:
            raise ex
        return
    
    def _val_exists(self, rssi):
        for val in self._matrix:
            if (val[0] == rssi):
                return True
        return False
    
    def _get_deltas(self, right_index)->typing.List:
        '''
        Returns the delta in rssi and distance for a given matrix step.  This has to be a 
        dynamically calculated property since since the matrix array is loaded potentially
        out of sequence and in successive calls.  
        '''
        matrix_cnt = len(self._matrix)
        if (right_index <= 0):
            #Value is less than first calibration
            right_val = self._matrix[0]
            if (len(right_val) == 2):
                #have not added deltas yet
                rssi_delta = right_val[0]
                dist_delta = right_val[1]
                right_val.append(rssi_delta)
                right_val.append(dist_delta)
                return rssi_delta,dist_delta
            else:
                return right_val[2],right_val[3]
        elif (right_index >= matrix_cnt):
            right_val = self._matrix[matrix_cnt - 1]
            if (len(right_val) == 2):
                left_val = self._matrix[matrix_cnt - 2]
                rssi_delta = np.abs(right_val[0] - left_val[0])
                dist_delta = np.abs(right_val[1] - left_val[1])
                right_val.append(rssi_delta)
                right_val.append(dist_delta)
                return rssi_delta,dist_delta
            else:
                return right_val[2],right_val[3]
        else:
            right_val = self._matrix[right_index]
            if (len(right_val) == 2):
                left_val = self._matrix[right_index - 1]
                rssi_delta = np.abs(right_val[0] - left_val[0])
                dist_delta = np.abs(right_val[1] - left_val[1])
                right_val.append(rssi_delta)
                right_val.append(dist_delta)
                return rssi_delta,dist_delta
            else:
                return right_val[2],right_val[3]
        return None

    def __init__(self, sensor_id:str, params:ATSensorClusterParams):
        '''
        Constructor
        '''
        self._matrix_cnt = 0
        self._key_list = []
        self._params = params
        self._sensor_id = sensor_id
        self._sensor_device = params.get_sensor_by_id(sensor_id)
        if (self._sensor_device == None):
            raise Exception("Sensor is not active")
        self._device_coord = np.array([self._sensor_device.X,self._sensor_device.Y,self._sensor_device.Z])
        return
    
class SensorCalibrationMatrix(object):
    '''
    Memory resident sensor calibration matrix.
    '''
    CALIBRATION_FILE = '/etc/popt/aero_tracker/at_sensor_calibration.dat'
    SEPERATOR = '|'
    
    mp_lock = None
    _sensors = None #typing.List[SensorCalibrationItem]
    _params = ATSensorClusterParams
    __instance = None
    
    _filter_window_size = 11 #Must be an odd number
    FILTER_POLYORDER = 2
    FILTER_DERIVATIVE = 0
    FILTER_DERIVATIVE_DELTA = 5.0

    @staticmethod
    def get_instance(params:ATSensorClusterParams):
#         if (SensorCalibrationMatrix.mp_lock == None):
#             SensorCalibrationMatrix.mp_lock = mp.Lock()
#         SensorCalibrationMatrix.mp_lock.acquire()
#         if (SensorCalibrationMatrix.__instance == None):
#             SensorCalibrationMatrix.__instance = SensorCalibrationMatrix(params)
#         SensorCalibrationMatrix.mp_lock.release()
#         return SensorCalibrationMatrix.__instance
        return SensorCalibrationMatrix(params)
    
    def get_sensor(self,sensor_id:str):
        if (self._sensors != None):
            for snsr in self._sensors:
                if (snsr.sensor_id == sensor_id):
                    return snsr
        if (self._sensors == None):
            self._sensors = []
        try:
            snsr = SensorCalibrationItem(sensor_id=sensor_id, params=self._params)
            self._sensors.append(snsr)
        except Exception as ex:
            print(ex)
            snsr = None
        return snsr
    
    def __init__(self, params:ATSensorClusterParams):
        self._params = params
        self._load_calibration_data()
        return
    
    def _add_calibration_line(self,dat_itms:typing.Tuple):
        i = 0
        num_items = len(dat_itms)
        while (i < num_items):
            itm = dat_itms[i]
            if (i == 0):
                #xyz
                itm = itm.replace('[', '')
                itm = itm.replace(']', '')
                xyz = itm.split(sep=',')
            else:
                sensor_id = itm
                i += 1
                rssi = float(dat_itms[i])
                snsr = self.get_sensor(sensor_id=sensor_id)
                if (snsr != None):
                    snsr.add_calibration(xyz=xyz, rssi=rssi)
            i += 1
        return
    
    def _load_calibration_data(self):
        calib_file = self.CALIBRATION_FILE
        fl = open(calib_file, "r");
        dat_raw = fl.read();
        dat_lines = dat_raw.split("\n");
        for dat_line in dat_lines:
            if (len(dat_line) == 0):
                pass
            elif ((dat_line[0] == "#") or (dat_line[0] == " ")):
                pass
            else:
                dat_itms = dat_line.split(self.SEPERATOR);
                self._add_calibration_line(dat_itms)
        self._sort_sensors()
        self._filter_smooth_sensor_values()
        return
    
    def _filter_smooth_sensor_values(self):
        '''
        Filter to smooth the sensor calibration values.  At this point,
        matrix is in the form [rssi,distance]
        '''
        for snsr in self._sensors:
            filter_dist = []
            for m in snsr.matrix:
                filter_dist.append(m[1])
            #run the filter
            filt_vals = scipy.signal.savgol_filter(x=filter_dist, window_length=self._filter_window_size, \
            polyorder=self.FILTER_POLYORDER, deriv=self.FILTER_DERIVATIVE, \
            delta=self.FILTER_DERIVATIVE_DELTA)
            #ensure that the distance does not decrease (values are reversed)
            dist = filt_vals[0]
            for i in range(0, len(snsr.matrix)):
                if (filt_vals[i] < dist):
                    dist = (filt_vals[i])
                    snsr.matrix[i][1] = filt_vals[i]
                else:
                    snsr.matrix[i][1] = dist
            
        return
    
    def _sort_sensors(self):
        '''
        Sorts the data in the sensor specific matrix.
        '''
        for snsr in self._sensors:
            snsr.sort_matrix()
        return
    
    
#Tester
# CONF_FILE = "/etc/popt/aero_tracker/at_sensors.conf"
# params = ATSensorClusterParams(CONF_FILE)
# obj = SensorCalibrationMatrix(params)
# snsr = obj.get_sensor('NP_SE_B')
# snsr.get_distance(-23)
        