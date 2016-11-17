'''
Created on Sep 18, 2016

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
# from aero_tracker.network.at_socket_handler_base import AT_SocketHandlerBase
from aero_tracker.server.directory.at_directory_server_client import AT_DirectoryServerClient
from aero_tracker.client.at_result_listener_socket_server import AT_ResultListenerSocketServer
from aero_tracker.network.at_protocol import AT_Protocol
from aero_tracker.log.at_logging import AT_Logging
from aero_tracker.client.at_result_listener_thread import AT_ResultListenerThread

class ResultListenerBase(object):
    '''
    Result Listener Base class.
    '''
    
    @property
    def listener_name(self)->str:
        raise Exception("Must redefine in inheriting class")
        return
    
    @property
    def params(self):
        return self._params
    
    @property
    def handler_class(self):
        raise Exception("Must redefine in inheriting class")
        return
    
    
    _params = None
    _log = None
    _client_data_port = 0
    _host_address = ""
    _socket_srvr = None
    _rslt_queue = None
    _rl_thread = None
    _log_file = '/var/log/aerotracker/at_results.log'
    
    def start(self):
        #Serve and listen for incoming connections
        self._rl_thread.start()
#         self._socket_srvr.serve_forever()
        return
    
    def close(self):
        if (self._rl_thread != None):
            self._rl_thread.stop()
        return
    

    def __init__(self, params, rslt_queue, log_file):
        '''
        Constructor
        '''
        self._log_file = log_file
        self._params = params
        self._log = AT_Logging(params=self._params,log_file=log_file)
        self._rslt_queue = rslt_queue
        self._host_address = self._get_local_interface_address()
        self._set_dir_store(host_address=self._host_address, port=self._params.port)
        self._open_listening_port(self._host_address)
        self._register_as_result_listener(host_address=self._host_address, port=self._client_data_port)
        self._rl_thread = AT_ResultListenerThread(rslt_lstner_socket_server=self._socket_srvr, params=self.params, log_file=log_file)
        return
    
    def __del__(self):
        self.close()
        return
    
    def _set_dir_store(self, host_address, port):
        self._log.log2(msg1='Connecting to Directory Server:', msg2=host_address + ':' + str(port), caller=self, msgty=AT_Logging.MSG_TYPE_INFO)
        dirsvr_client = AT_DirectoryServerClient(server_name=self._params.server_name, 
            port=self._params.port, auth_key=self._params.manager_auth_key, log=self._log)
        self._dir_store = dirsvr_client.get_dirctory_store()
        return
    
    def _register_as_result_listener(self, host_address, port):
        self._log.log2(msg1='Registering as result listener:', msg2=host_address + ':' + str(port), caller=self, msgty=AT_Logging.MSG_TYPE_INFO)
        self._dir_store.add_result_data_listener(listener_name=self.listener_name, address=host_address, port=port)
        return
    
    def _open_listening_port(self, server_address):
        #Start up a local multiprocessing manager server for use by the incoming sockets 
        #to this data processing worker.  This has to be started before the socket listeners
        #in oder to get thh generated address and port
        self._log.log(msg1='Starting to open a listening port:', caller=self, msgty=AT_Logging.MSG_TYPE_INFO)
        connected = False
        tries = 0
        data_port = self._params.port + 1#port to start trying at
        while ((not connected) and (tries < 10)):
            try:
                self._socket_srvr = AT_ResultListenerSocketServer((self._dir_store), server_address=(server_address, data_port), \
                        RequestHandlerClass=self.handler_class,
                        params=self._params,
                        terminator=AT_Protocol.DATA_TERMINATOR)
                self._socket_srvr.set_listener_address(server_address)
                self._socket_srvr.set_listener_port(data_port)
                self._socket_srvr.set_result_queue(self._rslt_queue)
                self._socket_srvr.log_file = self._log_file
                connected = True
            except Exception as ex:
                tries += 1
                data_port += 1
                
        if (connected):
            self._client_data_port = data_port
            self._log.log2(msg1='Successfully opened listening port on:', msg2=server_address + ':' + str(data_port), caller=self, msgty=AT_Logging.MSG_TYPE_INFO)
        else:
            data_port = 0
            raise Exception("Could not open listening port for client.")
        return data_port
    
    
    def _get_local_interface_address(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect((self._params.server_name,self._params.port))
            addr = s.getsockname()[0]
            s.close()
        except Exception as ex:
            self.log.log2(msg1='Could not connect to directory server:', msg2=str(ex), caller=self, msgty=AT_Logging.MSG_TYPE_ERROR)
            raise ex
        return addr
    
    
    