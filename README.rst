repl11
======

This is simultaneously 

- no-dependencies Python REPL served over HTTP with completion and help, 
- a Vim client to said server

requiring only Vim w/ Python and a Python with stdlib (so PyPy, Jython
should work in principle).

This is motivated by needing to work on Windows (bye tmux_, tslime_) and
even when not using IPython/ZMQ (bye vim-ipython_).
This is currently specific to Vim and Python, but in principle can be
extended to any combination of server & client.

By the way, if you're missing a good terminal and tmux on Windows, you're
missing out on ConEmu_.

install
-------

Assuming you use Pathogen_, clone
this under you bundles directory. Now the Vim client should work.
Next, in your bundles/repl11 directory, run 
``python setup.py install --user`` to install the server.

use
---

Fire up the repl11 however you like, e.g.  ``python -m repl11``
and open a Python file in Vim. ``<F9>`` sends the paragraph under
the cursor, ``K`` gets documentation for ``<cword>``, etc. 
``<c-x><c-u>`` completes. Read
``ftplugin/python.vim`` to see what's up. (Re)map according to taste.

missing
-------

- visual debugging
- correct translation of tracebacks to quickfixlist (buggy implementation
  thereof is already in place)
- line profiling blocks of code (get wrapped in @profiled defs)
- embedding into running application
- eval/exev within specific module a la clojure based on current file
- logging of session
- open definition, show source, etc.
- repl config : which interpreter, pythonpath, cwd, venv etc. 
- start repl from vim's python in subprocess
- complete available modules

- cover as much as possible with tests.. 
- monkey patching methods & functions: find class and objects, ... 
- implement js/codemirror & vim clients as demos
- read pdb sources to see how to set trace, etc. 
- subexpression profiling
- writing at class level in coordination with tests: for given
  cursor position, find list of tests that cover this branch or
  comes closest
- "static view" of stack when not debugging to quickfixlist
- for dynamic, visual debugging, code needs to run in separate thread
  so we can interact, poke, evaluate expressions, etc. 

- need some serious reloading support 
  - intercept imports
  - intercept class & function definitions
  - intercept references to functions, classes & methods
  - instrument change propagation

- optional repl manager: controls subprocesses so crash doesn't knock out
  server, and server runs independently. need to build basic server first


- snapshot stacks static (traceback.extract_stack) and dynamically?
- hybrid debugging: stack with locals' reprs. 
- keep tag list updated with modules, functions, etc. 



.. _tmux: http://tmux.sourceforge.net
.. _tslime: http://www.vim.org/scripts/script.php?script_id=3023
.. _vim-ipython: https://github.com/ivanov/vim-ipython
.. _ConEmu: http://code.google.com/p/conemu-maximus5
.. _Pathogen: https://github.com/tpope/vim-pathogen
