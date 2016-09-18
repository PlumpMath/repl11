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
the exception that existing objects are not updated, which is a bug 
or a feature as you see it.

Using IPython also tends to a decoupling between serious code editing
and interactive testing. With repl11 there is no discontinuity
between the two, as you use your (my) favorite editor (vim) (for the
moment).

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
  updating of modules attributes. There are some module related issues
  to work out.

- auto dedent makes it easier to write & test code in indented blocks, 
  and perhaps in rst as well while writing sphinx documentation.

- logging now handling through http api, client can display as 
  desired, and interpreter can run in background, no terminal requried
  (though it's rather crude ftm).

- start repl directly from vim, no terminal required (`\rb` & `\re`)

- rudimentary jump to source using Python's inspect (`\rd`)

wish list & navel gazing
------------------------

- visual debugging
- line profiling blocks of code (get wrapped in @profiled defs)
- embedding into running application
- open definition, show source, etc.
- repl config : which interpreter, pythonpath, cwd, venv etc. 
- complete available modules
- find any object in running process, filter for specific class,
  poke object, etc.

- cover as much as possible with tests.. 
- monkey patching methods & functions: find class and objects, ... 
- implement js/codemirror & vim clients as demos (?)
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

- asynch execution for long running tasks? Q: how to let user handle it
  should they specify not to wait then check up on status later?
- running different code blocks in different threads or processes?
- debug stack traces backwards, "time traveling debugger", called tardis

- add event loops for other systems like gl, plain qt, wx, bla bla

- python 3 has a new async i/o library which may or may not be interesting
  for a rewrite of the servers, etc. 

- open up a bit the interactions: kernels implement set of apis that mimick
  what usually do at repl, like entering text, eval in namespace, completion
  etc. 

- have a popup window in vim listing status of currently known repls; perhaps
  require some central file that lists these e.g. hostname / time / port / etc

- 


.. _tmux: http://tmux.sourceforge.net
.. _tslime: http://www.vim.org/scripts/script.php?script_id=3023
.. _vim-ipython: https://github.com/ivanov/vim-ipython
.. _ConEmu: http://code.google.com/p/conemu-maximus5
.. _Pathogen: https://github.com/tpope/vim-pathogen
