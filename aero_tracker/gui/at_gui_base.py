'''
Created on Nov 12, 2016

@author: Joel Blackthorne
'''
import typing
import os
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from aero_tracker.params.at_result_listener_params import AT_ResultListenerParams
from aero_tracker.client.at_result_data_queue import AT_ResultDataQueue
from aero_tracker.log.at_logging import AT_Logging

class AT_GUI_Base(object):
    '''
    Standard base functionality for all AeroTracker front-end components.
    '''
    CONF_DIR = 'conf'
    LOG_DIR = 'log'
    CONF_FILE_NAME = 'at_gui.conf'
    LOG_FILE_NAME = 'at_graph.log'
    RESULT_LOG_FILE_NAME = 'at_graph_results.log'
    
    SOURCE_DIRECTORY = 'aero_tracker'
    GLADE_DIR = 'glade'
    
    _params = AT_ResultListenerParams
    _glade_bldr = Gtk.Builder()
    _window_id = 'window_id'
    _glade_file = 'glad.glade'
    _min_window_height = 600
    _min_window_width = 800
    _rslt_data_queue = AT_ResultDataQueue
    _pole_to_cluster = typing.List
    _cluster_to_pole = typing.Dict
    
    @property
    def glade_bldr(self):
        return self._glade_bldr
    
    @property
    def params(self):
        return self._params
    
    @property
    def log_file(self):
        rval = os.path.normpath(AT_GUI_Base.get_base_dir() + os.sep + self.LOG_DIR + os.sep + self.LOG_FILE_NAME)
        print('Using log file: ', rval)
        return rval
    
    @property
    def result_log_file(self):
        rval = os.path.normpath(AT_GUI_Base.get_base_dir() + os.sep + self.LOG_DIR + os.sep + self.RESULT_LOG_FILE_NAME)
        print('Using log file: ', rval)
        return rval
    
    @property
    def conf_file(self):
        rval = os.path.normpath(AT_GUI_Base.get_base_dir() + os.sep + self.CONF_DIR + os.sep + self.CONF_FILE_NAME)
        return rval
    
    @staticmethod
    def get_conf_file():
        rval = os.path.normpath(AT_GUI_Base.get_base_dir() + os.sep + AT_GUI_Base.CONF_DIR + os.sep + AT_GUI_Base.CONF_FILE_NAME)
        print('Using conf file: ', rval)
        return rval
    
    @staticmethod
    def get_base_dir():
        rval = os.getcwd()
        if (rval.endswith('gui')):
            rval = rval[:-17]
        elif(rval.endswith('aerotracker' + os.sep + 'aero_tracker')):
            rval = rval[:-13]
        return rval
    
    '''
    Events Section
    '''
    def on_window_delete(self, *args):
        '''
        Standard event handler for main window delete.
        '''
        self._rslt_data_queue.stop()
        Gtk.main_quit(*args)
        
    def on_window_show(self, *args):
        '''
        Standard event handler for main window delete.
        '''
        return
    
    def on_data_handler(self, sender, **kwargs):
        '''
        cluster_id = kwargs['cluster_id']
        target_id = kwargs['target_id']
        target_index = kwargs['target_index']
        '''
#         target_id = kwargs['target_id']
#         target_index = kwargs['target_index']
#         self._log.log2(msg1='Data Arrived for target:', msg2=str(target_id), caller=self, msgty=AT_Logging.MSG_TYPE_DEBUG)
        return
    
    def on_cut_handler(self, sender, **kwargs):
        '''
        target_id
        target_index
        num_cuts
        '''
        print('Cut - Target: ' + kwargs['target_id'])
        return
    
    def on_turn_apex_handler(self, sender, **kwargs):
        '''
        target_id
        target_index
        lap_number
        turn_apex
        '''
        trn_apex = kwargs['turn_apex']
        
#         print('Turn Apex = ' + "%.2f" % float(kwargs['turn_apex']) + \
#             ' lap #: ' + kwargs['lap_number'] + \
#             ' target: '+ kwargs['target_id'])
        print('Turn Apex = ' + "%.2f" % (trn_apex[2]) + \
            ' lap #: ' + str(kwargs['lap_number']) + \
            ' cluster: ' + kwargs['cluster_id'] + \
            ' target: '+ kwargs['target_id'])
        return
    
    def get_gui_object(self, object_id:str):
        return self.glade_bldr.get_object(object_id)
    
    def get_pole_from_cluster(self, cluster_id):
        return self._cluster_to_pole[cluster_id]
    
    def get_cluster_for_pole(self, pole_num):
        indx = pole_num - 1
        return self._pole_to_cluster[indx]
    
    def _load_glade(self):
        self.glade_bldr.add_from_file(self._glade_file_path())
        self.glade_bldr.connect_signals(self)
#         window.set_size_request(self._min_window_width,self._min_window_height)
        return
    
    def _glade_file_path(self)->str:
        rval = os.path.normpath(AT_GUI_Base.get_base_dir() + os.sep + self.SOURCE_DIRECTORY + os.sep + self.GLADE_DIR + os.sep + self._glade_file)
        return rval
    

    def __init__(self, gui_name:str, window_id:str, glade_file:str, min_window_height=600, min_window_width=800):
        '''
        Constructor
        '''
        self._min_window_width = min_window_width
        self._min_window_height = min_window_height
        self._window_id = window_id
        self._glade_file = glade_file
        self._load_glade()
        
        self._params = AT_ResultListenerParams(self.get_conf_file())
        self._log = AT_Logging(params=self._params, log_file=self.log_file)
        self._rslt_data_queue = AT_ResultDataQueue(self._params, gui_name, log_file=self.result_log_file)
        #Set even handlers
        self._log.log2(msg1='Registering event handlers', msg2='', caller=self, msgty=AT_Logging.MSG_TYPE_DEBUG)
        self._rslt_data_queue.on_data.register(self.on_data_handler)
        self._rslt_data_queue.on_turn_apex.register(self.on_turn_apex_handler)
        self._rslt_data_queue.on_cut.register(self.on_cut_handler)
        self._rslt_data_queue.start()
        self._load_pole_to_cluster()
        #Save the background buffer
#         self._background = self._graph_figure.canvas.copy_from_bbox(self._graph_axis.bbox)
        self._log.log2(msg1='Fully started', msg2='', caller=self, msgty=AT_Logging.MSG_TYPE_DEBUG)
        return
        
        
    def _load_pole_to_cluster(self):
        self._cluster_to_pole = {
            'SP':1,
            'NP':2
            }
        self._pole_to_cluster = ['SP','NP'] 
        return
    
        
        