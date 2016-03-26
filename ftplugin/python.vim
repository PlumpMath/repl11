
" TODO need to send current buffer name/file so that quickfixing
" errors can take advantage
function! HREPLSend(target, message)
python<<EOF
import vim
from urllib import urlopen, urlencode
target  = vim.eval('a:target')
message = vim.eval('a:message')
message = urlencode({'message': message})
req = urlopen('http://127.0.0.1:8080/{0}?{1}'.format(target, message))
resp = req.read()
if resp:
  if 'Traceback (most recent call last)' in resp:
      print resp
      vim.command("let g:hreplqfl = []")
      lines = resp.split('\n')[2:-1]
      trace, exc = lines[:-1][::-1], lines[-1]
      qf = []
      for i, tr in enumerate(trace):
          if i%2==0:
              qf.append({'text': tr.strip()})
          else:
              f, l, m = [s.split(' ')[1] for s in tr.strip().split(', ')]
              qf[-1]['filename'] = eval(f)
              qf[-1]['lnum'] = l
      for i, qfi in enumerate(qf):
          qfis = ', '.join('%r: %r' % (k, v) for k, v in qfi.items())
          vim.command('call add(g:hreplqfl, {%s})' % (qfis, ))
      vim.command('call setqflist(g:hreplqfl)')
      print exc
  else:
      print resp
EOF
endfunction


function! HREPLDescribeCword()
    call HREPLSend('describe', expand("<cword>"))
endfunction

function! HREPLComplete(findstart, base)
    if a:findstart
        " borrowed from ivanov/vim-ipython
        let line = getline('.')
        let start = col('.') - 1
        while start > 0 && line[start-1] =~ '\k\|\.' " keyword or dot
            let start -= 1
        endwhile
        return start
    else
python<<EOF
import vim
from urllib import urlopen, urlencode
message = urlencode({'message': vim.eval('a:base')})
req = urlopen('http://127.0.0.1:8080/complete?{0}'.format(message))
vim.command('let b:hrepl_resp = %r' % (req.read().strip(), ))
EOF
return split(b:hrepl_resp, ',')
    endif
endfunction

setl completefunc=HREPLComplete

function! HREPLCurrentObjectName()
    " borrowed from ivanov/vim-ipython
    let line = getline('.')
    let start = col('.') - 1
    let endl = col('.')
    while start > 0 && line[start-1] =~ '\k\|\.' " keyword or dot
        let start -= 1
    endwhile
    while endl < strlen(line) && line[endl] =~ '\k\|\.'
        let endl += 1
    endwhile
    return strpart(line, start, endl)
endfunction

function!HREPLHelp()
    let obj = HREPLCurrentObjectName()
    call HREPLSend('ex', 'help(' . obj . ')')
endfunction

function!HREPLSource()
    let obj = HREPLCurrentObjectName()
    call HREPLSend('ex', 'import inspect; print inspect.getsource(' . obj . ')')
endfunction

vmap <F9> "ry:call HREPLSend('ex', @r)<CR>
map K :call HREPLHelp()<CR>
map <c-K> :call HREPLSource()<CR>

