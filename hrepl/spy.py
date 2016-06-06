
import os
import sys
import logging

LOG = logging.getLogger(__name__)

try:
    import numpy
    isarray = lambda o: isinstance(o, numpy.ndarray)
    LOG.debug('numpy available')
except ImportError:
    isarray = lambda o: False
    LOG.debug('numpy not available')

def file_exists(path):
    try:
        os.stat(path)
        return True
    except:
        return False

def modules_in_path():
    modules = []
    for root in sys.path:
        # empty is current directory
        if len(root) == 0:
            root = './'
        # get listing
        try:
            contents = os.listdir(root)
        except:
            continue
        # check if is py file or dir contains __init__
        for content in contents:
            if content.endswith('.py'):
                module_name = content.split('.py')[0]
            elif file_exists(os.path.join(root, content, '__init__.py')):
                module_name = content
            else:
                continue
            modules.append(module_name)
    return modules
