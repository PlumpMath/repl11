
from repl11 import ns

reload(ns)

def test_idem():
    n = ns.Namespaces()
    assert n['foo'] is n['foo']
    assert n['bar'] is not n['foo']
    assert n['bar'] is n['bar']

def test_persist():
    n = ns.Namespaces()
    foo = n['foo']
    exec "x = 3" in foo
    del foo
    assert n['foo']['x'] == 3
