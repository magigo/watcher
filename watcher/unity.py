# ! /usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function
import subprocess
from subprocess import check_output

try:
    EC2ID = check_output("curl -s http://169.254.169.254/latest/meta-data/instance-id --connect-timeout 1",
                         shell=True).decode('utf8')
except subprocess.CalledProcessError:
    EC2ID = '00000000'
if __name__ == '__main__':
    pass
