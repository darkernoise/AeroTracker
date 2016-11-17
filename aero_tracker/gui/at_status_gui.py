'''
Created on Nov 11, 2016

@author: Joel Blackthorne
'''

# import os
import typing
import gi
from pygments.lexers import graph
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.animation as animation

import numpy as np

# from matplotlib.backends.backend_gtk3agg import FigureCanvasGTK3Agg as FigureCanvas
from matplotlib.backends.backend_gtk3cairo import FigureCanvasGTK3Cairo as FigureCanvas


from matplotlib.figure import Figure

from aero_tracker.gui.at_gui_base import AT_GUI_Base

class AT_GraphObjects(object):
    figure = None
    axis = None
    flight_paths = []
    
    def __init__(self, figure, axis, flight_paths):
        self.figure = figure
        self.axis = axis
        self.flight_paths = flight_paths
        return
    

class AT_StatusGUI(AT_GUI_Base):
    '''
    AeroTracker race status front-end consolidates the results from multiple data processors.
    '''
    GLADE_FILE = 'at_status_window.glade'
    WINDOW_ID = 'window_at_status'
    GUI_NAME = 'AeroTracker Status Client'
    
    _status_bar = None
    _status_bar_context = None
    _log_view = None
    _graph_canvas = FigureCanvas
    
    _axis_1 = None
    _axis_2 = None
    _axis_3 = None
    _axis_4 = None
    _use_blit = False
    
    _pole_targets = typing.List
    _graph_objects = typing.List
    
    def on_window_show(self, *args):
        '''
        Standard event handler for main window delete.
        '''
        self._set_status_bar(status_text="Welcome to " + self.GUI_NAME + "!")
        
        return
    
    def on_data_handler(self, sender, **kwargs):
        '''
        cluster_id = kwargs['cluster_id']
        target_id = kwargs['target_id']
        target_index = kwargs['target_index']
        '''
        super().on_data_handler(sender, kwargs)
        
        cluster_id = kwargs['cluster_id']
        target_id = kwargs['target_id']
        target_index = kwargs['target_index']
        
        pole_index = self.get_pole_from_cluster(cluster_id=cluster_id) - 1
        tgt = self._pole_targets[pole_index]
        if (tgt == None):
            self._pole_targets[pole_index] = {target_id:target_index}
        else:
            if (not target_id in tgt):
                tgt.update({target_id:target_index})
            else:
                tgt[target_id] = target_index
            
        return
    
    def update_flight_path_pole_1(self, num):
        '''
        Updates the animated flight path curve.  This is called by the graph is real-time 
        to get a data point for a specific interval number.
        '''
        indx = 0
        graph_obj = self._graph_objects[0]
        try:
            for target_id in self._pole_targets[0]:
                if (target_id != None):
                    target_index = self._pole_targets[0][target_id]
                    
                    gx = self.__rslt_data_queue.graph_x(target_index=target_index)
                    gy = self.__rslt_data_queue.graph_y(target_index=target_index)
#                     gz = self.__rslt_data_queue.graph_z(target_index=target_index)
                    
                    flight_path = graph_obj.fight_paths[indx]
                    indx += 1
                    flight_path.set_data(gx, gy)
                    
        except Exception as ex:
            return self._flight_path
        
        #redraw 
        try:
            if (self._use_blit):
                graph_obj.figure.canvas.restore_region(self._background)
                graph_obj.axis.draw_artist(self._flight_path)
                graph_obj.figure.canvas.blit(self._graph_axis.bbox)
            else:
                plt.draw()
        except Exception as ex:
            print(ex)
            raise ex
         
        return flight_path,
    
    def init_flight_path(self):
#         self._flight_path, = self._graph_axis.plot([0.0,0.1], [0.0,0.1], [0.0,0.1], linewidth=2.0, color='b')
        return self._flight_path,

    def __init__(self):
        '''
        Constructor
        '''
        super().__init__(gui_name=self.GUI_NAME,window_id=self.WINDOW_ID, glade_file=self.GLADE_FILE)
        self._graph_objects = []
        self._init_pole_targets()
        self._init_log_view()
        self._add_graphing_plots()
