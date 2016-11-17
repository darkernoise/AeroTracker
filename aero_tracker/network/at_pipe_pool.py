'''
Created on Oct 22, 2016

@author: Joel Blackthorne
'''

import typing
import multiprocessing as mp
from multiprocessing.connection import Connection

class AT_PipePool(object):
    '''
    Pool of pipes for sending data across processes.
    '''
    
    _params = None
    _num_pipes = 1
    _pool_parent_cons = typing.List
    _pool_child_cons = typing.List
    _usage_list = typing.List
    
    @property
    def parent_conns(self):
        '''
        Parent pipe connections.
        '''
        return self._pool_parent_cons
    
    @property
    def usage_list(self):
        return self._usage_list
    
    @property
    def num_pipes(self):
        return self._num_pipes
    
    def get_pipe_pool(self):
        return self
    
    def get_available_pool_index(self):
        for i in range(0, self._num_pipes):
            if (not self._usage_list[i]):
                self._usage_list[i] = True
                return i
            
        raise Exception('No pipes are available for use.')
        return
    
    def release_pool_index(self, indx):
        self._usage_list[indx] = False
        return
    
    def get_child_pipe(self, pipe_index)->Connection:
        '''
        Gets a child pipe by index.
        '''
        return self._pool_child_cons[pipe_index]

    def __init__(self, params, num_pipes):
        '''
        Constructor
        '''
        self._params = params
        self._num_pipes = num_pipes
        self._init_pipe_pool(num_pipes)
        self._init_usage_list(num_pipes)
        return
    
    def __del__(self):
        #Close all the pipes
        for i in range(0, self._num_pipes):
            chld = self._pool_child_cons[i]
            try:
                chld.close()
            except:
                pass
            prnt = self._pool_parent_cons[i]
            try:
                prnt.close()
            except:
                pass
        return
    
    def _init_usage_list(self, num_pipes):
        self._usage_list = []
        for i in range(0, num_pipes):
            self._usage_list.append(False)
        return
    
    def _init_pipe_pool(self, num_pipes):
        '''
        Pre-opens a pool of worker pipes.
        '''
        self._pool_parent_cons = []
        self._pool_child_cons = []
        for i in range(0, num_pipes):
            parent_conn, child_conn = mp.Pipe()
            self._pool_parent_cons.append(parent_conn)
            self._pool_child_cons.append(child_conn)
        return
    
    
        