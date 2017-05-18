# ! /usr/bin/python
# -*- coding: utf-8 -*-

"""
这个模块负责处理CloudWatch数据点的发布

#. 自动的发布心跳
#. 发布自定义指标
"""
from future import standard_library
standard_library.install_aliases()
from time import sleep
from datetime import datetime
from subprocess import getstatusoutput
from collections import namedtuple
from subprocess import check_output
import sys

from boto.ec2 import cloudwatch
import pytz

tz = pytz.timezone('Asia/Shanghai')
utc_tz = pytz.utc
cst_time_now = datetime.now(tz)


class CloudWatchPublisher(object):
    """
    CloudWatch数据点发布器，实现了向某一个命名空间发送任意指标，任意维度的数据点
    """

    def __init__(self, namespace):
        """
        构造函数会自动获取其所运行的服务器的'实例-ID'，如果是本地运行默认是'00000000'

        :param namespace: str, 命名空间，应该是公司AWS账号全局内唯一的命名，默认取项目入口文件的命名

        :return: None
        """
        self.cw_conn = cloudwatch.connect_to_region('cn-north-1')
        if str(sys.platform).startswith('darwin'):
            self.ec2_id = '00000000'
        else:
            self.ec2_id = check_output(["curl", "-s", 'http://169.254.169.254/latest/meta-data/instance-id'])
        self.namespace = namespace

    def publish_data_point(self, matrix_name, value, unit=None, dimensions=None):
        """
        向CloudWatch发布数据点

        :param matrix_name: str, 指标名

        :param value: int/float/long, 数据点的值

        :param unit: str, 单位, 可用的值: Seconds |
            Microseconds | Milliseconds | Bytes | Kilobytes |
            Megabytes | Gigabytes | Terabytes | Bits | Kilobits |
            Megabits | Gigabits | Terabits | Percent | Count |
            Bytes/Second | Kilobytes/Second | Megabytes/Second |
            Gigabytes/Second | Terabytes/Second | Bits/Second |
            Kilobits/Second | Megabits/Second | Gigabits/Second |
            Terabits/Second | Count/Second | None

        :param dimensions: dict{str: str}, 维度数据, 字典的key为'维度名', 字典的value是'维度值'

        :return: 不重要
        """
        resp = self.cw_conn.put_metric_data(namespace=self.namespace, name=matrix_name, value=value, unit=unit,
                                            dimensions=dimensions)
        return resp


class HeartBeatPublisher(CloudWatchPublisher):
    """
    信条信息发布器, 本类会取得磁盘剩余空间作为信条信息发布

    * 数据指标为'Disk Remain'
    * 数据维度包括'Instance ID'和'Disk'
    * 数据点是磁盘剩余的百分比, 单位'Percent'
    """

    def __init__(self, namespace):
        super(HeartBeatPublisher, self).__init__(namespace)
        self.DiskInfo = namedtuple('DiskInfo', 'Filesystem Size Used Avail Used_percentage Mounted_on')

    def _get_disk_info(self):
        """
        获取磁盘剩余容量信息

        :return: list, 每个磁盘分区剩余容量的列表
        """
        status, output = getstatusoutput("df -h")
        disk_info_list = []
        if not status:
            lines = output.split('\n')
            for line in lines[1:]:
                line_sp = line.split()
                line_sp = line_sp[:5] + [line_sp[-1]]
                if '/dev/' in line_sp[0]:
                    disk_info_list.append(self.DiskInfo(*line_sp))
        return disk_info_list

    def _publish_disk_info(self, disk_info):
        """
        发布磁盘剩余量的信息作为心跳信息

        :param disk_info: object[DiskInfo], 磁盘剩余信息的具名元组对象

        :return: 不重要
        """
        data = {"Instance ID": self.ec2_id, "Disk": disk_info.Filesystem}
        if disk_info.Used_percentage.endswith('%'):
            value = int(disk_info.Used_percentage[:-1])
        else:
            raise self.NoDiskInfoError()
        resp = self.publish_data_point('Disk Remain', value, 'Percent', data)
        return resp

    def publish_heartbeat(self):
        """
        对外暴露的接口, 发布心跳信息

        :return: None
        """
        for disk_info in self._get_disk_info():
            self._publish_disk_info(disk_info)

    class NoDiskInfoError(Exception):
        pass


def start():
    """
    启动一个后台线程发送心跳数据

    :return:
    """
    import threading
    import sys

    def main(name):
        cwp.namespace = name
        while True:
            cwp.publish_heartbeat()
            sleep(60)

    cwp = HeartBeatPublisher('ServiceHeartBeat')
    app_name = sys.argv[0].split('/')[-1].split('.', 1)[0]

    threads = []
    t1 = threading.Thread(target=main, args=(app_name,))
    threads.append(t1)

    for t in threads:
        t.setDaemon(True)
        t.start()
