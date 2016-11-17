'''
Created on Nov 11, 2016

@author: Joel Blackthorne
'''

import time
import pyttsx
from aero_tracker.common.at_threaded_base import AT_ThreadedBase
from queue import Queue

class AT_Audio(AT_ThreadedBase):
    '''
    Thread to speak queued items
    '''
    QUEUE_TIMEOUT = 0.1
    
    _speech_queue = Queue
    _speech_engine = None
    _speaking = False
    
    def add_text(self, text_phrase):
        self._speech_queue.put(item=text_phrase, block=False)
        return
    
    def run_clycle(self):
        '''
        Executes within the while is_running loop.
        '''
        if ((not self._speaking) and (not self._speech_queue.empty())):
#             and not self._speech_engine.isBusy()):
            try:
                itm = self._speech_queue.get(block=False, timeout=1)
                if (itm != None):
                    self._speaking = True
                    try:
#                         self._speech_engine = pyttsx.init()
                        rate = self._speech_engine.getProperty('rate')
                        self._speech_engine.setProperty('rate', rate)
                        voices= self._speech_engine.getProperty('voices')
                        #for voice in voices:                                                                                    
                        self._speech_engine.setProperty('voice', 'english-us')
                        print('Busy:', str(self._speech_engine.isBusy()))
                        self._speech_engine.say(itm)
                        
                        rs = self._speech_engine.runAndWait()
                        self._speech_engine.iterate()
#                         self._speech_engine.stop()
                        time.sleep(0.1)
#                         self._speech_engine.startLoop(False)
#                         self._speech_engine.iterate()
#                         try:
#                             self._speech_engine.endLoop()
#                         except:
#                             pass
                    except Exception as ex:
                        print(ex)
                    self._speaking = False
                else:
                    #Nothin to say
                    time.sleep(0.5)
            except Exception as ex_get:
                print(ex_get)
        else:
            time.sleep(0.1)
        return

    def __init__(self, params):
        '''
        Constructor
        '''
        
        super().__init__(params=params, log_file='./log/at_audio.log')
        self._speech_queue = Queue()
        self._speech_engine = pyttsx.init()
        self.add_text('AeroTracker online')
        return

#Tester
def signalHandler(arg1, arg2):
    print(AT_Audio, "signalHandler called to shutdown process")
    print(arg1,arg2)
    return

obj = AT_Audio(params=None)
obj.start()
# time.sleep(1)
obj.add_text('Plus 10.2 feet')
# time.sleep(1)
obj.add_text('Minus 4 feet')
# time.sleep(1)
# obj.stop()

while (True):
    time.sleep(1)
    pass




