from SessionTimedOutException import SessionTimedOutException
from datetime import datetime
import time

class Shell:
    def __init__(self, toolbox, index, prompt):
        self._toolbox = toolbox
        self._index = index
        self._prompt = prompt # old shell


    def write(self, command):
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

        return ret


    def is_timer_expired(self, begin):
        currentTime = datetime.now()
        delta = (currentTime - begin).total_seconds()
        return delta > 30
