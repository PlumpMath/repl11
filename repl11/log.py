
"Logging stuff"

import sys
import time
import logging

CFG = {}

class LogStream(object):
    
    def __init__(self):
        self.records = []

    def write(self, msg, *args):
        t = time.time()
        if args:
            msg %= args
        self.records.append((t, msg))

    def since(self, t):
        i = len(self.records) - 1
        while self.records[i][0] > t and i > 0:
            i -= 1
        return self.records[i:]

    def flush(self):
        pass

def setup_logging(level, stream=False):
    if stream:
        stream = sys.stdout = sys.stderr = LogStream()
    else:
        del stream
    CFG.update(locals())
    logging.basicConfig(**CFG)

