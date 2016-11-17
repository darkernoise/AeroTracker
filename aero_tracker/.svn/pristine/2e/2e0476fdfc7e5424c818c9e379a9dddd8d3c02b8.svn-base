'''
Created on Oct 4, 2016

@author: Joel Blackthrone
'''

from aero_tracker.common.at_threaded_base import AT_ThreadedBase
from aero_tracker.client.at_result_listener_socket_server import AT_ResultListenerSocketServer
from aero_tracker.log.at_logging import AT_Logging

class AT_ResultListenerThread(AT_ThreadedBase):
    '''
    Separate thread for the socket server.
    '''
    
    _rslt_lstner_socket_server = None
    
    def run_clycle(self):
        '''
        Executes within the while is_running loop.
        '''
        self.log.log1(msg1='Result Listner Thread stopping', caller=self, msgty=AT_Logging.MSG_TYPE_INFO)
        return
    
    def before_run(self):
        '''
        Executes before the run cycle starts.
        '''
        self._rslt_lstner_socket_server.serve_forever()
        return

    def __init__(self, rslt_lstner_socket_server:AT_ResultListenerSocketServer, params, log_file):
        '''
        Constructor
        '''
        self._rslt_lstner_socket_server = rslt_lstner_socket_server
        super().__init__(params=params, log_file=log_file)
        return
    
        