'''
Created on Jun 3, 2016

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

import datetime
import time

class TimeSlice(object):
    '''
    Time slicer for grouping trangulation coordinates.
    
    Note: All times processed in UTC
    '''
    
    MS_IN_SECOND = 1000000 #Decimal digits of a single second in miliseconds
    
    _second_divisor = 10 
    _second_slice_number = 1
    _time_val = float(0)
    _start_time_set = False
    _start_time = time.time()
    _end_time_set = False
    _end_time = time.time()
    _sort_key = 0.0
    
    @property
    def sort_key(self):
        return self._sort_key
    
    
    @staticmethod
    def calc_second_slice_num(tm, sec_div):
        '''
        Calculates which time slice the current time milliseconds fall into.
        '''
        divisor = 1 / sec_div
        ms = tm - int(tm)
        rval = int(ms / divisor)
        return rval
    
    @staticmethod
    def get_next_time_slice(tm_slice, params):
        tm = tm_slice.get_time_val()
        ms = tm_slice.get_slice_miliseconds()
        slice_num = tm_slice.get_slice_number()
        if (slice_num == tm_slice.get_second_divisor()):
            slice_num = 1
        else:
            slice_num += 1
            
        
        if (slice_num == tm_slice.get_second_divisor()):
            tm += 1.0
            ms = 0
            slice_num = 0
        else:
            tm += ms
        
#         print("Old Slice: ", tm_slice.get_slice_number(), " New Slice: ", slice_num, ", ms: ", ms)
        
        new_tm_slice = TimeSlice(time_val=tm, \
            second_divisor=tm_slice.get_second_divisor(), \
            second_slice_number=slice_num, \
            params=params)
        return new_tm_slice
    
    def get_slice_number(self):
        return self._second_slice_number
    
    def get_time_val(self):
        return self._time_val
    
    def get_second_divisor(self):
        return self._second_divisor
    
    def get_slice_miliseconds(self):
        return ((TimeSlice.SECOND_IN_MS / self.get_second_divisor()) / TimeSlice.SECOND_IN_MS) / 10
    
    def start_time(self):
        if (not self._start_time_set):
            dt = datetime.datetime.fromtimestamp(self._time_val)
            div = self.SECOND_IN_MS / self._second_divisor
            ms = div * self._second_slice_number
            self._start_time = datetime.datetime(year=dt.year,month=dt.month,day=dt.day, \
                hour=dt.hour,minute=dt.minute,second=dt.second, \
                microsecond=int(ms)).timestamp()
            self._start_time_set = True
        return self._start_time
    
    def end_time(self):
        if (not self._end_time_set):
            dt = datetime.datetime.fromtimestamp(self._time_val)
            div = self.SECOND_IN_MS / self._second_divisor
#             ms = ((div * self._second_slice_number) + (div - 1))
            ms = (div * self._second_slice_number) + (div - 1)
#             print(ms)
            self._end_time = datetime.datetime(year=dt.year,month=dt.month,day=dt.day, \
                hour=dt.hour,minute=dt.minute,second=dt.second, \
                microsecond=int(ms)).timestamp()
            self._end_time_set = True
        return self._end_time
    
    def is_time_in_time_slice(self, tm):
        if ((tm >= self.start_time()) and (tm <= self.end_time())):
            return True
        return False
    
    def is_time_greater_end_time(self, tm):
        if (tm > self.end_time()):
            return True
        return False
    
    def is_time_less_start_time(self, tm):
        if (tm < self.start_time()):
            return True
        return False

    def __init__(self, time_val, sec_div):
        '''
        Constructor for the Time Slice class.
        
        time_val = time value in microseconds (float form)
        second_divisor = number of slice divisions per second
        second_slice_number = 0 indexed count up to the second_divisor (-1)
        '''
        self._second_divisor = sec_div
        self._second_slice_number = TimeSlice.calc_second_slice_num(time_val,sec_div)
        self._time_val = time_val
        self._sort_key = int(time_val) + (self._second_slice_number * (1 / sec_div))
        
    def __lt__(self, other):
         return self.sort_key < other.sort_key
        
'''
Tester
'''
# dt = time.time()
# dt_obj = datetime.datetime.fromtimestamp(dt)
# # dt_obj.year
# obj = TimeSlice(time_val=dt, second_divisor=100, second_slice_number=1, params=None)
# print("Start: ", obj.start_time().strftime('%Y-%m-%d %H:%M:%S.%f'))
# print("End  : ", obj.end_time().strftime('%Y-%m-%d %H:%M:%S.%f'))
# for i in range(1, 105):
#     obj= TimeSlice.get_next_time_slice(obj, params=None)
#     print("Start: ", obj.start_time().strftime('%Y-%m-%d %H:%M:%S.%f'))
#     print("End  : ", obj.end_time().strftime('%Y-%m-%d %H:%M:%S.%f'))


'''
Tester 2
'''
# print('\n')
# dt = time.time()
# dt_obj = datetime.datetime.fromtimestamp(dt)
# print('Time:', dt_obj)
# sec_slice = TimeSlice.calc_second_slice_num(tm=dt, sec_div=20)
# print('Second Slice:',sec_slice)
# obj = TimeSlice(time_val=dt,sec_div=20)
# print('Sort Key', obj.sort_key)
# #


         