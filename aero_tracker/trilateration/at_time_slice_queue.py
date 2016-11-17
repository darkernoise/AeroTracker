'''
Created on Oct 20, 2016

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
import typing
import multiprocessing as mp
from aero_tracker.trilateration.time_slice import TimeSlice
from aero_tracker.network.at_sensor_data_packet import AT_SensorDataPacket
from aero_tracker.trilateration.raw_data.ts_queue_item import TSQueueItem
from aero_tracker.trilateration.raw_data.ts_queue_item import TSQueueItemSensor
from aero_tracker.params.at_sensor_cluster_params import ATSensorClusterParams
from aero_tracker.log.at_logging import AT_Logging

class AT_TimeSliceQueueItem(object):
    '''
    This is the storage format for data packets while in the queue.
    '''
    time_slice = TimeSlice
    data_pkt = AT_SensorDataPacket
    
    def __lt__(self, other):
        return self.time_slice < other.time_slice
    
    def __init__(self, time_slice, data_pkt):
        self.time_slice = time_slice
        self.data_pkt = data_pkt
        return

class AT_TimeSliceQueue(object):
    '''
    Multiprocessing safe time slice data organization queue.
    '''
    MAX_QUEUE_SIZE = 1010
    MIN_ITEM_SIZE = 4 #This is the number of sensors needed to Trilaterate
    OVERFLOW_LOGGING = 100
    QUEUE_INACTIVE_TIME = 30 #seconds
    MIN_BUFFER_SIZE = 300
    
    _buffer_size = 20 #set via param: TIME_SLICE_QUEUE_BUFFER
    _force_pop_size = 10
    _time_slices_per_sec = 40 #Set via param: time_slices_per_sec
    _lock = mp.Lock()
    _sensor_queues = None
    _params = ATSensorClusterParams
    _buffer = []
    _last_enqueue_time = time.time()
    _overflow_cnt = 0
    _log = AT_Logging
    
    @property
    def get_queue(self):
        return self
    
    @property
    def queue_inactive(self):
        time_elapsed = time.time() - self._last_enqueue_time
        if (time_elapsed >= self.QUEUE_INACTIVE_TIME):
            return True
        return False
    
    def enqueue(self, sensor_datpkt:AT_SensorDataPacket):
        '''
        Adds a data packet to the queue of the specific sensor.  Each sensor's 
        queue is stored in memory separately for speed. 
        '''
        self._last_enqueue_time = time.time()
        time_slice = TimeSlice(time_val=sensor_datpkt.timestamp, sec_div=self._time_slices_per_sec)
        delay_required = False
        
        buff_len = len(self._buffer)
        
        q_itm_snsr = TSQueueItemSensor(sensor_id=sensor_datpkt.sensor_id, data_pkt=sensor_datpkt)
        q_itm = TSQueueItem(tm_slc=time_slice, q_itm_snsr=q_itm_snsr)
        if (buff_len == 0):
            self._buffer.append(q_itm)
        else:
            try:
                indx = self._get_buffer_index(q_itm=q_itm, test_reverse=True, except_on_missing=True)
                #If we made it here, the value exits
                q_itm = self._buffer[indx]
                snsr_found = False
                for snsr in q_itm.sensors:
                    if (snsr.sensor_id == sensor_datpkt.sensor_id):
                        #sensor already exists
                        snsr.data_pkts.append(sensor_datpkt)
                        snsr_found = True
                        exit
                if (not snsr_found):
                    q_itm_snsr = TSQueueItemSensor(sensor_id=sensor_datpkt.sensor_id, data_pkt=sensor_datpkt)
                    q_itm.sensors.append(q_itm_snsr)
#                     q_itm.sort_by_sensor_id()
                
            except:
                #Value does not exist
                self._buffer.append(q_itm)
                self._buffer.sort()
            
        #check for overflow
        if (buff_len > self.MAX_QUEUE_SIZE):
            self._buffer.pop(0)
            self._overflow_cnt += 1
            delay_required = True
        elif(buff_len > self._buffer_size):
            delay_required = True
            
            
        if (self._overflow_cnt >= self.OVERFLOW_LOGGING):
            self._log.log2(msg1='Buffer overflow at time_slice_queue:', msg2=str(self._overflow_cnt) + ' items', caller=self, msgty=AT_Logging.MSG_TYPE_WARNING)
            self._overflow_cnt = 0
        
        if (delay_required):
            #impose a delay to slow this process down and to let others catch up
            time.sleep(0.01)
    
        return
    
    def pop(self)->TSQueueItem:
#         rval = None
        rval = self._get_pop_value()
        return rval
    
    def _get_pop_value(self, seed_value=None, pop_count=0)->TSQueueItem:
        rval = None
        
        buff_len = len(self._buffer)
#         if (buff_len <= self.MIN_BUFFER_SIZE):
        if (buff_len <= self._params.time_slice_queue_buffer_size):
            return None
        
        new_val = None
        force_pop = False
        if (buff_len > pop_count):
            new_val = self._buffer[pop_count]
        
#       Combine seed value with new value
#         if ((seed_value != None) and (new_val != None)):
#             if (abs(new_val.sort_key - seed_value.sort_key) < self._params.MAX_TIME_SLICE_DIFF):
#                 #The two values are close enough that they will be added together
#                 new_val = TSQueueItem.merge_queue_items(q_old=seed_value, q_new=new_val)
#                 
# #             elif(buff_len > self._force_pop_size):
#             elif(buff_len > self._params.time_slice_queue_buffer_size):
#                 #sort key values are too far apart, pop off the items used so far
#                 force_pop = True
        
        if (new_val != None):
            if ((len(new_val.sensors) >= self.MIN_ITEM_SIZE) or
                (buff_len >= self._force_pop_size) or
                (force_pop)):
                rval = new_val
                for i in range(0, pop_count + 1):
                    self._buffer.pop(0)
#             else:
#                 #try to combine the shorted item with the next item
#                 rval = self._get_pop_value(seed_value=new_val, pop_count=pop_count+1)
        
        rval = self._average_sensor_vals(queue_item=rval)
        return rval
    
    def _average_sensor_vals(self, queue_item:TSQueueItem):
        '''
        If a sensor contains more than 1 data packet, averages the 
        data packets and removes all but the result data packet.
        '''
        snsr = TSQueueItemSensor
        for snsr in queue_item.sensors:
            if (len(snsr.data_pkts) > 1):
                avg_ttl = 0.0
                num_pkts = len(snsr.data_pkts)
#                 dpkt = AT_SensorDataPacket
                
                for i in range(0, num_pkts - 1):
                    dpkt = snsr.data_pkts.pop(0)
                    avg_ttl = avg_ttl + dpkt.filter_dist
                avgval = avg_ttl / num_pkts
                snsr.data_pkts[0].filter_dist = avgval
        
        return queue_item
    
    def _get_buffer_index(self, q_itm:TSQueueItem, test_reverse=True, except_on_missing=True):
        rval = -1
        
        if (test_reverse):
            for i in range(len(self._buffer)-1,-1,-1):
                tst_q_itm = self._buffer[i]
                if (q_itm.sort_key == tst_q_itm.sort_key):
                    return i
                elif(q_itm.sort_key > tst_q_itm.sort_key):
                    #Not found in queue
                    if (except_on_missing):
                        raise Exception('Value not found')
                    return rval
        else: #forward
            for i in range(0, len(self._buffer)):
                tst_q_itm = self._buffer[i]
                if (q_itm.sort_key == tst_q_itm.sort_key):
                    return i
        
        if ((except_on_missing) and (rval < 0)):
            raise Exception('Value not found')
        
        return rval
        

    def __init__(self, log:AT_Logging, params:ATSensorClusterParams):
        '''
        Constructor
        '''
        self._params = params
        self._log = log
        self._time_slices_per_sec = self._params.time_slices_per_sec
        self._force_pop_size = int(self._time_slices_per_sec / 2)
        print('Time slices per/sec: ' + str(self._time_slices_per_sec))
        self._buffer = []
        self._buffer_size = self._params.time_slice_queue_buffer_size
        if (self._buffer_size > self.MAX_QUEUE_SIZE):
            self._buffer_size = self.MAX_QUEUE_SIZE - 10
        return
    
    
#Tester
# import time
# params = AT_DataProcServerParams('/etc/popt/aero_tracker/at_data_proc_server.conf')
# obj = AT_TimeSliceQueue(params=params)        
# cluster_id = 'NP'
# target_id = 'target1234'
#    
# pkt_a = AT_SensorDataPacket(cluster_id=cluster_id, sensor_id=cluster_id + '_A', target_id=target_id, filter_dist=12.6, raw_dist=13.2, rssi=-34, timestamp=time.time() - 0.1)
# obj.enqueue(pkt_a)
# pkt_a = AT_SensorDataPacket(cluster_id=cluster_id, sensor_id=cluster_id + '_A', target_id=target_id, filter_dist=12.6, raw_dist=13.2, rssi=-34, timestamp=time.time() - 0.1)
# obj.enqueue(pkt_a)
#  
# pkt_base = AT_SensorDataPacket(cluster_id=cluster_id, sensor_id=cluster_id + '_BASE', target_id=target_id, filter_dist=12.6, raw_dist=13.2, rssi=-34, timestamp=time.time())
# obj.enqueue(pkt_base)
# pkt_b = AT_SensorDataPacket(cluster_id=cluster_id, sensor_id=cluster_id + '_B', target_id=target_id, filter_dist=12.6, raw_dist=13.2, rssi=-34, timestamp=time.time())
# obj.enqueue(pkt_b)
# pkt_c = AT_SensorDataPacket(cluster_id=cluster_id, sensor_id=cluster_id + '_C', target_id=target_id, filter_dist=12.6, raw_dist=13.2, rssi=-34, timestamp=time.time() + 0.2)
# obj.enqueue(pkt_c)
# pkt_d = AT_SensorDataPacket(cluster_id=cluster_id, sensor_id=cluster_id + '_D', target_id=target_id, filter_dist=12.6, raw_dist=13.2, rssi=-34, timestamp=time.time() + 0.1)
# obj.enqueue(pkt_d)
# pkt_a = AT_SensorDataPacket(cluster_id=cluster_id, sensor_id=cluster_id + '_A', target_id=target_id, filter_dist=12.6, raw_dist=13.2, rssi=-34, timestamp=time.time() - 0.1)
# obj.enqueue(pkt_a)
#    
# val = obj.pop()
# print(val)

        