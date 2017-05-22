# ! /usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function
import os
import logging
import logging.handlers
import time

from watcher import CloudWatchLogHandler

LOG = logging.getLogger('Test')
LOG.setLevel(logging.DEBUG)
fh = logging.handlers.RotatingFileHandler(
    '{}/test_{}.log'.format('/tmp', os.getpid()), maxBytes=100000000, backupCount=5, encoding='utf8')
fh.setFormatter(
    logging.Formatter(
        '[%(asctime)s] {} [%(processName)s] %(filename)s [line:%(lineno)d] %(levelname)s %(message)s'.format(
            '00000000')))
LOG.addHandler(fh)
LOG.addHandler(CloudWatchLogHandler())

LOG.info('start')

for x in range(100):
    LOG.info('log num: {}'.format(x))
    time.sleep(1)

if __name__ == '__main__':
    pass
