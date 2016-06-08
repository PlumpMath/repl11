"Support for distinct namespaces" 

import logging

LOG = logging.getLogger(__name__)

class Namespaces(object):

    # per script, or default
    # per module
    # exe performs generic run & return last value
    # introspection tools expect a namespace..

    def __init__(self):
        self.all = {}

    def __getitem__(self, key):
        if key not in self.all:
            self.all[key] = {}
        return self.all[key]


