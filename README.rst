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

why not just ipython?
---------------------

Using ipython as an IDE has its limits: making coordinated changes 
across modules requires redundant reloading of all modules and perhaps
dependencies thereof. Without a robust deep, automatic reloading
facility, this is problematic. In repl11, evaluation occurs in the 
module's namespace directly, so changes take effect immediately, with
the exception that existing objects are not updated.

Using IPython also forces a decoupling between serious code editing
and interactive testing. With repl11 there is no discontinuity
between the two.

For the moment, debugging is the part where repl11 is not so good: 
stack traces are mapped to Vim's quickfixlist but that's all, and 
one has to pass to (i)pdb or IDLE to get better support.

recently implemented
--------------------

- standard library only, only requires http server and urllib
  for RPC.

- tracebacks are converted into Vim's quickfixlist for both installed
  modules and scratch files, making it easy to jump to relevant code

- exec performed on a per-file module basis: where a filename has a 
  mapping to a Python module (for the running interpreter), the existing
  module is used, otherwise a fake module is created. This allows live
  updating of modules attributes

- auto dedent makes it easier to write & test code in indented blocks

- logging now handling through http api, client can display as 
  desired, and interpreter can run in background, no terminal requried

- start repl directly from vim, no terminal required (`\rb` & `\re`)

- rudimentary jump to source using Python's inspect (`\rd`)

missing
-------

- visual debugging
- line profiling blocks of code (get wrapped in @profiled defs)
- embedding into running application
- open definition, show source, etc.
- repl config : which interpreter, pythonpath, cwd, venv etc. 
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

- use fork to quickly boot new repls with scipy/numpy deps already imported

- snapshot stacks static (traceback.extract_stack) and dynamically?
- hybrid debugging: stack with locals' reprs. 
- keep tag list updated with modules, functions, etc. 

- asynch execution for long running tasks?




.. _tmux: http://tmux.sourceforge.net
.. _tslime: http://www.vim.org/scripts/script.php?script_id=3023
.. _vim-ipython: https://github.com/ivanov/vim-ipython
.. _ConEmu: http://code.google.com/p/conemu-maximus5
.. _Pathogen: https://github.com/tpope/vim-pathogen