#         self._add_test_graph()
        
        return
    
    def _init_pole_targets(self):
        self._pole_targets = [None, None, None, None]
        return
    
    def _set_status_bar(self, status_text):
        if (self._status_bar == None):
            self._status_bar = self.glade_bldr.get_object('statusbar1')
        self._status_bar_context = self._status_bar.get_context_id("status")
        self._status_bar.push(self._status_bar_context,status_text)
        return
    
    
    def _add_graphing_plots(self):
        '''
        Adds the graphs to the window.
        '''
        self._pole_flight_paths = []
        fig = Figure(figsize=(5, 5))
         
#         self._axis_1 = plt.subplot2grid((2,2),(0, 0))
#         self._axis_2 = plt.subplot2grid((2,2),(0, 1))
#         self._axis_3 = plt.subplot2grid((2,2),(1, 0))
#         self._axis_4 = plt.subplot2grid((2,2),(1, 1))
        
        self._axis_1 = fig.add_subplot(221)
        self._axis_3 = fig.add_subplot(222)
        self._axis_2 = fig.add_subplot(223)
        self._axis_4 = fig.add_subplot(224)
         
        self._init_graph(figure=fig, graph_axis=self._axis_1,graph_title='Pole 1')
        self._init_graph(figure=fig, graph_axis=self._axis_2,graph_title='Pole 2')
        self._init_graph(figure=fig, graph_axis=self._axis_3,graph_title='Pole 3')
        self._init_graph(figure=fig, graph_axis=self._axis_4,graph_title='Course')
        
#         annimation = animation.FuncAnimation(fig, 
#             self.update_flight_path_pole_1, 
#             frames=200, 
#             init_func=self.init_flight_path,
#             interval=20, 
#             blit=self._use_blit)
         
        self._graph_canvas = FigureCanvas(fig)  # a gtk.DrawingArea         
        window_graph = self.get_gui_object('scrolledwindow_graph')
        window_graph.add_with_viewport(self._graph_canvas)
        window_graph.show()
        window_graph.set_visible(True)
        return
      
    def _init_graph(self, figure, graph_axis, graph_title):
        graph_axis.set_xlabel('X')
        graph_axis.set_ylabel('Y')
        graph_axis.set_title(graph_title)
         
        self._plot_pole(graph_axis)
        graph_axis.plot()
        
        flight_paths = []
        flight_path, = graph_axis.plot([0.0,0.1], [0.0,0.1], linewidth=2.0, color='b')
        flight_paths.append(flight_path)
        flight_path, = graph_axis.plot([0.0,0.1], [0.0,0.1], linewidth=2.0, color='g')
        flight_paths.append(flight_path)
        flight_path, = graph_axis.plot([0.0,0.1], [0.0,0.1], linewidth=2.0, color='p')
        flight_paths.append(flight_path)
        flight_path, = graph_axis.plot([0.0,0.1], [0.0,0.1], linewidth=2.0, color='o')
        flight_paths.append(flight_path)
        
        graph_obj = AT_GraphObjects(figure=figure, axis=graph_axis, flight_paths=flight_paths)
        self._graph_objects.append(graph_obj)
        
        return
     
    def _plot_pole(self, graph_axis):
        '''
        Plots the pole on the graph.
        '''

        x = 0
        y = 0
        graph_axis.plot(x,y,'or', label='Pole',linewidth=3.0, color='r')
        return
     
    def _init_log_view(self):
        #textview_raw_data
        self._log_view = self.get_gui_object('textview_raw_data')
        self._log_view.set_size_request(300,500)
        return
    
#Main application
obj = AT_StatusGUI()
window = obj.glade_bldr.get_object(AT_StatusGUI.WINDOW_ID)
window.show_all()
Gtk.main()

