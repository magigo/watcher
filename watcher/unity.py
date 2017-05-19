# ! /usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function
import sys
from subprocess import check_output

if str(sys.platform).startswith('darwin'):
    EC2ID = '00000000'
else:
    EC2ID = check_output(["curl", "-s", 'http://169.254.169.254/latest/meta-data/instance-id']).decode('utf8')

if __name__ == '__main__':
    pass
