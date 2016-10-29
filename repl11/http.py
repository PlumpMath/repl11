
import json
import pprint
import logging
import urlparse

from BaseHTTPServer import (
        BaseHTTPRequestHandler, 
        HTTPServer as Server
    )

from . import code, spy, log


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
        self.log.debug('kwds %r', kwds)
        lineno = int(kwds['lineno'][0]) - 1
        filename = kwds['filename'][0]
        mod = spy.module_from_path(filename)
        self.log.debug('running in module %r', mod)
        result = code.Code(src, filename, lineno)(mod)
        if 'result' in result:
            result['result'] = pprint.pformat(result['result'])
        js = json.dumps(result)
        self.log.debug('response: %r', js)
        return js


    def do_complete(self, message=[], **kwds):
        name = message[0]
        filename = kwds['filename'][0]
        self.log.debug('completing in ns %r on %r', filename, name)
        mod = spy.module_from_path(filename)
        if '.' in name:
            parts = name.split('.')
            base, name = '.'.join(parts[:-1]), parts[-1]
            try:
                keys = dir(eval(base, mod.__dict__))
            except Exception as e:
                self.log.info('completion failed %r', e)
                return ''
            base += '.'
        else:
            base = ''
            keys = mod.__dict__.keys()
        return ','.join('%s%s' % (base, k) for k in keys if k.startswith(name))

    def do_describe(self, message=[], **kwds):
        def describe(obj):
            if 'ndarray' in type(obj).__name__:
                desc = '%s %r' % (obj.dtype.name, obj.shape)
            else:
                desc = repr(obj)[:80]
            return desc
        name = message[0]
        filename = kwds['filename'][0]
        g = spy.module_from_path(filename).__dict__
        if name == 'whos':
            desc = '\n'.join('%-30s %s' % (k, describe(g[k]))
                             for k in sorted(g.keys())
                             if not k.startswith('_'))
        elif name not in g:
            desc = ''
        else:
            desc = describe(g[name])
            #if isinstance(obj, numpy.ndarray):
        return json.dumps({
            'status': 'ok',
            'out': desc,
            'result': 'None'
            })


    def do_log(self, since=[], **kwds):
        "Retrieve log contents"
        t = float(since[0]) if since[0] else 0.0
        return json.dumps(log.CFG['stream'].since(t))



