
import ast
import pprint

from repl11 import code

src1 = """
class Foo:
    x = 3

    y = 4
"""

src2 = """
    def foo():
        x = 3

        y = 4
"""

src2_correct = """
def foo():
    x = 3

    y = 4
"""

def test_dedent():
    assert src1 == code.dedent(src1)
    assert src2_correct == code.dedent(src2)

def test_assign_last():
    ns = {}
    key = '__'
    src = "print 'foo'\n4 + 3"
    mod = ast.parse(src, 'exec')
    mod, assigned = code.assign_last(mod, key=key)
    assert assigned == True
    mod = ast.fix_missing_locations(mod)
    co = compile(mod, 'none', 'exec')
    exec co in ns
    assert ns[key] == 7
    
def test_io_capture():
    with code.IOCapture() as io:
        assert io.active
        print 'ok'
    assert not io.active
    assert io.contents == 'ok\n'

def do_code(src, ns={}):
    c = code.Code(src)
    ns = ns or {}
    ret = c(ns)
    return c, ns, ret

def test_code_stmt():
    c, ns, ret = do_code("import ast")
    assert ret['status'] == 'ok'
    assert ret['result'] is None
    assert 'ast' in ns and ns['ast'] == ast

def test_code_expr():
    c, ns, ret = do_code("3 + 4")
    assert ret['status'] == 'ok'
    assert ret['result'] == 7

def test_code_stmt_expr():
    c, ns, ret = do_code("import ast\n3 + 4")
    assert ret['status'] == 'ok'
    assert ret['result'] == 7
    assert 'ast' in ns and ns['ast'] == ast

def test_code_fail_syntax():
    c, ns, ret = do_code("import")
    assert ret['status'] == 'fail'
    assert isinstance(ret['result'], SyntaxError)

src_tb_test = """
def f1():
    f2()

def f2():
    f3()

def f3():
    f4()

def f4():
    f5()

def f5():
    f6()

def f6():
    1/0

f1()
"""

# TODO setup tb across several files w/ class
def test_code_fail_tb():
    l1 = 78
    nl = len(src_tb_test.split('\n'))
    ns, c = {}, code.Code(src_tb_test, __file__, l1)
    ret = c(ns)
    assert ret['status'] == 'fail'
    assert isinstance(ret['result'], ZeroDivisionError)
    tb = ret['traceback']
    assert len(tb) > 0
    # should start in Code.__call__
    assert tb[0][0].endswith('repl11/code.py')
    assert tb[0][2].endswith('__call__')
    # continue with f1() in src
    assert tb[1][1] == l1 + nl - 1
    assert tb[1][3] == 'f1()'
    # chain of calls
    for i in '12345':
        fname = 'f%s' % i
        f = ns[fname]
        lfi = f.func_code.co_firstlineno
        ip1 = int(i) + 1
        assert tb[ip1][1] == lfi + 1
        assert tb[ip1][2] == fname
        assert tb[ip1][3] == 'f%d()' % ip1
    fname = 'f6'
    f = ns[fname]
    lfi = f.func_code.co_firstlineno
    assert tb[7][1] == lfi + 1
    assert tb[7][2] == fname
    assert tb[7][3] == '1/0'


