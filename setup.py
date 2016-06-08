
from distutils.core import setup

with open('README.rst', 'r') as fd:
    readme = fd.read()

setup(
    name='repl11',
    version='0.5',
    description='Advanced Python REPL over HTTP',
    author='Marmaduke Woodman',
    author_email='maedoc@mm.st',
    url='http://github.com/maedoc/repl11',
    packages=['repl11'],
    long_description=readme
)
