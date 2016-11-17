'''
Created on Sep 9, 2016

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
from aero_tracker.log.at_logging import AT_Logging
from aero_tracker.server.directory.at_directory_mp_manager import AT_DirectoryMPManager

class AT_DirectoryServerClient(object):
    '''
    Primary client logic to connect to the directory server and to access the directory store object.
    '''
    
    _server_name = ''
    _port = 0
    _auth_key = ''
    _log = None
    
    def get_dirctory_store(self):
        '''
        Get instance of the directory store from the manager
        '''
        manager_connected = False
        tries = 0
        AT_DirectoryMPManager.register_client_methods()
        manager =  AT_DirectoryMPManager(address=(self._server_name, self._port), \
            authkey=bytearray(self._auth_key,'ascii'))
        while ((not manager_connected) and (tries < 15)):
            try:
                manager.connect()
                manager_connected = True
            except Exception as ex:
                self.log.log2(msg1='Unable to connect to Directory Server Manager at:', \
                    msg2=self._server_name + ':' + str(self._port), caller=self, msgty=AT_Logging.MSG_TYPE_WARNING)
                tries += 1
            
        self._dir_store = manager.get_instance()
        return self._dir_store
    
    def validate_directory_store_address(self, except_on_error=True):
        '''
        Checks to ensure that there is a server and port available at the specified
        address.
        '''
        test_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        test_sock.settimeout(3)
        is_valid = False
        try:
            test_sock.connect((self._server_name,self._port))
            is_valid = True
        except Exception as ex:
            if (except_on_error):
                raise Exception('Could not Connect to Directory Server at ' + self._server_name + ':' + str(self._port))
        return is_valid

    def __init__(self, server_name, port, auth_key, log:AT_Logging):
        '''
        Constructor
        '''
        self._server_name = server_name
        self._port = port
        self._log = log
        self._auth_key = auth_key
        self.validate_directory_store_address(except_on_error=True)
        return
        