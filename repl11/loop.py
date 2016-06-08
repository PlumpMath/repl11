
"Event loops"

import logging

from . import http

class BaseLoop(object):
    "Basic event loop, only processing HTTP requests"

    def __init__(self, host='127.0.0.1', port=8080, protocol='HTTP/1.0'):
        self.host = host 
        self.port = port 
        self.protocol = protocol 
        self.log = logging.getLogger(repr(self))
        self.setup()

    def setup(self):
        http.Handler.protocol_version = self.protocol
        self.server = http.Server((self.host, self.port), http.Handler)
        self.server.timeout = 0.01
        self.log.info('serving on %s:%d', *self.server.socket.getsockname())

    def handle(self):
        self.server.handle_request()
        
    def __call__(self):
        "Run event loop"
        while True:
            self.handle()

class PGLoop(BaseLoop):
    "Integrates processing PyQtGraph events"

    def setup(self):
        super(PGLoop, self).setup()
        import pyqtgraph as pg
        self.app = pg.mkQApp()
        self.log.info('PG QtApp successfully created %r', self.app)

    def handle(self):
        super(PGLoop, self).handle()
        self.app.processEvents()


available = {}
for k, v in globals().items():
    if not isinstance(v, type):
        continue
    if issubclass(v, BaseLoop):
        name = k.split('Loop')[0].lower()
        available[name] = v
del k, v, name
