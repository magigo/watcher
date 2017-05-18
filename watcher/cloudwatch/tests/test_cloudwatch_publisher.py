# ! /usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function
import unittest
import sys
import os

sys.path.insert(0, os.path.abspath('../../..'))


class TestCloudwatchPublisher(unittest.TestCase):
    def testCloudWatchPublisher(self):
        from watcher.cloudwatch.cloudwatch_publisher import CloudWatchPublisher
        self.assertTrue(True)

    def testHeartBeatPublisher(self):
        from watcher.cloudwatch.cloudwatch_publisher import HeartBeatPublisher
        self.assertTrue(True)

    def testStart(self):
        from watcher.cloudwatch.cloudwatch_publisher import start
        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()