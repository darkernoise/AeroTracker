'''
Created on Oct 22, 2016

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
import socket
from aero_tracker.network.at_pipe_pool import AT_PipePool
from aero_tracker.params.at_sensor_cluster_params import ATSensorClusterParams
from aero_tracker.common.at_process_base import AT_ProcessBase
from aero_tracker.log.at_logging import AT_Logging
from aero_tracker.network.at_sensor_data_packet import AT_SensorDataPacket
from aero_tracker.trilateration.at_time_slice_queue import AT_TimeSliceQueue
from aero_tracker.trilateration.raw_data.ts_queue_item import TSQueueItem
from aero_tracker.network.at_data_proc_address import AT_DataProcAddress
from aero_tracker.network.at_protocol import AT_Protocol
from aero_tracker.server.directory.at_directory_mp_manager import AT_DirectoryMPManager
from aero_tracker.data.at_data_rate import AT_DataRate
from scipy import cluster

class AT_DataSorter(AT_ProcessBase):
    '''
    This object reads from the data pipes connected to the sensor targets in order to 
    group the data by target and then synchronize the data into time slices.  In the 
    case multiple entries are received from the same sensor, for the same time slice,
    those values are averaged into a single entry.
    
    Only results with over 4 sensors present are sent to the data processor.
    '''
    NUM_PIPES = 6 #TODO  This needs to be incremented based on the number of sensor arrays
    SYNCHRONIZE_ON_TIME_DIFF = 0.5
    STATISTICS_UPDATE_NUM = 1000
    
    _pipe_pool = AT_PipePool
    _time_slice_queue = AT_TimeSliceQueue
    _packet_timer = None
    _target_data = typing.Dict
    _dir_store = None
    _rate_total_sort = AT_DataRate
    _rate_packet_sort = AT_DataRate
        
    @property
    def pipe_pool(self):
        return self._pipe_pool
    
    def run_clycle(self):
        '''
        Executes within the while is_running loop.
        '''
        if (self._packet_timer == None):
            self._packet_timer = time.time()
        
        no_data = True
        datpkt = AT_SensorDataPacket
        
        for i in range(0, self._pipe_pool.num_pipes):
            conn = self._pipe_pool.parent_conns[i]
            if (conn.poll()):
                data_packet_bytes = conn.recv()
                if (data_packet_bytes != None):
                    no_data = False
#                     print(data_packet_bytes)
                    
                    datpkt = AT_SensorDataPacket.from_packet_bytes(pkt_bytes=data_packet_bytes)
                    if (not datpkt.target_id in self._target_data):
                        #Target does not exist
                        tsqueue = AT_TimeSliceQueue(log=self.log, params=self.params)
                        dataproc_socket = self._get_data_proc_connection(target_id=datpkt.target_id,cluster_id=datpkt.cluster_id)
                        self._target_data.update({datpkt.target_id:[tsqueue,dataproc_socket]})
                        
                    #Add to the proper target queue    
                    tsqueue = self._target_data[datpkt.target_id][0] #AT_TimeSliceQueue
                    tsqueue.enqueue(sensor_datpkt=datpkt)
#                     itm = TSQueueItem
                    itm = tsqueue.pop() #TSQueueItem
                    if (itm != None):
#                         dataproc_socket = socket.socket
                        dataproc_socket = self._target_data[datpkt.target_id][1]
                        if (dataproc_socket == None):
                            #Socket was closed due to connection error
                            try:
                                dataproc_socket = self._get_data_proc_connection(target_id=datpkt.target_id,cluster_id=datpkt.cluster_id)
                                self._target_data[datpkt.target_id][1] = dataproc_socket
                            except:
                                pass
                            
                        if (dataproc_socket != None):
                            #socket is open and ok
                            try:
                                dataproc_socket.send(AT_Protocol.sorted_data_bytes( 
                                    time_slice=itm.time_slice, tsq_sensors=itm.sensors))
                                self._rate_packet_sort.increment_cnt()
#                                 print(str(itm.time_slice.sort_key) + ' # sensors:' + str(len(itm.sensors)))  
                            except Exception as ex:
                                #Socket error occurred
                                self.log.log2(msg1='Socket exception occurred:', msg2=str(ex), caller=self, msgty=AT_Logging.MSG_TYPE_WARNING)
                                self._closeServerSocket(target_id=datpkt.target_id, dataproc_socket=dataproc_socket)
                                self._target_data[datpkt.target_id][1] = None
                                
                    #Statistics update
                    self._rate_total_sort.increment_cnt()
        
        #Do cleanup during slow cycles
        if (no_data):
            #See if any queues are inactive
            self._check_for_inactive_queues()
            time.sleep(0.1)
        
        return
    
    def _check_for_inactive_queues(self):
        trgt_queue = AT_TimeSliceQueue
        for target_id in self._target_data:
            trgt_queue = self._target_data[target_id][0]
            dataproc_socket = self._target_data[target_id][1]
            if (trgt_queue.queue_inactive):
                #Close the socket and free the data processing server
                self._closeServerSocket(target_id=target_id, dataproc_socket=dataproc_socket)
                self._free_data_proc_srvr(target_id=target_id)
                #Free the inactive queue
                del self._target_data[target_id]
        return

    def __init__(self, params:ATSensorClusterParams, log_file:str):
        '''
        Constructor
        '''
        super().__init__(params=params, log_file=log_file)
        self._pipe_pool = AT_PipePool(params=params, num_pipes=params.num_sensors)
        self._time_slice_queue = AT_TimeSliceQueue(log=self.log, params=params)
        self._target_data = {}
        self._rate_total_sort = AT_DataRate(log=self.log, report_label='Total packets', report_cnt=self.STATISTICS_UPDATE_NUM)
        self._rate_packet_sort = AT_DataRate(log=self.log, report_label='Sorted packets', report_cnt=self.STATISTICS_UPDATE_NUM)
        return
    
    
    
    def _get_data_proc_connection(self, target_id:str, cluster_id:str)->socket.socket:
        '''
        Opens a socket to a data processing server for a target id.
        '''
        rval = None
        addr = self._get_data_proc_srvr_address(target_id=target_id,cluster_id=cluster_id)
        if (addr != None):
            rval = self._openServerSocket(data_proc_addr=addr)
            #the sorted counter label
            self._rate_packet_sort.set_label(report_label=cluster_id + '-' + target_id +' Sorted pkts')
            #send id packet 
            rval.send(AT_Protocol.sensor_cluster_id_bytes(target_id=target_id, cluster_id=cluster_id))
        return rval
    
    def _get_data_proc_srvr_address(self, target_id:str, cluster_id:str)->AT_DataProcAddress:
        '''
        Contact the directory server and get a data processing server for the given target.
        '''
        rval = None
        tries = 0
        while ((rval == None) and (tries < 10)):
            try:
                if (self._dir_store == None):
                    self._dir_store = self._get_directory_store()
                rval = self._dir_store.get_data_port_for_target(target_id=target_id,cluster_id=cluster_id)
            except Exception as ex:
                self._log.log2(msg1='Exception:', msg2=str(ex), caller=self, msgty=AT_Logging.MSG_TYPE_DEBUG)
                tries += 1
                self._dir_store = None
                
            if (rval == None):
                self._log.log2(msg1='Data proc server unavailable for target:', msg2=target_id, caller=self, msgty=AT_Logging.MSG_TYPE_WARNING)
                self._log_data_proc_servers() 
                time.sleep(1)
        return rval
    
    def _free_data_proc_srvr(self, target_id):
        try:
            if (self._dir_store == None):
                self._dir_store = self.free_data_proc_srvr(target_id)
#             rval = self._dir_store.get_data_port_for_target(sensor=self._sensor, target_id=target_id)
        except Exception as ex:
            self._log.log2(msg1='Exception:', msg2=str(ex), caller=self, msgty=AT_Logging.MSG_TYPE_DEBUG)
            self._dir_store = None
        return
    
    def _get_directory_store(self):
        '''
        Get instance of the directory store from the manager
        '''
        if (self._dir_store != None):
            return self._dir_store
        
        manager_connected = False
        AT_DirectoryMPManager.register_client_methods()
        manager =  AT_DirectoryMPManager(address=(self._params.server_name, self._params.port), \
            authkey=bytearray(self._params.manager_auth_key,'ascii'))
        while (not manager_connected):
            try:
                manager.connect()
                manager_connected = True
            except Exception as ex:
                self.log.log2(msg1='Unable to connect to Directory Server Manager at:', \
                    msg2=self._params.server_name + ':' + str(self._params.port), caller=self, msgty=AT_Logging.MSG_TYPE_WARNING)
            
        self._dir_store = manager.get_instance()
        return self._dir_store
    
    def _log_data_proc_servers(self):
        assgns = self._dir_store.get_data_proc_srvr_assignments()
        for assgn in assgns:
            self._log.log3(msg1='Data Proc Srvr Assigned:', msg2='target: ' + assgn[0], msg3=str(assgn[1]), caller=self, msgty=AT_Logging.MSG_TYPE_INFO)
        return
       
    def _openServerSocket(self, data_proc_addr:AT_DataProcAddress):
        rval = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        rval.connect((data_proc_addr.address, int(data_proc_addr.port)))
        self._log.log2(msg1='Connected on socket:', msg2=str(data_proc_addr), caller=self, msgty=AT_Logging.MSG_TYPE_INFO)
        return rval
         
    def _closeServerSocket(self, target_id:str, dataproc_socket:socket.socket):
        try:
            self._log.log2(msg1='Disconnecting Target', msg2=target_id, \
                caller=self, msgty=AT_Logging.MSG_TYPE_INFO)
        except:
            pass
        if (dataproc_socket != None):
            try:
                if (not dataproc_socket._closed):
                    dataproc_socket.close()
            except:
                pass
        return
    
        