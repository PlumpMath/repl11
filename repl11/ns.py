"Support for distinct namespaces" 

class NameSpace(object):

    # per script, or default
    # per module
    # exe performs generic run & return last value
    # introspection tools expect a namespace..

    all = {}
    
    @classmethod
    def module(cls, mod):
        if type(mod) in (str, unicode):
            mod = __import__(str_or_mod_obj)
        return cls(mod.__name__, mod.__dict__)

    @classmethod
    def frame(cls):
        "Allow attach to specific frame / function"
        raise NotImplemented

    def __new__(cls, name, dict=None):
        if name not in cls.all:
            cls[name] = super(NameSpace, cls).__new__(name, dict=dict)
        return cls[name]

    def __init__(self, name, dict=None):
        self.name = name
        self.dict = dict or {}


