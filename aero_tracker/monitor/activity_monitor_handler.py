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

from aero_tracker.network.at_protocol import AT_Protocol
from aero_tracker.log.at_logging import AT_Logging
# from aero_tracker.monitor.monitor_base import MonitorBase

class ActivityMonitorHandler(object):
    '''
    Socket data handler for incoming activity data connections.
    '''
    
    _log = None
    _params = None
    
    def handle(self, connection, address):
        request = None
        client_connected = True
        prior_data = ""
        
        self._log.log4(msg1='Data connection:', msg2=str(connection), msg3='Connected at:', msg4=str(address), caller=self, msgty=AT_Logging.MSG_TYPE_INFO)
        while (client_connected):
            data = str(connection.recv(self.READ_LEN), 'ascii')
            data = prior_data + data
            prior_data = "" #Clear prior data after use.  
            #Critical Note: A client has only two read cycles to send a command. Otherwise, the whole 
            #command is erased and the client must start over.
            #This is handled differently than a data connection to ensure complete and accurate commands.
    
            if ((data == None) or (data == "")):
                client_connected = False
                connection_params = None
            elif (len(data) == 0):
                client_connected = False
                connection_params = None
            elif ((data.index(AT_Protocol.COMMAND_TERMINATOR) <= 0) or 
                  (data[-1] != AT_Protocol.COMMAND_TERMINATOR)):
                #command is incomplete
                self._log.log4(msg1='Incomplete data received:', msg2=str(connection), msg3='data:', msg4=str(data), caller=self, msgty=AT_Logging.MSG_TYPE_WARNING)
                prior_data += data
                data = ""
            else:
                pkts = data.split(sep=AT_Protocol.COMMAND_TERMINATOR)
                num_pkts = len(pkts)
                for i in range(0, num_pkts):
#                 for pkt in pkts:
                    pkt = pkts[i]
                    pkt_len = len(pkt)
                    if (pkt_len > 0):
                        print("Data: ", pkt)
                        #TODO
#                         MonitorBase.data_recived(data=pkt, calling_process=connection)
#                         try:
#                             cmd = AT_Command(pkt)
#                             if (cmd.command == AT_Protocol.COMMAND_REQUEST_SERVER_PORT):
#                                 cmd_port_req = AT_CommandDataPortRequest(cmd)
#                                         
#                         except Exception as ex:
#                             if (self.PARAMS.debug_level >= 2):
#                                 print("Client: ", connection, " Connected at: ", address, " Exception: ", ex)
#                                 traceback.print_exc(file=sys.stdout)
                
            if (not client_connected):
                self._log.log4(msg1='Data disconnected:', msg2=str(connection), msg3='From:', msg4=str(address), caller=self, msgty=AT_Logging.MSG_TYPE_INFO)    
        return

    def __init__(self, params):
        '''
        Constructor
        '''
        self._params = params
        self._log = AT_Logging(self._params)
        return