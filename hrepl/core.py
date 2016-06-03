
import re
import os
import ast
import sys
import atexit
import tempfile
import traceback
from urlparse import urlparse, parse_qs
import BaseHTTPServer

try:
    from cStringIO import StringIO
except:
    from StringIO import StringIO

try:
    import numpy
    isarray = lambda o: isinstance(o, numpy.ndarray)
except ImportError:
    isarray = lambda o: False

class LineOffsetter(ast.NodeVisitor):
    "Offsets lineno fields in an AST node"

    def __init__(self, lineinc):
        self.lineinc = lineinc

    def generic_visit(self, node):
        super(LineOffsetter, self).generic_visit(node)
        if hasattr(node, 'lineno'):
            node.lineno += self.lineinc

def compiled_with_info(src, lineinc, filename, mode):
    "Compile code with line and file information"
    code = ast.parse(src)
    LineOffsetter(lineinc).visit(code)
    return compile(code, filename, mode)

exec_temp_files = []

def dedent(src):
    "Unindent a block of code"
    leftmostcol = 1000
    lines = src.split('\n')
    for l in lines:
        if l.strip(): # i.e. ignore empty lines
            start = re.search(r'\S', l).start()
            if start < leftmostcol:
                leftmostcol = start
    return '\n'.join([l[leftmostcol:] for l in lines])

class Snippet(object):
    "Code sent that is somewhere in file in client"
    client_file = ''
    client_line = 0

class HREPL(BaseHTTPServer.BaseHTTPRequestHandler):

    def do_GET(self):
        pr = urlparse(self.path)
        qd = parse_qs(pr.query, keep_blank_values=True, strict_parsing=True)
        target = getattr(self, 'do_' + '_'.join(pr.path[1:].split('/')), None)
        if target is None:
            return self.send_response(404)
        self.send_response(200)
        self.end_headers()
        self.wfile.write(target(**qd))
    
    def do_ex(self, message=[], **kwds):
        src = message[0]
        print src
        print repr(src)
        out, err = sys.stdout, sys.stderr
        sio = StringIO()
        sys.stdout = sys.stderr = sio
        try:
            try:
                print repr(eval(src, globals()))
            except SyntaxError:
                # TODO have Vim send us file & line numbers instead of using a temp file
                f = tempfile.NamedTemporaryFile(suffix='.py', delete=False)
                exec_temp_files.append(f)
                f.write(dedent(src))
                f.close()
                execfile(f.name, globals())
        except Exception as e:
            print e
            traceback.print_exc(e)
        sys.stdout, sys.stderr = out, err
        output = sio.getvalue()
        print 'output = ', repr(output)
        return output

    def do_complete(self, message=[], **kwds):
        name = message[0]
        if '.' in name:
            parts = name.split('.')
            base, name = '.'.join(parts[:-1]), parts[-1]
            try:
                keys = dir(eval(base, globals()))
            except Exception as e:
                print 'completion failed', e
                return ''
            base += '.'
        else:
            base = ''
            keys = globals().keys()
        return ','.join('%s%s' % (base, k) for k in keys if k.startswith(name))

    def do_describe(self, message=[], **kwds):
        name = message[0]
        g = globals()
        if name == 'whos':
            return '\n'.join('%-30s %s' % (k, type(g[k]))
                             for k in sorted(g.keys())
                             if not k.startswith('_'))
        if name not in g:
            return ''
        obj = g[name]
        #if isinstance(obj, numpy.ndarray):
        if 'ndarray' in type(obj).__name__:
            return '%s %r' % (obj.dtype.name, obj.shape)
        else:
            return repr(obj)[:80]

@atexit.register
def close_temp_files():
    for f in exec_temp_files:
        try:
            os.unlink(f.name)
        except Exception as e:
            print e


def main(address='127.0.0.1', port=8080, protocol='HTTP/1.0', pg=False):
    if pg:
        import pyqtgraph
        app = pyqtgraph.mkQApp()
    HREPL.protocol_version = protocol
    httpd = BaseHTTPServer.HTTPServer((address, port), HREPL)
    httpd.timeout = 0.01
    sa = httpd.socket.getsockname()
    print 'HREPL on ', sa[0], 'port', sa[1]
    while True:
        httpd.handle_request()
        if pg:
            app.processEvents()
