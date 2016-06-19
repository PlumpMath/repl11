
"Implments instrospection utilities"

import os
import sys
import types
import logging

# much fun to be had here, not just completion..
import inspect
import symtable

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

def modname_from_path(path):
    "Guess a module from path"
    filename = os.path.abspath(path)
    found = False
    for path in sys.path:
        apath = os.path.abspath(path)
        if filename.startswith(apath):
            found = True
            break
    if found:
        dirname = os.path.dirname(filename)
        if not dirname.endswith(os.path.sep):
            dirname += os.path.sep
        LOG.debug('found %r for %r', apath, filename)
        LOG.debug('dirname %r', dirname)
        reldir = dirname.split(apath + os.path.sep)[1]
        basename = os.path.basename(filename)
        basemod = basename.split('.py')[0]
        parentname = reldir.replace(os.path.sep, '.')
        LOG.debug('parentname %r', parentname)
        modname = parentname + basemod
        # don't create a fake module just because hasn't been
        # imported yet
        """
        try:
            LOG.debug('preemptively importing module %r', modname)
            __import__(modname)
        except:
            pass
        """
        return modname
    return filename

def get_module(key):
    if key not in sys.modules:
        LOG.debug('%r not in sys.modules', key)
        sys.modules[key] = types.ModuleType(key)
    mod = sys.modules[key]
    LOG.debug('found for %r module %r', key, mod)
    return mod

def module_from_path(path):
    guess = modname_from_path(path)
    LOG.debug('guess modname %r from path %r', guess, path)
    return get_module(guess)

