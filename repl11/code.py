
"""
Code handling functions & classes.

"""

import ast


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

def syntax_mode(source):
    "Evaluate mode of syntax for source"
    mode = 'eval'
    try:
        ast.parse(source, mode=mode)
    except SyntaxError:
        mode = 'exec'
        try:
            ast.parse(source, mode=mode)
        except SyntaxError as mode:
            pass
    return mode

def assign_last(mod, key='_'):
    "Modify parsed module `mod` inline such that the last expression or "
    "assignment is also assigned to a variable named `key`."
    last = mod.body[-1]
    us = [ast.Name(id=key, ctx=ast.Store())]
    if isinstance(last, ast.Expr):
        last = ast.Assign(targets=us, value=last)
    elif isinstance(last, ast.Assign):
        last.targets = us + last.targets
    mod.body[-1] = last
    return mod


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

    def __exit__(self):
        self.swap()

    @property
    def contents(self):
        return self.sio.getvalue()


class Code(object):
    "Code sent that is somewhere in file in client"

    nofile = '<no file>'
    noline = 0
    lastkey = '_'

    def __init__(self, source, filename=nofile, lineno=noline):
        self.source   = dedent(source)
        self.filename = filename
        self.lineno   = lineno
        self.mode     = syntax_mode(source)
        self.log = logging.getLogger(repr(self))

        for i, line in enumerate(source.split('\n')):
            self.log.debug('%02d  %s', i, line)
        self.log.debug('requires mode %r', self.mode)

        if isinstance(self.mode, SyntaxError):
            raise self.mode

        self.mod  = assign_last(ast.parse(source), key=self.lastkey)
        self.code = ast.fix_missing_locations(ast.parse(source))
        self.code = ast.increment_lineno(self.code, n=self.lineno)
        self.object = compile(self.code, self.filename, self.mode)

    def __call__(self, namespace):
        "Run code in namespace"

        co = self.object
        ns = namespace.dict
        pf = pprint.pformat

        if self.mode == 'eval':
            return pf(eval(co, ns))

        else:
            with IOCapture() as io:
                exec co in ns
            return "%s\n%s" % (
                    io.contents, 
                    pf(ns[self.lastkey])
                )


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
