'''
Created on Aug 13, 2016

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
import numpy as np
import filterpy.kalman as kf
# from filterpy.common import Q_discrete_white_noise
from typing import List, Tuple

class KalmanFilterQueue(object):
    '''
    First pass of filtering Aero Tracker data.  This filter runs a Kalman filter on the 
    distances received from each sensor.
    
    Code based on:
    
    * Kalman Filter documentation at: http://en.wikipedia.org/wiki/Kalman_filter
    
    * Book by Roger Labbe:
    
        https://github.com/rlabbe/Kalman-and-Bayesian-Filters-in-Python
        
    * http://quant-econ.net/py/kalman.html
    
    '''    
    MEASURE_NOISE_VARIANCE = 8 #Amount of noise most likely found in measures
    SENSOR_NOMINAL_RANGE = 300
    
    _filter = None
    _num_entries = 0
    _last_time_change = 0.0
    _avg_time_change = 0.0 #Stores average time change
    _calc_time_change = 0.0 #Working value for calculating the time change
    _raw = [] #Raw data points
    _data = [] #Filtered data points
    _timestamps = [] #Timestamps for data points
    
    def enqueue(self, val:float, timestamp:float)->Tuple[float,float,float]: 
        '''
        Filters entries at N-1 and return values.
        
        Returns Filtered data, Raw data, Timestamp
        '''
        rval = None
        self._num_entries += 1
        self._timestamps.append(timestamp)
        self._raw.append(val)
        
        if (self._num_entries < 2):
            self._data.append(val)
        else:
            self._covariance_calc(timestamp)
            if (self._num_entries == 2):
                self._init_filter(val0=self._data[0], ts0=self._timestamps[0], val1=val, ts1=timestamp)
            #Execute filter to fill the data array
            self._exec_filter(val, timestamp)
            #Prepare return results
            r_tmstmp = self._timestamps[0]
            self._timestamps.pop(0)
            self._calc_time_change -= r_tmstmp
            r_raw = self._raw[0]
            self._raw.pop(0)
            r_data = self._data[0]
            self._data.pop(0)
            self._num_entries -= 1
            return r_data, r_raw, r_tmstmp 
        
        return val, val, timestamp
    
    def flush(self):
        '''
        returns all values waiting
        '''
        rval = []
        for i in range(self._num_entries,0,-1):
            rval.append([self._data[i-1], self._raw[i-1], self._timestamps[i-1]])
    
        self._raw = []
        self._data = []
        self._timestamps = []
        return rval
    
    def __init__(self):
        '''
        Constructor
        '''
        return
    
    def _exec_filter(self, val:float, timestamp:float):
        self._filter.predict()
        self._filter.update(val)
        fltrval = self._filter.x
        self._data.append(fltrval[0])
        return
    
    def _init_filter(self, val0:float, ts0:float, val1:float, ts1:float):
        '''
        ts = timestamp.
        '''
        dt = ts1 - ts0 #Velocity
        self._filter = kf.KalmanFilter(dim_x=2, dim_z=1)   
        self._filter.x = np.array([val0,dt]) #Initial state of position and velocity
        self._filter.F = np.array([[1.,dt], \
                                   [0.,1.]])# state transition matrix
        self._filter.H = np.array([[1.,0.]]) # Measurement function
#         self._filter.P = np.array([[val1, 0.],[0.,dt]]) # covariance matrix with known starting positions set
        self._filter.P *= 500.                 # covariance matrix
        self._filter.R = self.SENSOR_NOMINAL_RANGE                  # state uncertainty
        self._filter.Q = self.MEASURE_NOISE_VARIANCE #(2,.1,.1) #Q_discrete_white_noise(2, dt, .1) # process uncertainty
#         self._filter.Q = Q_discrete_white_noise(dim=2, dt=dt, var=self.MEASURE_NOISE_VARIANCE)
        return
    
    def _covariance_calc(self, timestamp:float):
        if (self._num_entries == 0):
            #first entry
            return
        self._last_time_change = timestamp - self._timestamps[self._num_entries - 2]
        self._calc_time_change += self._last_time_change
        self._avg_time_change = self._calc_time_change / ( self._num_entries  - 1 )
#         self._r = self._avg_time_change
        return


# #####################################    
# #Tester
# #####################################
# import time
# import matplotlib.pyplot as plt
# 
# #Data arrays to plot
# NUM_SAMPLES = 30
# adata = np.empty((NUM_SAMPLES),dtype=np.float)
# sdata = np.empty((NUM_SAMPLES),dtype=np.float)
# fdata = np.empty((NUM_SAMPLES),dtype=np.float)
# tdata = np.empty((NUM_SAMPLES),dtype=np.float)
# 
# #Generate data points
# obj = KalmanFilterQueue()
# 
# act_dist = 4
# tm_strt = time.time()
# tm = time.time()
# noise = 4 * np.random.random(NUM_SAMPLES)
# for i in range(0,NUM_SAMPLES):
#     act_data = act_dist + i
#     tm += 0.1
#     tdata[i] = tm
#     adata[i] = act_data
#     if (i % 2 == 0):
#         noise_data = act_data + noise[i]
#     else:
#         noise_data = act_data - noise[i]
#     sdata[i] = noise_data
#     flt_data = obj.enqueue(val=noise_data, timestamp=tm)
#     if (i > 0):
#         fdata[i-1] = flt_data[0]
#         
# #Fix the last data sample
# flt_data = obj.flush()
# fdata[NUM_SAMPLES-1] = flt_data[0][0]
# 
# fig, ax = plt.subplots()
# ax.grid(True)
# 
# ln_act = ax.plot(tdata, adata, 'bo')
# ln_sg = ax.plot(tdata, sdata, 'r--')
# ln_fl = ax.plot(tdata, fdata, lw=2,c='g')
# plt.legend((ln_act[0], ln_sg[0], ln_fl[0]), ('actual', 'signal', 'filtered'), loc=2)
# plt.show()
    