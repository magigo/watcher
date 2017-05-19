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
.. code-block:: python
    :linenos:
    :emphasize-lines: 3,5

    from watcher import CloudWatchLogHandler

    LOG = logging.getLogger('Spider')
    LOG.setLevel(logging.DEBUG)
    fh = logging.handlers.RotatingFileHandler(
        '{}/kw_ads_{}.log'.format('/mnt', os.getpid()), maxBytes=100000000, backupCount=5, encoding='utf8')
    fh.setFormatter(
        logging.Formatter(
            '[%(asctime)s] {} [%(processName)s] %(filename)s [line:%(lineno)d] %(levelname)s %(message)s'.format('00000000')))
    LOG.addHandler(fh)
    LOG.addHandler(CloudWatchLogHandler())


    LOG.info('start')
