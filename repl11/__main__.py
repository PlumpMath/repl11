
"""
Running hrepl module as __main__ means we need to start a hrepl 
server correctly based on arguments. 

"""

import sys
import argparse

parser = argparse.ArgumentParse(description='repl11')

import logging

logging.basicConfig(
    level=logging.DEBUG if '-v' in sys.argv else logging.INFO)

from .core import main

main(pg='--pg' in sys.argv)
