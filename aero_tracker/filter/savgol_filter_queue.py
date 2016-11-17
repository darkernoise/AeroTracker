'''
Created on Aug 22, 2016

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
import math
from typing import Tuple

class SavGolFilterQueue(object):
    '''
    classdocs
    '''
    
    _filter_buffer_size = 20
    _filter_window_size = 7 #Must be an odd number
    FILTER_POLYORDER = 2
    FILTER_DERIVATIVE = 0
    FILTER_DERIVATIVE_DELTA = 1.0
    
    _params = None
    #Note: These arrays below have to be separate in order to process through the secondary
    #SavGol filter
    _coords_x = []
    _coords_y = []
    _coords_z = []
    _slice_ts = []
    _num_results = 0
    
    def enqueue(self, slice_ts:float, coord_xyz:Tuple[float])->Tuple[float,float,float,float]:
        '''
        Returns: timestamp, X, Y, Z
        '''
        rval = []
        if ((math.isnan(coord_xyz[0])) or (math.isnan(coord_xyz[1])) or (math.isnan(coord_xyz[2]))):
#             print('Error: nan')
            #TODO
            return rval
        
        self._coords_x.append(coord_xyz[0])
        self._coords_y.append(coord_xyz[1])
        self._coords_z.append(coord_xyz[2])
        self._slice_ts.append(slice_ts)
        self._num_results += 1
        if (self._is_time_to_filter()):
            rval = self._filter_results()
        return rval
    
    def flush_results(self):
        '''
        Flush and write all remaining results.
        '''
        write_num = self._num_results
        self._get_results(write_num)
        return
    
    def _is_time_to_filter(self):
        '''
        Determines if enough items are in the queue to filter.
        '''
        if (self._num_results > self._filter_buffer_size):
            return True
        return False
    
    def _filter_results(self):
        '''
        Secondary filter pass execution.
        '''
        self._coords_x = self._filter_dimension(self._coords_x)
        self._coords_y = self._filter_dimension(self._coords_y)
        self._coords_z = self._filter_dimension(self._coords_z)
        
        #write out half of the filter set
#         write_num = int(self._num_results / 2)
#         return self._get_results(write_num)
        return self._get_results(1)
    
    def _get_results(self, write_num:int):
        '''
        Retrieves ready results for return.
        '''
        rslts = []
        for i in range(0, write_num):
            rslts.append([self._slice_ts[i], self._coords_x[i], self._coords_y[i], self._coords_z[i]])
            #Pop items off the arrays
            self._coords_x.pop(0)
            self._coords_y.pop(0)
            self._coords_z.pop(0)
            self._slice_ts.pop(0)
            self._num_results -= 1
        return rslts
    
    def _filter_dimension(self, coords)->Tuple:
        '''
        Secondary filter pass for a single array.
        
        scipi Parameters:    
            x : array_like
                The data to be filtered. If x is not a single or double precision floating point array, it will be converted to type numpy.float64 before filtering.
                window_length : int
                The length of the filter window (i.e. the number of coefficients). window_length must be a positive odd integer.
            polyorder : int
                The order of the polynomial used to fit the samples. polyorder must be less than window_length.
            deriv : int, optional
                The order of the derivative to compute. This must be a nonnegative integer. The default is 0, which means to filter the data without differentiating.
                delta : float, optional
                The spacing of the samples to which the filter will be applied. This is only used if deriv > 0. Default is 1.0.
            axis : int, optional
                The axis of the array x along which the filter is to be applied. Default is -1.
            mode : str, optional
                Must be ‘mirror’, ‘constant’, ‘nearest’, ‘wrap’ or ‘interp’. This determines the type of extension to use for the padded signal to which the filter is applied. When mode is ‘constant’, the padding value is given by cval. See the Notes for more details on ‘mirror’, ‘constant’, ‘wrap’, and ‘nearest’. When the ‘interp’ mode is selected (the default), no extension is used. Instead, a degree polyorder polynomial is fit to the last window_length values of the edges, and this polynomial is used to evaluate the last window_length // 2 output values.
            cval : scalar, optional
                Value to fill past the edges of the input if mode is ‘constant’. Default is 0.0.
            Returns:    
                y : ndarray, same shape as x the filtered data.
        '''
        filt_coords = scipy.signal.savgol_filter(x=coords, window_length=self._filter_window_size, \
            polyorder=self.FILTER_POLYORDER, deriv=self.FILTER_DERIVATIVE, \
            delta=self.FILTER_DERIVATIVE_DELTA)
        return filt_coords.tolist()

    def __init__(self, params):
        '''
        Constructor
        '''
        self._params = params
        self._filter_buffer_size = self._params.SECONDARY_FILTER_BUFFER
        self._filter_window_size = self._params.SECONDARY_FILTER_WINDOW
        return
        
        