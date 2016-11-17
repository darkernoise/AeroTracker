'''
Created on Oct 4, 2016

@author: Joel Blackthorne
'''

class AT_Event(object):
    '''
    Base class for AeroTracker events.
    '''

    _handlers = []
    
    @property
    def handlers(self):
        return self._handlers

    def __init__(self):
        self._handlers = []
        return
    
    def register(self, handler):
        self._handlers.append(handler)
        return self
    
    def remove(self, handler):
        self._handlers.remove(handler)
        return self
    
    def fire(self, sender, **kwargs):
        for handler in self._handlers:
            handler(sender, **kwargs)
        return
    
    __iadd__ = register
    __isub__ = remove
    __call__ = fire
        