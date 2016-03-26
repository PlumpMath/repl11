
from distutils.core import setup

with open('README.rst', 'r') as fd:
    readme = fd.read()

setup(
    name='hrepl',
    version='0.5',
    description='Interactive Python REPL over HTTP',
    author='Marmaduke Woodman',
    author_email='maedoc@mm.st',
    url='http://github.com/maedoc/hrepl',
    packages=['hrepl'],
    long_description=readme
)
