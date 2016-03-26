hrepl
=====

This is simultaneously 

- no-dependencies Python REPL served over HTTP with completion and help, 
- a Vim client to said server

requiring only Vim w/ Python and a Python with stdlib (so PyPy, Jython
should work in principle).

This is motivated by needing to work on Windows (bye tmux_, tslime_) and
even when not using IPython/ZMQ (bye vim-ipython_)
This is currently specific to Vim and Python, but in principle can be
extended to any combination of server & client.

By the way, if you're missing a good terminal and tmux on Windows, you're
missing out on ConEmu_.

install
-------

Assuming you use Pathogen_, clone
this under you bundles directory. Now the Vim client should work.
Next, in your bundles/hrepl directory, run 
``python setup.py install --user`` to install the server.

use
---

Fire up the hrepl however you like, e.g.  ``python -m hrepl``
and open a Python file in Vim. ``<F9>`` sends the paragraph under
the cursor, ``K`` gets documentation for ``<cword>``, etc. Read
``ftplugin/python.vim`` to see what's up. (Re)map according to taste.

missing
-------

- visual debugging
- correct translation of tracebacks to quickfixlist (buggy implementation
  thereof is already in place)
- line profiling blocks of code (get wrapped in @profiled defs)
- correct threading for IPython as well as Qt
- embedding into running application
- eval/exev within specific module a la clojure


.. _tmux: http://tmux.sourceforge.net
.. _tslime: http://www.vim.org/scripts/script.php?script_id=3023
.. _vim-ipython: https://github.com/ivanov/vim-ipython
.. _ConEmu: http://code.google.com/p/conemu-maximus5
.. _Pathogen: https://github.com/tpope/vim-pathogen
