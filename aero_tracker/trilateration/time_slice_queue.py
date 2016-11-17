'''
Created on Aug 19, 2016

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
import time
import threading
from aero_tracker.trilateration.time_slice import TimeSlice
from aero_tracker.network.at_sensor_data_packet import AT_SensorDataPacket
from aero_tracker.trilateration.raw_data.ts_queue_item import *
from aero_tracker.params.at_data_proc_server_params import AT_DataProcServerParams
import multiprocessing as mp


class TimeSliceQueue(object):
    '''
    Sorted queue where asychronously arriving sensor data is sorted and grouped
    for trilateration.  First, incoming data is categorized into a time slice of
    a second.  Then, for the given time slice, data from each sensor is grouped
    into an array by sensor.
    '''
    
    MAX_BUFFER_SIZE = 300
    MIN_BUFFER_SIZE = 5
    MIN_ITEM_SIZE = 4
    
    _buffer_size = 20 #set via param: TIME_SLICE_QUEUE_BUFFER
    
    _data = None #List of TSQueueItem
    _lock = None
    _params = None
#     _process_buffer_size = 20
    
    @property
    def data(self):
        return self._data
    
    def get_size(self):
        rval = 0
        self._lock.acquire()
        rval = len(self._data)
        self._lock.release()
        return rval
    
    def get_process_size(self):
        '''
        Number of records to cache and sort before processing.
        '''
        return self._buffer_size
    
    def get_time_slice_queue(self):
        '''
        Called to get a proxy object.
        '''
        return self
    
    def enqueue(self, sensor_datpkt:AT_SensorDataPacket, triangulations_psec):
        self._lock.acquire()
        ts = TimeSlice(time_val=sensor_datpkt.timestamp, sec_div=triangulations_psec)
        
        self._lock.release()
        return
    
    def enqueue_old(self, sensor_datpkt:AT_SensorDataPacket, triangulations_psec):
        '''
        Queue is sorted first by times slice, then by sensor.
        
        Queue Item contains:
            time_slice = None
            sensors = [] #array of TSQueueItemSensor
            
        Queue Item Sensor contains:
            sensor_id = ""
            data_pkts = []
        '''
        self._lock.acquire()
        ts = TimeSlice(time_val=sensor_datpkt.timestamp, sec_div=triangulations_psec)
        indx = self.pos_of_time_slice(sort_key=ts.sort_key)
        if (indx < 0):
            #does not exist yet
            q_itm_snsr = TSQueueItemSensor(sensor_id=sensor_datpkt.sensor_id, data_pkt=sensor_datpkt)
            q_itm = TSQueueItem(tm_slc=ts, q_itm_snsr=q_itm_snsr)
            self.data.append(q_itm)
            self.data.sort(key=lambda x: x.sort_key, reverse=False)
        else:
            #append value to existing item
            q_itm = self.data[indx] #type TSQueueItem
            snsr_indx = self.pos_of_sensor_in_slice(ts_itm=q_itm, sensor_id=sensor_datpkt.sensor_id)
            if (snsr_indx < 0):
                q_tim_snsr = TSQueueItemSensor(sensor_id=sensor_datpkt.sensor_id, data_pkt=sensor_datpkt)
                q_itm.sensors.append(q_tim_snsr)
#                 print('Append sensor to existing time slice: ', sensor_datpkt.sensor_id)
            else:
                q_itm.sensors[snsr_indx].data_pkts.append(sensor_datpkt)
            self.data[indx] = q_itm #Value is not mutable
        
        #Check for overflow
        if (len(self._data) > self.MAX_BUFFER_SIZE):
          self.data.pop(0)
            
        self._lock.release()
        return
    
    def pop(self, size_min=False):
        '''
        pop the next item off the queue.  
        
        size_min param indicates to only pop the item if the minimum number of items is present.
        
        Item is in format:
        
        [TimeSlice, [AT_SensorDataPacket]]
        
        In short, there is a single time slice object and an array of sensor data packets that go to it.
        '''
        self._lock.acquire()
        
        itm = None
        if (len(self._data) > 0):
            if ((size_min) and (len(self._data) > self.MIN_BUFFER_SIZE)):
                tst_slice = self.data[0]
                if (len(tst_slice.sensors) > self.MIN_ITEM_SIZE):
                    itm = self.data.pop(0)
            else:
                #pop the item regardless of size
                itm = self.data.pop(0)
                
      
        self._lock.release()
        return itm

    def pos_of_sensor_in_slice(self, ts_itm:TSQueueItemSensor, sensor_id: str):
        '''
        Find the position of a sensor within a time slice.
        '''
        for i in range(len(ts_itm.sensors)-1,-1,-1):
            snsr = ts_itm.sensors[i]
            if (snsr.sensor_id == sensor_id):
                return i
            
        return -1
    
    def pos_of_time_slice(self, sort_key: float):
        '''
        Find the position of a time slice in the array
        '''
        #start from the top, not the bottom
        for i in range(len(self.data)-1,-1,-1):
            tm_slc = self.data[i].time_slice
            if (tm_slc.sort_key == sort_key):
                return i
        return -1
    
    def __init__(self, params:AT_DataProcServerParams):
        self._data = []
        self._params = params
#         self._lock = mp.RLock()
        self._lock = mp.Lock()
        self._buffer_size = self._params.TIME_SLICE_QUEUE_BUFFER
        return
    
    
#Tester
# tm = time.time()
# dpk1 = AT_SensorDataPacket(cluster_id='NP', sensor_id='NP_BASE', \
#     target_id='ff484da4d57869c60b071600b0000000', filter_dist=2.3, raw_dist=2.2,rssi=26, timestamp=tm)
# dpk2 = AT_SensorDataPacket(cluster_id='NP', sensor_id='NP_A', \
#     target_id='ff484da4d57869c60b071600b0000000', filter_dist=19.3, raw_dist=19.2,rssi=76, timestamp=tm)
# dpk2_2 = AT_SensorDataPacket(cluster_id='NP', sensor_id='NP_A', \
#     target_id='ff484da4d57869c60b071600b0000000', filter_dist=20.3, raw_dist=19.2,rssi=54, timestamp=tm)
# dpk3 = AT_SensorDataPacket(cluster_id='NP', sensor_id='NP_B', \
#     target_id='ff484da4d57869c60b071600b0000000', filter_dist=25.3, raw_dist=29.2,rssi=37, timestamp=tm)
# dpk4 = AT_SensorDataPacket(cluster_id='NP', sensor_id='NP_C', \
#     target_id='ff484da4d57869c60b071600b0000000', filter_dist=12.3, raw_dist=12.2,rssi=62, timestamp=tm)
# 
# q = TimeSliceQueue()
# q.enqueue(dpk1, 100)
# q.enqueue(dpk2, 100)
# q.enqueue(dpk2_2, 100)
# q.enqueue(dpk3, 100)
# q.enqueue(dpk4, 100)
# 
# while (q.size() > 0):
#     itm = q.pop()
#     print(itm)
#         