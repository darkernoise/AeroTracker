'''
Created on Sep 20, 2016

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
import time
from aero_tracker.params.at_result_listener_params import AT_ResultListenerParams
from aero_tracker.data.at_curve_apex import AT_CurveApex

class LapDataSort(object):
    '''
    Sorts result data into laps.
    
    For purpose of tracking, this divides the data into 4 X,Y quadrants:
    
    2 | 1
    -----
    3 | 4
    
    Also, a buffer of data points is used to track if the vehicle is flying towards or 
    away from the pole.  Specifically, the Y axis is tracked over a short buffer to 
    detect a change in direction.  That change in direction is considered the apex
    of the turn.
    '''
    
    DIRECTION_UNKNOWN = 0
    DIRECTION_TOWARDS = 1
    DIRECTION_AWAY = 2
    MIN_Y_BUFFER_SIZE = 3
    Y_BUFFER_SIZE = 10
    DIRECTION_CHANGE_CNT = 5
    MAX_BUFFER_SIZE = 1000  #Max size any buffer can reach before truncation
    
    _x = []
    _y = []
    _z = []
    _params = AT_ResultListenerParams
    _last_quadrant = 0
    
    _y_buffer = [] #holds the predominate values during a single direction
    _tmp_y_buffer = [] #holds values during a change in direction
    
    _current_direction = 0
    _data_buffer = []
    _last_apex = None
    _num_cuts = 0
    _lap_number = 0
    _time_last_lap_data = None
    _curve_apex_calc = AT_CurveApex
    
    @property
    def x(self)->typing.List:
        return self._x
    
    @property
    def y(self)->typing.List:
        return self._y
    
    @property
    def z(self)->typing.List:
        return self._z
    
    @property
    def time_last_lap_data(self):
        return self._time_last_lap_data
    
    @property
    def num_cuts(self):
        return self._num_cuts
    
    @property
    def lap_number(self):
        '''
        Number of laps around the pole completed.  A lap is not 
        counted at the pole until the apex is reached.
        '''
        return self._lap_number
    
    @property
    def last_apex(self):
        '''
        Returns the Y value from the last turn apex.
        '''
        return self._last_apex
    
    @property
    def quadrant(self):
        return self._last_quadrant
    
    def append_data(self, dat):
        '''
        Append a data list in the form:
        
        [timestamp, X, Y, Z]
        
        returns if a new graph should be started
        '''
        self._time_last_lap_data = time.time()
        cur_quad = self.curr_quadrant(X=dat[1], Y=dat[2])
        new_graph = self._add_new_y(new_y=dat[2], dat=dat)
        self._last_quadrant = cur_quad
        if (new_graph):
            self._x = []
            self._y = []
            self._z = []
            
        self._x.append(dat[1])
        self._y.append(dat[2])
        self._z.append(dat[3])
            
        if (len(self._x) > self.MAX_BUFFER_SIZE):
            self._x.pop(0)
            self._y.pop(0)
            self._z.pop(0)
        return new_graph
    
    def curr_quadrant(self, X, Y):
        '''
        Determines the current quadrant of the X, Y data values
        '''
        if ((X >= 0) and (Y >= 0)):
            return 1
        elif ((X < 0) and (Y >= 0)):
            return 2
        elif ((X < 0) and (Y < 0)):
            return 3
        return 4
    
    def check_lap_timeout(self):
        '''
        Checks time since last data against current time to see if a 
        lap must have already elapsed.
        '''
        if (self._time_last_lap_data == None):
            return False
        
        time_passed = time.time() - self._time_last_lap_data
        if (time_passed > self._params.lap_timeout_secs):
            return True
        
        return False
    
    def check_race_timeout(self):
        '''
        Checks time since last data against current time to see if a 
        race must be over.
        '''
        if (self._time_last_lap_data == None):
            return False
        
        time_passed = time.time() - self._time_last_lap_data
        if (time_passed > self._params.race_timeout_secs):
            self._time_last_lap_data = None
            return True
        
        return False

    def __init__(self, params):
        '''
        Constructor
        '''
        self._params = params
        self._curve_apex_calc = AT_CurveApex(interpolate_resolution=AT_CurveApex.INTERPOLATE_RESOLUTION)
        return
    
    def _add_new_y_smart(self, new_y, dat):
        
        return
    
    def _add_new_y(self, new_y, dat):
        new_graph = False
        
        #first records
        if (len(self._y_buffer) == 0):
            new_graph = True
        if (len(self._y_buffer) < self.MIN_Y_BUFFER_SIZE):
            self._y_buffer.append(new_y)
        
        first_y = self._y_buffer[0]
        last_y = self._y_buffer[len(self._y_buffer) - 1]
        temp_set = False
        
        #Set values based on direction
        if ((self._current_direction == self.DIRECTION_UNKNOWN) and 
            (len(self._y_buffer) >= self.MIN_Y_BUFFER_SIZE)):
            if (last_y <  first_y):
                self._current_direction = self.DIRECTION_TOWARDS
            else:
                self._current_direction = self.DIRECTION_AWAY
        elif (self._current_direction == self.DIRECTION_TOWARDS):
            if (new_y < last_y):
                self._y_buffer.append(new_y)
                self._tmp_y_buffer = []
            else:
                self._tmp_y_buffer.append(new_y)
                temp_set = True
        elif (self._current_direction == self.DIRECTION_AWAY):
            if (new_y > last_y):
                self._y_buffer.append(new_y)
                self._tmp_y_buffer = []
            else:
                self._tmp_y_buffer.append(new_y)
                temp_set = True
        
        #Process temp changes
        if (temp_set):
            self._data_buffer.append(dat)
             
            if (len(self._tmp_y_buffer) > self.DIRECTION_CHANGE_CNT):
                #Test amount of change
                chng = abs(new_y - self._tmp_y_buffer[0])
                if (chng >= self._params.min_lap_y_distance):
                    #Direction has changed
                    self._last_apex = self._data_buffer[0]
                    self._lap_number += 1
                    self._y_buffer = self._tmp_y_buffer
                    self._tmp_y_buffer = []
                    
                    #Prodcess the direction change
                    if (self._current_direction == self.DIRECTION_TOWARDS):
                        self._current_direction = self.DIRECTION_AWAY
                    else:
                        self._current_direction = self.DIRECTION_TOWARDS
                        new_graph = True
            if (len(self._tmp_y_buffer) > self.MAX_BUFFER_SIZE):
                self._tmp_y_buffer.pop(0)

        #Keep the buffer to its max size
        if (len(self._y_buffer) >= self.Y_BUFFER_SIZE):
            self._y_buffer.pop(0)
        
        return new_graph
    
    
    
    
        