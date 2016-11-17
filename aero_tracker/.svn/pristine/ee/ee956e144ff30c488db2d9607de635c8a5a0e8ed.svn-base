'''
Created on Aug 15, 2016

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

import socket
import threading
import time
from aero_tracker.log.at_logging import AT_Logging
from aero_tracker.network.at_protocol import AT_Protocol
from aero_tracker.network.at_response import AT_Response
from aero_tracker.exception.at_exception import AT_Exception
from aero_tracker.network.at_command_reg_data_listener import AT_CommandRegDataListener
from aero_tracker.monitor.activity_monitor_handler import ActivityMonitorHandler

class MonitorBase(threading.Thread):
    '''
    Base class for data and activity monitors.
    '''
    
    RECEIVE_SIZE = 200

    _run = False
    _data_socket = None
    _tcp_socket = None
    _params = None
    _client_data_port = 0
    _log = None
    _registered = False
    _connect_cnt = 0
    
    @staticmethod
    def data_recived(data, calling_process=""):
        #TODO: Finish
        return
    
    @staticmethod
    def connection_handle(connection, address, params):
        req_hndl = ActivityMonitorHandler(params)
        req_hndl.handle(connection, address)
        return
    
    def run(self):
        threading.Thread.run(self)
        tries = 0
        while ((self._run) and (tries < 100)):
            try:
                self.execute_direct()
                tries = 0
            except Exception as ex:
                self._log.log2(msg1='Failed to connect to Manager Server:', msg2=str(ex), caller=self, msgty=AT_Logging.MSG_TYPE_ERROR)
                tries += 1
            time.sleep(.5)
        return
    
    def execute_direct(self):
        '''
        Directly execute inside the existing thread.  This method opens a listening port for a data publisher to connect.
        '''
        if (not self._registered):
            self._registered = self.connect_and_register()
        self._log.log2(msg1='About to wait for a connection. Cons so far:', msg2=str(self._connect_cnt), caller=self, msgty=AT_Logging.MSG_TYPE_DEBUG)
        conn, address = self._data_socket.accept()
        thread = threading.Thread(target=MonitorBase.connection_handle, args=(conn, address, self._params))
        thread.daemon = True
        thread.start()
        self._connect_cnt += 1
        self._log.log2(msg1='Incoming connection. Cons so far:', msg2=str(self._connect_cnt), caller=self, msgty=AT_Logging.MSG_TYPE_DEBUG)
        return
                
    
    def start(self):
        if (not self._run):
            threading.Thread.start(self)
            self._run = True
        return
    
    def stop(self):
        self.close_data_socket()
        self._run = False
        return
    
    def connect_and_register(self):
        '''
        Connect to the directory server and register as a data listener. The data listener has to open its
        own listening ports and act as a server since there can be many data processing servers parallel 
        processing the location data for various targets.
        '''
        try:
            self._openManagerSocket()
            client_ip = self._tcp_socket.getsockname()[0] #Gets the ip address of the client used to connect to the manager server
            client_port = self._open_listening_port(client_address=client_ip)
            
            self._tcp_socket.send(bytes(AT_Protocol.cmd_register_data_listener(client_display_name=self._params.client_display_name, \
                client_address=client_ip, client_port=client_port),'ascii'))
            resp = str(self._tcp_socket.recv(self.RECEIVE_SIZE), 'ascii')
            if ((resp != None) and (len(resp) > 0)):
                pkts = resp.split(sep=AT_Protocol.RESPONSE_TERMINATOR)
                if (len(pkts) >= 1):
                    resp = AT_Response.from_packet_bytes(pkts[0])
                    if (self._params.debug_level >= 1):
                        self._log.log4(msg1='Connection from Client:', msg2=str(client_ip), msg3='at Port:', msg4=str(client_port), caller=self, msgty=AT_Logging.MSG_TYPE_INFO)
                        self._log.log4(msg1='Status:', msg2=str(resp.data[0]), msg3='registered data servers:', \
                            msg4=str(resp.data[1]), caller=self, msgty=AT_Logging.MSG_TYPE_DEBUG)
                else:
                    #There was an error, so skip
                    ex = AT_Exception(source=self, method='connect_and_register', \
                        message='Invalid server response.', details='More than 1 response arrived to request.')
                    raise ex
                    return
        except Exception as ex:
            self._log.log(msg1='Failed to register with manager server as data listener.', caller=self, msgty=AT_Logging.MSG_TYPE_ERROR)
            raise ex
        finally:
            self._closeManagerSocket()
        return True
    
    def close_data_socket(self):
        try:
            self._data_socket.close()
        except:
            pass
        return
    
    def __init__(self, params):
        '''
        Constructor
        '''
        super().__init__()
        self._params = params
        self._log = AT_Logging(self._params)
        return
    
    def __del__(self):
        self.close_data_socket()
        return
    
    def _openManagerSocket(self):
        try:
            self._tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#             self._tcp_socket.connect((self._manager_host_name, int(self._manager_port)))
            self._tcp_socket.connect((self._params.server_name, int(self._params.port)))
        except Exception as ex:
            self._log.log4(msg1='Could not connect to manager server:', msg2=self._manager_host_name, \
                msg3='at port:', msg4=str(self._manager_port), caller=self, msgty=AT_Logging.MSG_TYPE_ERROR)
            raise ex
        return
        
    def _closeManagerSocket(self):
        if (self._tcp_socket != None):
            try:
                if (not self._tcp_socket._closed):
                    self._tcp_socket.close()
            except:
                pass
        self._tcp_socket = None
        return
    
    def _open_listening_port(self, client_address):
        connected = False
        tries = 0
        data_port = self._params.port + 1 #port to start trying at
        self._data_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        while ((not connected) and (tries < 100)):
            try:
                self._data_socket.bind((client_address, data_port))
                self._data_socket.listen(1)
                connected = True
            except Exception as ex:
                tries += 1
                data_port += 1
                
        if (connected):
            self._client_data_port = data_port
        else:
            data_port = 0
        return data_port
        