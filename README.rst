Provide easy logging and CloudWatch support by 3th module
*********************************************************

run unittest
============
略

compile doc
===========
sphinx-build docs/source docs/build

packaging
=========
python setup.py sdist

install
=======
Firstly, you must package this project. And then install this project by pip with its .tar.gz package

python -m pip install watcher-0.0.1.dev7.tar.gz

support
=======
Python2.7,Python3.5,Python3.6

example
=======
./example/sample.py