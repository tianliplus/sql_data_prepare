#!/usr/bin/env python3
__author__ = 'tianli'

'''
Table : h25v03

+----+------+------+--------+--------+--------+--------+--------+--------+--------+--------+---------+------+--------+--------+-----------+------+---------+------+--------+
| id | date | line | sample | nbar_1 | nbar_2 | nbar_3 | nbar_4 | nbar_5 | nbar_6 | nbar_7 | nbar_qc | lai  | lai_qc | laimod | laimod_qc | ndvi | ndvi_qc | lst  | lst_qc |
+----+------+------+--------+--------+--------+--------+--------+--------+--------+--------+---------+------+--------+--------+-----------+------+---------+------+--------+
|  1 |    1 |    2 |      3 |   NULL |   NULL |   NULL |   NULL |   NULL |   NULL |   NULL |    NULL | NULL |   NULL |   NULL |      NULL | NULL |    NULL | NULL |   NULL |
+----+------+------+--------+--------+--------+--------+--------+--------+--------+--------+---------+------+--------+--------+-----------+------+---------+------+--------+


"date","line","sample", ... ...
'''

import os.path
import sys

# 数据文件路径
__datadir = sys.argv[1]
# 存放结果路径
__tmpfile = sys.argv[2]

fields_dsname = {
    "nbar_1": "test_1",
    "nbar_2": "test_2"
}

lai_files = list(filter(lambda x: "MCD15A2" in x, os.listdir(os.path.join(__datadir, "lai"))))
print(lai_files)
exit(0)
tmp_data_file = open(__tmpfile, 'w')

def put_item(item):
    tmp_data_file.write("\"{0}\"".format(item))





tmp_data_file.close()