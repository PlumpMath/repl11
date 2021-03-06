
"repl11 cli"

import sys
import logging
import argparse


parser = argparse.ArgumentParser(description='repl11')
verbosity = parser.add_mutually_exclusive_group()

verbosity.add_argument(
        '-v', 
        '--verbose', 
        action='store_true',
        help='Increase verbosity (log level from INFO to DEBUG)')

verbosity.add_argument(
        '-q', 
        '--quiet', 
        action='store_true',
        help='Decrease verbosity (log level from INFO to WARNING)')

parser.add_argument(
        '-s',
        '--stream',
        action='store_true',
        help='Log to internal stream, accessible by API')

args, _ = parser.parse_known_args()

if args.quiet:
    loglevel = logging.WARNING
elif args.verbose:
    loglevel = logging.DEBUG
else:
    loglevel = logging.INFO

from . import log

log.setup_logging(loglevel, stream=args.stream)

LOG = logging.getLogger(__name__)
LOG.info('logging system setup')

from . import loop

parser.add_argument(
        '-l',
        '--loop', 
        choices=loop.available.keys(),
        default='base',
        help='Event loop to use (defaults to base, HTTP-only)')

parser.add_argument(
        '-p',
        '--port',
        default=4242,
        type=int,
        help='Port number to start on (default 4242)')

parser.add_argument(
        '-H',
        '--host',
        default='127.0.0.1',
        help='Host name to serve on (default 127.0.0.1)')


args = parser.parse_args()
LOG.info('starting with args %r', args)

MainLoop = loop.available[args.loop]
main_loop = MainLoop(host=args.host, port=args.port)
main_loop()


