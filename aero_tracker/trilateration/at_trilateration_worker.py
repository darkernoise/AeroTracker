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
import typing
import numpy as np
from aero_tracker.common.at_process_base import AT_ProcessBase
from aero_tracker.network.at_pipe_pool import AT_PipePool
from aero_tracker.network.at_protocol import AT_Protocol
from aero_tracker.data.sphere_coordinates import SphereCoordinates
from aero_tracker.data.at_data_rate import AT_DataRate

# from aero_tracker.trilateration.raw_data.ts_queue_item import *

from aero_tracker.sensor.sensor_device import SensorDevice
from aero_tracker.trilateration.at_trilateration import AT_Trilateration
from aero_tracker.filter.savgol_filter_queue import SavGolFilterQueue
from aero_tracker.log.at_logging import AT_Logging
from aero_tracker.network.at_listener_multicast import AT_ListenerMulticast
from builtins import str

class AT_ConnectionID(object):
    
    target_id = None
    cluster_id = None
    connection_time = None
    
    def __init__(self, target_id:str, cluster_id):
        self.target_id = target_id
        self.cluster_id = cluster_id
        self.connection_time = time.time()
        return

class AT_TrilaterationWorker(AT_ProcessBase):
    '''
    Process to receive and manage the trilateration of data.  Each trilateration worker 
    will service only 1 target. Thus, all data received and processed here is for the 
    same target.
    
    Though, a data processor can be recycled in which case the target is changed.
    
    '''
    FILTER_RSLT_STAT_CNT = 1000
    MAX_QUEUE_SIZE=200
    LOG_FILE_BASE = '/var/log/aerotracker/at_target_'
    INCOMPLETE_STATUS = 30
    
    _sensors = typing.List # [SensorDevice]
    _dir_store = None
    _pipe_pool = AT_PipePool
    _listeners = typing.List
    _filter = None #SavGolFilterQueue
    _incomplete_cnt = 0
    _listener_multicast = None
    _target_id = None
    _first_packet_sent = False
    _last_time_slice_sort_key = 0.0
    _connection_ids = typing.List #AT_ConnectionID
    _rate_filtered = AT_DataRate
    _rate_prefiltered = AT_DataRate

    
    
    @property
    def log_file(self):
        rval = self.LOG_FILE_BASE + 'none'
        if (self._target_id != None):
            rval = self.LOG_FILE_BASE + self._target_id
        return rval
    
    @property
    def queue(self):
        '''
        Trilateration queue is filled with items received from the sensor clusters.  The data 
        is pre-sorted by time slice and organized by target.
        '''
        return self._trilat_q

    
    def run_clycle(self):
        '''
        Executes within the while is_running loop.
        '''
        no_data = True
        for i in range(0, self._pipe_pool.num_pipes):
            conn = self._pipe_pool.parent_conns[i]
            if (conn.poll()):
                data_packet_bytes = conn.recv()
                if (data_packet_bytes != None):
                    no_data = False
                    #determine if command or data
                    if (data_packet_bytes[0] == AT_Protocol.COMMAND_ID):
                        cmd_id, target_id, cluster_id = AT_Protocol.bytes_to_sensor_cluster_id(data_bytes=data_packet_bytes)
                        con_id = AT_ConnectionID(target_id=target_id, cluster_id=cluster_id)
                        self._connection_ids[i]  = con_id
                        
                        #setup rate counters
                        lbl_prefix = cluster_id + '-' + target_id + ' : '
                        self._rate_filtered = AT_DataRate(log=self.log, report_label=lbl_prefix + 'Filtered rslts', report_cnt=self.FILTER_RSLT_STAT_CNT)
                        self._rate_prefiltered = AT_DataRate(log=self.log, report_label=lbl_prefix + 'Pre-filtered rslts', report_cnt=self.FILTER_RSLT_STAT_CNT)
                        
                        #set the target id to check for recycling
                        if ((target_id != None) and (self._target_id != target_id)):
                            #the data processor has been recycled and this data processor is now tracking a new target
                            self._first_packet_sent = False
                            self._target_id = target_id
                    else:
                        #Convert the data bytes back to sorted data
                        time_slice_sort_key, sensor_vals = AT_Protocol.bytes_to_sorted_data(data_bytes=data_packet_bytes)
    #                     self.log.log2(msg1='Target: ' + target_id, msg2=str(time_slice_sort_key), caller=self, msgty=AT_Logging.MSG_TYPE_DEBUG)
                        
                        if (not self._first_packet_sent):
                            self._rate_filtered.reset()
                            self._rate_prefiltered.reset()
                            self._first_packet_sent = True
                            
                            self.set_new_log(self.log_file)
                            self._filter = SavGolFilterQueue(params=self._params)
                            self._listener_multicast = AT_ListenerMulticast(dir_store=self._dir_store, 
                                cluster_id=self._connection_ids[i].cluster_id,
                                target_id=self._connection_ids[i].target_id,
                                params=self.params, log=self.log)
                
                        #Process packet components
                        if (time_slice_sort_key > self._last_time_slice_sort_key):
                            #Sometimes the socket buffer can send the same data twice.  Check to ensure advancing time stamp
                            self._last_time_slice_sort_key = time_slice_sort_key
                            self._process_packet(self._target_id, time_slice_sort_key, sensor_vals)
                
            if (no_data):
                time.sleep(0.1)
        return

    
    def _process_packet(self, target_id, time_slice_sort_key, sensor_vals):
        '''
        Process data from a single packet group.
        '''
        if (self.params.ONLY_LOG_SENSOR != None):
            #Debug setting to output the value from a single sensor for logging
            #This setting should be remarked out in the conf file to deactivate
            for snsr_val in sensor_vals: #List in form: [sensor_id, distance]
                if (snsr_val[0] == self.params.ONLY_LOG_SENSOR):
                    log_str = ''
                    log_str = str(time_slice_sort_key) + ' , ' + log_str + ',' + snsr_val[0] + ',' + str(snsr_val[1])
                    print(log_str)
                    
        elif (len(sensor_vals) >= 4):
            #There must be at least 4 sensors to trilaterate
            self._incomplete_cnt = 0
                
            sphere_coords_list = []
            dist = 0.0
            log_str = ''
            for snsr_val in sensor_vals: #List in form: [sensor_id, distance]
                snsr_device = self._get_sensor_device(sensor_id=snsr_val[0])
                
                if (snsr_device == None):
                    self.log.log2(msg1='Directory server missing sensor:', msg2=snsr_val[0], caller=self, msgty=AT_Logging.MSG_TYPE_DEBUG)
                else:
                    sphr = SphereCoordinates(X=snsr_device.X, Y=snsr_device.Y, Z=snsr_device.Z, \
                        Radius=snsr_val[1], Differential=0, Name=snsr_device.sensor_id)
                    
                    log_str = log_str + ',' + snsr_device.sensor_id + ',' + str(snsr_val[1])
                    sphere_coords_list.append(sphr)
            trilat = AT_Trilateration(sphere_coords_list)
            
            #Pre-filtered result printing
            self._rate_prefiltered.increment_cnt()
            if (self.params.PRINT_PREFILTERED_RESULTS):
                log_str = str(time_slice_sort_key) + ',' + str(trilat.get_result())  + log_str
                self.log.log2(msg1='Pre-Filter:', msg2=log_str, caller=self, msgty=AT_Logging.MSG_TYPE_DEBUG)
                
            #Listener Update 
            self._listener_multicast.refresh_check()
            #send trilaterated data through secondary filter.  Results are returned when filtered data
            #is available.
            rslts = self._filter.enqueue(slice_ts=time_slice_sort_key, coord_xyz=trilat.get_result())
            #Multicast send results
            if (len(rslts) > 0):
                for rslt in rslts:
                    self._rate_filtered.increment_cnt()
                    self._listener_multicast.send(result_line=rslt)
                    #For debugging, the settings file allows printing filtered results to the screen
                    if (self.params.PRINT_FILTERED_RESULTS):
                        self.log.log2(msg1='Filtered:', msg2=str(rslt), caller=self, msgty=AT_Logging.MSG_TYPE_DEBUG)
        else:
            #Not enough readings in time slice.  This may mean that the time slice queue buffer needs to be
            #enlarged or the window reduced
            self._incomplete_cnt += 1
            if (self._incomplete_cnt >= self.INCOMPLETE_STATUS):
                self.log.log3(msg1=str(self._incomplete_cnt) + " Incomplete reading from", msg2=str(len(sensor_vals)), msg3='sensors', caller=self, msgty=AT_Logging.MSG_TYPE_DEBUG)
                self._incomplete_cnt = 0
        return
    
    def __init__(self, dir_store, pipe_pool:AT_PipePool, params):
