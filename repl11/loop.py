
"Event loops"

import logging

from . import http

class BaseLoop(object):
    "Basic event loop, only processing HTTP requests"

    def __init__(self, address='127.0.0.1', port=8080, protocol='HTTP/1.0'):
        self.address = address 
        self.port = port 
        self.protocol = protocol 
        self.log = logging.getLogger(repr(self))
        self.setup()

    def setup(self):
        http.Handler.protocol_version = self.protocol
        self.server = http.Server((self.address, self.port), http.Handler)
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

    def __init__(self, qt=None, **kwds):
        super(PGLoop, self).__init__(**kwds)
        self.qt = qt

    def setup(self):
        super(PGLoop, self).setup()
        if self.qt == 'pyqt':
            import PyQt
        elif self.qt == 'pyside':
            import PySide
        import pyqtgraph as pg
        self.app = pg.mkQApp()
        self.log.info('PG QtApp successfully created %r', self.app)

    def handle(self):
        super(PGLoop, self).handle()
        self.app.processEvents()

