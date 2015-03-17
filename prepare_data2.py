#!/usr/bin/env python3

__author__ = 'tianli'

'''
Table : h08v05

+----+------+------+--------+--------+--------+--------+--------+--------+--------+--------+---------+------+--------+--------+-----------+------+------+-------+---------+-----------+-----------+-------------+
| id | date | line | sample |   ndvi |  vi_qc |
+----+------+------+--------+--------+--------+--------+--------+--------+--------+--------+---------+------+--------+--------+-----------+------+------+-------+---------+-----------+-----------+-------------+
|  1 |    1 |    1 |      1 |   NULL |   NULL |
+----+------+------+--------+--------+--------+--------+--------+--------+--------+--------+---------+------+--------+--------+-----------+------+------+-------+---------+-----------+-----------+-------------+

"date","line","sample", ... ...
'''

import os.path
import sys
import pyhdf.SD as SD
import time

# 数据文件路径
__datadir = sys.argv[1]
# 存放结果路径
__tmpfile = sys.argv[2]

fields_dsname = {
    "ndvi": "1 km 16 days NDVI",
    "vi_qc": "1 km 16 days VI Quality"
}


def get_files(m_name, p_name):
    """
    :param m_name: modis name (i.e. MCD15A2)
    :param p_name: product folder name (i.e. lai)
    :return: a list of files fullpath correspond to the given m_name and p_name
    """
    files_path = os.path.join(__datadir, p_name)
    return list(map(lambda x: os.path.join(files_path, x), filter(lambda x: m_name in x, os.listdir(files_path))))


def get_modis_date(fullname):
    filename = os.path.basename(fullname)
    return int(filename[9:16])


vi_files = get_files("MOD13A2.", "ndvi")
vi_files.sort()


# p1 - p5 分别指向上面5个files数组的下标首位，将文件名中日期位上 *最小* 且 *相等* 的文件读取并写入到一条文件记录当中
p1 = p2 = p3 = p4 = p5 = 0

# 写入的文件
tmp_data_file = open(__tmpfile, 'w')


def put_item(item):
    tmp_data_file.write("\"{0}\"".format(item))


def put_field(ds, line, sample):
    if ds != False:
        print("ds is true")
        put_item(ds[line][sample])
    else:
        print("ds is false")
        put_item("")


def get_ds_value(ds, line, sample):
    return ds[line][sample] if ds is not None else '\\N'


def get_now_time():
    return time.strftime("%H:%M:%S", time.localtime(time.time()))


count = 0

# 循环写入
while p4 < len(vi_files):
    count += 1
    # 选出头指针中最小的日期
    d4 = get_modis_date(vi_files[p4]) if p4 < len(vi_files) else 9999999
    min_date = d4

    # 读取数据，将读取文件的指针下标+1
    fields_ds = {
        "ndvi": None,
        "vi_qc": None
    }

    if d4 == min_date:
        vi_file = SD.SD(vi_files[p4])
        fields_ds["ndvi"] = vi_file.select(fields_dsname["ndvi"]).get()
        fields_ds["vi_qc"] = vi_file.select(fields_dsname["vi_qc"]).get()
        p4 += 1

    # 写入文件记录

    print("filecount: {0}, time: {1}".format(count, get_now_time()))
    for line in range(0, 1200):
        for sample in range(0, 1200):
            tmp_data_file.write('{0}\t{1}\t{2}\t{3}\t{4}\n'.format(min_date, line, sample,
                                                                   get_ds_value(fields_ds["ndvi"], line, sample),
                                                                   get_ds_value(fields_ds["vi_qc"], line, sample)))

tmp_data_file.close()
