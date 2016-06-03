
"""
Running hrepl module as __main__ means we need to start a hrepl 
server correctly based on arguments. 

"""

import sys

from .core import main

main(pg='--pg' in sys.argv)