#         sensor:SensorDevice
        super().__init__(params=params, log_file=self.log_file)
        self._dir_store = dir_store
        self._pipe_pool = pipe_pool
        self._listeners = []
        self._sensors = []
        
        #setup connection id list
        self._connection_ids = []
        for i in range(0, self._pipe_pool.num_pipes):
            self._connection_ids.append(None)
        return
        
    
    def _get_sensor_device(self, sensor_id:str)->SensorDevice:
        '''
        Gets the sensor from the local property or the directory store.  
         
        Note: Sometimes this method is called as such a speed that the datastore cannot 
        fulfill the request in time.  Thus, this has error correction to retry.
        '''
        for snsr in self._sensors:
            #snsr = SensorDevice
            if (snsr.sensor_id == sensor_id):
                return snsr
        
        #If the code makes it to here, the sensor needs to be retrieved from the directory server
        tries = 0
        success = False
        snsr = None
        while ((not success) and (tries < 10)):
            try:
                snsr = self._dir_store.get_sensor(sensor_id=sensor_id)
                success = True
            except Exception as exi:
                tries += 1
                if (tries < 10):
                    time.sleep(.02)
                else:
                    self.log.log3(msg1="Data Store Exception:", msg2=str(exi), msg3='Type:' + type(exi).__name__, caller=self, msgty=AT_Logging.MSG_TYPE_DEBUG)
                    raise exi
        if (snsr != None):
            self._sensors.append(snsr)
        return snsr


        