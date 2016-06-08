
"""
Code handling functions & classes.

"""

import re
import sys
import ast
import pprint
import logging
import traceback
import cStringIO


def dedent(source):
    "Unindent a block of code"
    leftmostcol = 1000
    lines = source.split('\n')
    for l in lines:
        if l.strip(): # i.e. ignore empty lines
            start = re.search(r'\S', l).start()
            if start < leftmostcol:
                leftmostcol = start
    return '\n'.join([l[leftmostcol:] for l in lines])

def assign_last(mod, key='_'):
    "Modify parsed module `mod` inline such that the last expression or "
    "assignment is also assigned to a variable named `key`."
    last = mod.body[-1]
    if isinstance(last, ast.Expr):
        assigned = True
        us = [ast.Name(id=key, ctx=ast.Store())]
        last = ast.Assign(targets=us, value=last.value)
        mod.body[-1] = last
    else:
        assigned = False
    return mod, assigned


class IOCapture(object):
    # TODO stdin??

    def __init__(self):
        self.out = self.err = self.sio = cStringIO.StringIO()
        self.active = False

    def swap(self):
        self.active = not self.active
        self.out, sys.stdout = sys.stdout, self.out
        self.err, sys.stderr = sys.stderr, self.err

    def __enter__(self):
        self.swap()
        return self

    def __exit__(self, et, ev, tb):
        self.swap()

    @property
    def contents(self):
        return self.sio.getvalue()


class Code(object):
    "Handles a snippet of code from client that can be executed."

    nofile = '<no file>'
    noline = 0
    lastkey = '_'

    def __init__(self, source, filename=nofile, lineno=noline):
        self.source   = dedent(source)
        self.filename = filename
        self.lineno   = lineno
        self.log = logging.getLogger(repr(self))

        for i, line in enumerate(source.split('\n')):
            self.log.debug('%02d  %s', i, line)

        try:
            self.mod = ast.parse(self.source)
            self.mod, self.lastexpr = assign_last(self.mod, key=self.lastkey)
            self.code = ast.fix_missing_locations(self.mod)
            self.code = ast.increment_lineno(self.code, n=self.lineno)
            self.log.debug(ast.dump(self.code))
            self.obj = compile(self.code, self.filename, 'exec')
        except Exception as exc:
            self.log.warning('compilation failed: %r', exc)
            self.obj = exc

    def __call__(self, namespace):
        "Run code in namespace"

        fail = lambda tb, exc, out: {
                 'status'   : 'fail'
                ,'traceback': tb
                ,'result': exc
                ,'out': out
                }

        if isinstance(self.obj, Exception):
            self.log.warning('compilation failure')
            ret = fail([], self.obj, '')

        else:
            try:
                with IOCapture() as io:
                    exec self.obj in namespace
                ret = {'status': 'ok'
                      ,'out'   : io.contents
                      ,'result': namespace[self.lastkey] 
                                 if self.lastexpr else None
                      }

            except Exception as exc:
                _, _, tb = sys.exc_info()
                ret = fail(traceback.extract_tb(tb), exc, io.contents)
                self.log.debug(pprint.pformat(ret['traceback']))
                self.log.warning('execution exception %r', exc)

        return ret

"""

For the moment, we assume that the client editor can turn traceback 
information into useful file/line information, and that persistance on 
disk isn't required.  If this turns out to be a bad assumption, then maybe
resurrect this class.


class TempFiler(object):
    "Handle temporary files"

    import os, atexit, logging

    def __init__(self, **tempkwds):
        self.filenames = []
        self.log = logging.getLogger(repr(self))
        self.tempkwds = tempkwds
        atexit.register(self.cleanup)

    def write_new(self, contents):
        fd = tempfile.NamedTemporaryFile(suffix='.py', delete=False)
        self.log.debug('new temporary file %s', fd.name)
        self.filenames.append(fd.name)
        fd.write(contents)
        fd.close()
        return fd.name

    def cleanup(self):
        for name in self.filenames:
            self.log.debug('cleaning up %s', name)
            try:
                os.unlink(name)
            except Exception as exc:
                self.log.exception(exc)

"""
