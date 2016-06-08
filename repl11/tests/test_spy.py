
import repl11.spy as spy

def test_modname_from_path():
    path = '/foo/bar/baz.py'
    assert spy.modname_from_path(path) == path
    assert spy.modname_from_path('./' + path) == 'foo.bar.baz'
