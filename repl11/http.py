
import json
import pprint
import logging
import urlparse

from BaseHTTPServer import (
        BaseHTTPRequestHandler, 
        HTTPServer as Server
    )

from . import code, ns

NS = ns.Namespaces()

class Handler(BaseHTTPRequestHandler):

    log = logging.getLogger(__name__ + '.Handler')

    def parse_path(self):
        self.log.debug('parsing path %r', self.path)
        request = urlparse.urlparse(self.path)
        query   = urlparse.parse_qs(request.query,
                    keep_blank_values=True, strict_parsing=True)
        target = '_'.join(request.path[1:].split('/'))
        self.log.debug('target=%r, query %r', target, query)
        return target, query

    def do_GET(self):
        target, query = self.parse_path()
        method = getattr(self, 'do_' + target, None)
        if method:
            self.log.debug('GETing target method %r', method)
            self.send_response(200)
            self.end_headers()
            self.wfile.write(method(**query))
        else:
            self.log.debug('method not found for target %r', target)
            self.send_response(404)

    def do_ex(self, message=[], **kwds):
        src = message[0]
        # TODO namespace handling
        reload(code)
        reload(ns)
        result = code.Code(src)(NS['default'])
        if 'result' in result:
            result['result'] = pprint.pformat(result['result'])
        js = json.dumps(result)
        self.log.debug('response: %r', js)
        return js


    def do_complete(self, message=[], **kwds):
        name = message[0]
        if '.' in name:
            parts = name.split('.')
            base, name = '.'.join(parts[:-1]), parts[-1]
            try:
                keys = dir(eval(base, NS['default']))
            except Exception as e:
                LOG.info('completion failed %r', e)
                return ''
            base += '.'
        else:
            base = ''
            keys = NS['default'].keys()
        return ','.join('%s%s' % (base, k) for k in keys if k.startswith(name))

    def do_describe(self, message=[], **kwds):
        name = message[0]
        g = NS['default']
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

