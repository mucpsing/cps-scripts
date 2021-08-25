# -*- coding: utf-8 -*-
#
# @Author: CPS
# @email: 373704015@qq.com
# @Date: 2021-07-19 09:16:56.383902
# @Last Modified by: CPS
# @Last Modified time: 2021-07-19 09:16:56.383902
# @file_path "Z:\CPS\MyProject\mikepy\core"
# @Filename "mikepy.py"
# @Description: 功能描述
#

import time, os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from mikeio import Dfsu,Dfs0,Mesh
from mikeio.spatial import Grid2D

from hashlib import md5
from tempfile import TemporaryFile,TemporaryDirectory
from shutil import copy2

if str(pd.__version__) != '1.3.0':
    print("本插件仅支持 pandas 1.3.0 (否则失去保存xls功能)")
    # exit()

class MikeIo(object):
    def __init__(self):
        self.dfs=None
        self.mesh=None
        self.len=0
        self.currt_file=""

        self.data={} # {'sheet_name':[{'column_name':'xxxxx', 'column_data':'xxxxx', 'file_name':'xxxxx'}]}
        self.file_list = []
        self.tmp_dir = None

    def __len__(self):
        return len(self.file_list)

    def __str__(self):
        return f"当前已处理 {len(self.file_list)} 个文件： {[*self.file_list]}"

    def read_with_xy(self, dirname:str, item:str, setp:int=-1):
        pass

    def read(self, filename, item="", title="", setp=-1, sheet_name:str=""):
        """
        Description 获取指定类型、时间步长的对应数据

        - param  target :{type}   文件名，绝对路径
        - param  item :{string}   需要提取的数据类型|Current_direction|Current_speed|U_velocity|V_velocity|...
        - param  title :{string}  属性最终的列名
        - param  setp :{int}      需要获取的步长，默认是最后一个时间

        returns { narray } {description}

        """
        name,ext = os.path.basename(filename).split('.')
        if ext == 'dfsu':
            # 防止重复读取同一文件
            if self.currt_file != filename:
                try:
                    self.dfsu = Dfsu(filename)
                    self.currt_file = filename
                except Exception:
                    print('tips >>> 请使用英文或数字命名文件，数据提取速度将会大大提升')
                    tmp_file = self.create_tmp_file(filename)
                    self.dfsu = Dfsu(tmp_file)
                    self.currt_file = filename

            if not self.dfsu: return print(f'无法读取文件{filename}')

            # 通过self.dfsu 读取数据
            data = self.get_dfsu_data(item=item, setp=setp)

            # 如果没有指定sheet_name，将以要提取的数据来命名
            if sheet_name == "":
                sheet_name = f'mesh_{len(data)}'

            # 读取 X Y 数据
            if not sheet_name in self.data:
                self.data[sheet_name] = []
                self.get_xy_by_mesh(self.dfsu)

            self.data[sheet_name].append({
                "column_name":f'{title}_{name}',
                "file_name":name,
                "column_data":np.round(data, 3),
            })

            # 记录已处理过的文件
            if not f'{name}.{ext}' in self.file_list:
                self.file_list.append(f'{name}.{ext}')

        return data

    def create_tmp_file(self, filename):
        # 创建临时目录
        if not self.tmp_dir: self.tmp_dir = TemporaryDirectory()

        # 记录当前文件已经被缓存
        name,ext = os.path.basename(filename).split('.')

        # 已 md5 命名临时文件
        md5_name = md5(name.encode('utf8')).hexdigest()
        tmp_file = f'{self.tmp_dir.name}{os.path.sep}{md5_name}.{ext}'

        # 复制文件到临时目录，同时先检查是否已存在临时文件
        if not os.path.exists(tmp_file):
            copy2(filename, tmp_file)

        return tmp_file

    def get_xy_by_xyz(self, xyz_file:str):
        if not os.path.exists(xyz_file): return

        self.xy = pd.read_table

    """
    : Description 获取文件的X，Y，
    :
    : returns { narray } {description}
    :
    """
    def get_xy_by_mesh(self, dfs):
        # 实例化网格
        # 获取网格内的数据[col1, col2, col3,...]
        if not dfs:
            self.mesh = Mesh(self.currt_file)
            xyz = self.mesh.element_coordinates
        else:
            xyz = dfs.element_coordinates

        # 以网格数量为基础创建一个对象，收集同一网格的所有数据
        sheet_name = f'mesh_{len(xyz)}'
        data = pd.DataFrame(xyz)
        self.data[sheet_name].append({'column_name':'x','column_data': data[0]})# x 为第一列数据
        self.data[sheet_name].append({'column_name':'y','column_data': data[1]})# y 为第二项数据

        return data


    """
    : Description 根据后缀名，导出excel文件，支持 shp/excel/xyz
    :
    : param  self:{type}        {description}
    : param  filename:{string}  {description}
    :
    : returns {} {description}
    :
    """
    def save(self, filename='./output.xls'):
        name,ext = os.path.basename(filename).split('.')

        if ext == 'xls' or ext == "xlsx":
            self.save_excel(filename)

        return self

    def clean(self):
        try:
            self.tmp_dir.cleanup()
        except :
            print('^.^ done！')

    """
    : Description 导出excel文件，sheet_name会根据网格网点决定，同一网格数据会存在同一sheet内
    :
    : param  self:{type}      {description}
    : param  filename:{type}  支持保存为【.xls】或者【.xlsx】文件
    :
    : returns {} {description}
    :
    """
    def save_excel(self, filename):
        name,ext = os.path.basename(filename).split('.')

        d = os.path.dirname(filename)

        writer = pd.ExcelWriter(f'{d}{os.path.sep}{name}_{int(time.time())}.{ext}')

        for sheet_name, data in self.data.items():
            # 生成数据对象
            sheet_data = { each_column['column_name']:each_column['column_data'] for each_column in data if each_column}

            # 根据数据的key 保证相同网格数据保存在同一sheet_name
            pd.DataFrame(sheet_data).to_excel(writer, index=False, sheet_name=sheet_name)

        writer.save()

    # 读取dfsu文件
    def get_dfsu_data(self, item, setp):
        # 防重读取
        res = None

        if item.lower() =="current direction":
            res = self.get_dfsu_direction(setp)[:]

        elif item.lower() =="current speed":
            res = self.get_dfsu_speed(setp)[:]

        else:
            res = self.dfsu.read([item])[0][setp][:]

        return self.check_data(res)

    # 获取dfsu文件的流速数据
    # return {narray}
    def get_dfsu_speed(self, setp):
        try:
            u,v = self.dfsu.read(['U velocity','V velocity'])
            u = u[setp]
            v = v[setp]
            return np.sqrt(u**2 + v**2)
        except KeyError:
            return self.dfsu.read(['Current speed'])[0]

    # 获取dfsu文件的流速数据
    # return {narray}
    def get_dfsu_direction(self, setp):
        try:
            u,v = self.dfsu.read(['U velocity','V velocity'])
            u = u[setp]
            v = v[setp]
            return np.mod(90 -np.rad2deg(np.arctan2(v,u)), 360)
        except KeyError:
            return self.dfsu.read(['Current direction'])[0] * 180/3.14


    """
    : Description 计算两个数据的差值，流速差值、水位差值等计算
    :
    : param  self:{type}     {description}
    : param  target1:{type}  {description}
    : param  target2:{type}  {description}
    : param  title:{string}  {description}
    :
    : returns {} {description}
    :
    """
    def sub(self, target1, target2, title=""):
        """
        Description {description}

        - param self    :{params} {description}1
        - param target1 :{params} {description}
        - param target2 :{params} {description}
        - param title   :{string} {description}

        returns `{}` {description}

        """
        # sub = np.round(self.result[target1] - self.result[target2], 3)
        sub = []
        return sub

    def check_data(self, data, fix=True, tip=True):
        """
        Description {description}

        - param self :{params} {description}
        - param data :{params} {description}
        - param fix  :{bool}   是否修复为0
        - param tip  :{bool}   是否打印出提示信息

        returns `{}` {description}

        """
        name, ext = os.path.basename(self.currt_file).split('.')
        for index, each in enumerate(data):
            if not np.isnan(each): continue

            if fix : data[index] = 0

            # if tip : print(f"warning >>> file：{name}.{ext}，posistion：<{ index + 1 }> has unknown value")
            if tip : print(f"警告！ >>> 文件：{name}.{ext}，位置：<{ index + 1 }> 的数据为空值")

        return data

if ( __name__ == "__main__"):
    pass
