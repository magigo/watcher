# ! /usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function
import sys
from watcher.cloudwatch.cloudwatch_publisher import start
from watcher.logging.easy_logging import CloudWatchLogHandler

app_name = sys.argv[0].split('/')[-1].split('.', 1)[0]

start(app_name)
if __name__ == '__main__':
    pass
