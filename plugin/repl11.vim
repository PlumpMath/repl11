
" TODO need to send current buffer name/file so that quickfixing
" errors can take advantage
function! R11Send(target, message)
python<<EOF
import vim, json, urllib
target  = vim.eval('a:target')
message = vim.eval('a:message')
row, col = vim.current.window.cursor
pars = {'message': message
       ,'filename': vim.eval("expand('%:p')")
       ,'lineno': row
       }
message = urllib.urlencode(pars)
req = urllib.urlopen('http://127.0.0.1:8080/{0}?{1}'.format(target, message))
resp = json.loads(req.read())
if resp['status'] in ('ok', 'fail'):
    out = resp['out'].strip()
    res = resp['result']
    if res != 'None':
        if out:
            out += '\n'
        out += res
    if len(out) == 0:
        out = resp['status']
    vim.vars['r11out'] = out
    #vim.command('let g:r11out = %r' % (out,))
    if resp['status'] == 'fail':
	qfl = []
        for filename, lineno, context, text in resp['traceback']:
	    if filename.endswith('repl11/code.py'):
		continue
	    qfl.append({
	        'text'     : text or '',
	        'filename' : filename,
	        'lnum'     : lineno
	    })
        vim.vars['r11qfl'] = vim.List(qfl)
        vim.command('call setqflist(g:r11qfl)')
else:
    print 'unknown response status', resp['status']
EOF
endfunction

function! R11DescribeCword()
    call R11Send('describe', expand("<cword>"))
endfunction

function! R11Complete(findstart, base)
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
message = urlencode(
    {'message': vim.eval('a:base')
    ,'filename': vim.eval("expand('%:p')") # to know which namespace
    })
req = urlopen('http://127.0.0.1:8080/complete?{0}'.format(message))
vim.command('let b:hrepl_resp = %r' % (req.read().strip(), ))
EOF
return split(b:hrepl_resp, ',')
    endif
endfunction

setl completefunc=R11Complete

function! R11CurrentObjectName()
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

function!R11Help()
    let obj = R11CurrentObjectName()
    call R11Send('ex', 'help(' . obj . ')')
endfunction

function!R11Source()
    let obj = R11CurrentObjectName()
    call R11Send('ex', 'import inspect; print inspect.getsource(' . obj . ')')
endfunction


map <c-p> :echo g:r11out<CR>

vmap <c-s> "ry:call R11Send('ex', @r)<cr>
nmap <c-s> mtvip<c-s>`t<c-p>
imap <c-s> <esc><c-s>

map K :call R11Help()<cr><c-p>
map <c-k> :call R11Source()<cr><c-p>
"map <c-w> :call R11Send('describe', 'whos')<cr><c-p>
map <c-j> :call R11DescribeCword()<cr><c-p>


"map <F5> :w<CR>:call R11Send('ex', 'execfile("' . expand('%') . '", globals())')

