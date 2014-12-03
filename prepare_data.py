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
import pyhdf.SD as SD
import time

# 数据文件路径
__datadir = sys.argv[1]
# 存放结果路径
__tmpfile = sys.argv[2]

fields_dsname = {
    "nbar_1": "Nadir_Reflectance_Band1",
    "nbar_2": "Nadir_Reflectance_Band2",
    "nbar_3": "Nadir_Reflectance_Band3",
    "nbar_4": "Nadir_Reflectance_Band4",
    "nbar_5": "Nadir_Reflectance_Band5",
    "nbar_6": "Nadir_Reflectance_Band6",
    "nbar_7": "Nadir_Reflectance_Band7",
    "nbar_qc": "BRDF_Albedo_Band_Quality",
    "lai": "Lai_1km",
    "lai_qc": "FparLai_QC",
    "laimod": "Lai_1km",
    "laimod_qc": "FparLai_QC",
    "ndvi": "1 km 16 days NDVI",
    "evi": "1 km 16 days EVI",
    "vi_qc": "1 km 16 days VI Quality",
    "lst_day": "LST_Day_1km",
    "lstday_qc": "QC_Day",
    "lst_night": "LST_Night_1km",
    "lstnight_qc": "QC_Night"
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


nbar_files = get_files("MCD43B4.", "nbar")
nbar_files.sort()
nbarqc_files = get_files("MCD43B2.", "nbar_qc")
nbarqc_files.sort()
lai_files = get_files("MCD15A2.", "lai")
lai_files.sort()
laimod_files = get_files("MOD15A2.", "lai-mod")
laimod_files.sort()
vi_files = get_files("MOD13A2.", "ndvi")
vi_files.sort()
lst_files = get_files("MOD11A2.", "lst")
lst_files.sort()

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
    return ds[line][sample] if ds is not None else ''


def get_now_time():
    return time.strftime("%H:%M:%S", time.localtime(time.time()))


count = 0

# 循环写入
while p1 < len(nbar_files) or p2 < len(lai_files) or p3 < len(laimod_files) or p4 < len(vi_files) or p5 < len(
        lst_files):
    count += 1
    # 选出头指针中最小的日期
    d1 = get_modis_date(nbar_files[p1]) if p1 < len(nbar_files) else 9999999
    d2 = get_modis_date(lai_files[p2]) if p2 < len(lai_files) else 9999999
    d3 = get_modis_date(laimod_files[p3]) if p3 < len(laimod_files) else 9999999
    d4 = get_modis_date(vi_files[p4]) if p4 < len(vi_files) else 9999999
    d5 = get_modis_date(lst_files[p5]) if p5 < len(lst_files) else 9999999
    min_date = min(d1, d2, d3, d4, d5)

    # 读取数据，将读取文件的指针下标+1
    fields_ds = {
        "nbar_1": None,
        "nbar_2": None,
        "nbar_3": None,
        "nbar_4": None,
        "nbar_5": None,
        "nbar_6": None,
        "nbar_7": None,
        "nbar_qc": None,
        "lai": None,
        "lai_qc": None,
        "laimod": None,
        "laimod_qc": None,
        "ndvi": None,
        "evi": None,
        "vi_qc": None,
        "lst_day": None,
        "lstday_qc": None,
        "lst_night": None,
        "lstnight_qc": None
    }

    if d1 == min_date:
        nbar_file = SD.SD(nbar_files[p1])
        fields_ds["nbar_1"] = nbar_file.select(fields_dsname["nbar_1"]).get()
        fields_ds["nbar_2"] = nbar_file.select(fields_dsname["nbar_2"]).get()
        fields_ds["nbar_3"] = nbar_file.select(fields_dsname["nbar_3"]).get()
        fields_ds["nbar_4"] = nbar_file.select(fields_dsname["nbar_4"]).get()
        fields_ds["nbar_5"] = nbar_file.select(fields_dsname["nbar_5"]).get()
        fields_ds["nbar_6"] = nbar_file.select(fields_dsname["nbar_6"]).get()
        fields_ds["nbar_7"] = nbar_file.select(fields_dsname["nbar_7"]).get()

        nbarqc_file = SD.SD(nbarqc_files[p1])
        fields_ds["nbar_qc"] = nbarqc_file.select(fields_dsname["nbar_qc"]).get()

        p1 += 1
    if d2 == min_date:
        lai_file = SD.SD(lai_files[p2])
        fields_ds["lai"] = lai_file.select(fields_dsname["lai"]).get()
        fields_ds["lai_qc"] = lai_file.select(fields_dsname["lai_qc"]).get()

        p2 += 1

    if d3 == min_date:
        laimod_file = SD.SD(laimod_files[p3])
        fields_ds["laimod"] = laimod_file.select(fields_dsname["laimod"]).get()
        fields_ds["laimod_qc"] = laimod_file.select(fields_dsname["laimod_qc"]).get()

        p3 += 1

    if d4 == min_date:
        vi_file = SD.SD(vi_files[p4])
        fields_ds["ndvi"] = vi_file.select(fields_dsname["ndvi"]).get()
        fields_ds["evi"] = vi_file.select(fields_dsname["evi"]).get()
        fields_ds["vi_qc"] = vi_file.select(fields_dsname["vi_qc"]).get()

        p4 += 1

    if d5 == min_date:
        lst_file = SD.SD(lst_files[p5])
        fields_ds["lst_day"] = lst_file.select(fields_dsname["lst_day"]).get()
        fields_ds["lstday_qc"] = lst_file.select(fields_dsname["lstday_qc"]).get()
        fields_ds["lst_night"] = lst_file.select(fields_dsname["lst_night"]).get()
        fields_ds["lstnight_qc"] = lst_file.select(fields_dsname["lstnight_qc"]).get()

        p5 += 1

    # 写入文件记录
    
    print("filecount: {0}, time: {1}".format(count, get_now_time()))
    for line in range(0, 1200):
        for sample in range(0, 1200):
            tmp_data_file.write('"{0}","{1}","{2}","{3}","{4}","{5}","{6}",'
                                '"{7}","{8}","{9}","{10}","{11}","{12}","{13}",'
                                '"{14}","{15}","{16}","{17}","{18}","{19}",'
                                '"{20}","{21}"\n'.format(min_date, line, sample,
                                                         get_ds_value(fields_ds["nbar_1"], line, sample),
                                                         get_ds_value(fields_ds["nbar_2"], line, sample),
                                                         get_ds_value(fields_ds["nbar_3"], line, sample),
                                                         get_ds_value(fields_ds["nbar_4"], line, sample),
                                                         get_ds_value(fields_ds["nbar_5"], line, sample),
                                                         get_ds_value(fields_ds["nbar_6"], line, sample),
                                                         get_ds_value(fields_ds["nbar_7"], line, sample),
                                                         get_ds_value(fields_ds["nbar_qc"], line, sample),
                                                         get_ds_value(fields_ds["lai"], line, sample),
                                                         get_ds_value(fields_ds["lai_qc"], line, sample),
                                                         get_ds_value(fields_ds["laimod"], line, sample),
                                                         get_ds_value(fields_ds["laimod_qc"], line, sample),
                                                         get_ds_value(fields_ds["ndvi"], line, sample),
                                                         get_ds_value(fields_ds["evi"], line, sample),
                                                         get_ds_value(fields_ds["vi_qc"], line, sample),
                                                         get_ds_value(fields_ds["lst_day"], line, sample),
                                                         get_ds_value(fields_ds["lstday_qc"], line, sample),
                                                         get_ds_value(fields_ds["lst_night"], line, sample),
                                                         get_ds_value(fields_ds["lstnight_qc"], line, sample)))

tmp_data_file.close()
