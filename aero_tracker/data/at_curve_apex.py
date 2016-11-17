'''
Created on Nov 8, 2016

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
import numpy as np
import matplotlib.pyplot as plt
from scipy import interpolate

from aptdaemon.config import log

class AT_CurveApex(object):
    '''
    Determines the dimensional apex of a curve.  This object requires that curve
    data be passed in with:
    
    X = time series
    Y = Curve values 
    '''
    INTERPOLATE_RESOLUTION = 0.01
    INTERPOLATE_RANGE = 1.0 # Minimum value to interpolate
    
    MAX_INTERPOLATION = 0 #curve is negative to positive to negative (horse shoe)
    MIN_INTERPOLATION = 1 #curve is positive to negative to positive (U shape)
    
    _interpolate_resolution = 0.1
    
    def graph_apex(self, x:typing.List, y:typing.List, curve_type=0)->float:
        '''
        Finds and graphs the apex of a 2 dimensional curve.  Also, returns the apex point
        as a result.
        '''
        rval = None
        
        intpol_y = interpolate.splrep(x=x, y=y, s=0)
        det_x = np.arange(x[0],x[len(x) - 1], self._interpolate_resolution)
        det_y = interpolate.splev(det_x, intpol_y, der=0)
        npy = np.array(det_y)
        if (curve_type == self.MAX_INTERPOLATION):
            indx = npy.argmax()  #Index of minimum value
        else:
            indx = npy.argmin()
        rval = det_y[indx]
        
        plt.figure()
        plt.plot(x, y, 'x', det_x, det_y, det_x, det_y, x, y, 'b')
        plt.title('Spline interpolation')
        plt.show()
        
        return rval
    
    def find_apex(self, x:typing.List, y:typing.List, curve_type=0):
        '''
        Takes incoming X and Y dimensions and find the curve apex using b-spline interpolation.
        
        Note: This uses the whole X and Y array.
        '''
        rval = None
        
        intpol_y = interpolate.splrep(x=x, y=y, s=0)
        det_x = np.arange(x[0],x[len(x) - 1], self.INTERPOLATE_RESOLUTION)
        det_y = interpolate.splev(det_x, intpol_y, der=0)
        npy = np.array(det_y)
        if (curve_type == self.MAX_INTERPOLATION):
            indx = npy.argmax()  #Index of minimum value
        else:
            indx = npy.argmin()
        rval = det_y[indx]
                
        return rval

    def __init__(self, interpolate_resolution):
        '''
        Constructor
        '''
        self._interpolate_resolution = interpolate_resolution
        return
    
    
#Tester
# obj = AT_CurveApex(interpolate_resolution=0.01, log=None)
# #6 data point test set, all equal time
# test_x = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6]
# test_y = [0.4,1.2,2.1,2.2,1.1,0.2]
# apex = obj.graph_apex(x=test_x, y=test_y)
# print('Apex: ' + str(apex))



# obj = AT_CurveApex(interpolate_resolution=0.01, log=None)
# #6 data point test set, all equal time
# test_x = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8]
# test_y = [-4,-2,0.4,1.2,2.2,1.1,0.2,-3]
# apex = obj.graph_apex(x=test_x, y=test_y)
# print('Apex: ' + str(apex))


# obj = AT_CurveApex(interpolate_resolution=0.01, log=None)
# #6 data point test set, all equal time
# test_x = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8]
# test_y = [-14,-2,0.4,1.2,6.2,10.1,2.2,-13]
# apex = obj.graph_apex(x=test_x, y=test_y)
# print('Apex: ' + str(apex))

