from SessionTimedOutException import SessionTimedOutException
from datetime import datetime
import time
import httplib

class Shell:
    def __init__(self, toolbox, index, prompt):
        self._toolbox = toolbox
        self._index = index
        self._prompt = prompt # old shell


    def write(self, command):
        if self._toolbox.get_streaming_flag():
            # CTRL+C + clean shell (in case of user changing page while stream is on)
            print "KILLED CATCHED"
            self._prompt.kill()
            self.read()
            self._toolbox.disable_streaming_flag()

        self._prompt.write(command)


    def read(self):
        ret = self._prompt.read()
        begin = self._oldTime = datetime.now()

        while (len(ret) == 0) and not (self.is_timer_expired(begin)):
            time.sleep(0.2)
            ret = self._prompt.read()

        if ("Rex::TimeoutError Operation timed out." in ret) or self.is_timer_expired(begin):
            self._toolbox.session_kill(self._index)
            raise SessionTimedOutException("SessionTimedOutException: session {} is dead.".format(self._index))

        if ("Broken pipe from" in ret):
            raise httplib.CannotSendRequest()

        return ret


    def kill(self):
        """ Do a CTRL+C on the meterpreter session """
        self._prompt.kill()


    def is_timer_expired(self, begin):
        currentTime = datetime.now()
        delta = (currentTime - begin).total_seconds()
        return delta > 30
