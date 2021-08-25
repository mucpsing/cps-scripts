# -*- coding: utf-8 -*-
#
# @Author: CPS
# @email: 373704015@qq.com
# @Date: 2021-08-24 15:46:39.362548
# @Last Modified by: CPS
# @Last Modified time: 2021-08-24 15:46:39.362548
# @file_path "Z:\CPS\MyProject\python-tools\mikepy"
# @Filename "test.py"
# @Description: 功能描述
#

import time, os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import geopandas as gpd
from pykrige import OrdinaryKriging

from mikeio import Dfsu,Dfs0,Mesh
from mikeio.spatial import Grid2D

from hashlib import md5
from tempfile import TemporaryFile,TemporaryDirectory
from shutil import copy2

from scipy.interpolate import griddata
from math import radians, sin, cos, asin, sqrt

# print(out)
def dfsu_to_shp(filename, item:str="", setp:int=-1, output:str=""):
    if output == "":
        name,ext = os.path.splitext(os.path.basename(filename))
        dirname = os.path.dirname(os.path.realpath(filename))
        output = os.path.join(dirname,f'{name}.shp')

    dfsu = Dfsu(filename)
    data = dfsu.read()

    # 指定需要提取的数据
    item_data = data[item][setp]
    item_dataframe = pd.DataFrame({'sp': item_data})

    shp = dfsu.to_shapely()
    poly_list = [e for e in shp]

    gdf = gpd.GeoDataFrame(item_dataframe, geometry=poly_list)
    gdf.to_file(output)


def get_data_by_xy(x, y, points, data, method='cubic'):
    # 根据 x，y 生成一个矩阵容器
    xi,yi = np.meshgrid(x, y)

    # cubic 插值
    interpolate_res = griddata(points, data, (xi,yi), method=method)

    # 获取对角线索引
    index = list(range(len(x)))

    # 获取对角线数据
    res = pd.DataFrame(cubic_z).values[index,index]

    return  res

def dict_to_excel(outname:str, data:dict):
    """
    Description {description}

    - param outname :{str}    {description}
    - param data    :{dict}   {description}

    ```python
    {
        # key对应sheet名，内容数组对应列数据
        "sheet_name1":["xxx","xxx",...],
        "sheet_name2":["xxx","xxx",...],
        "sheet_name3":["xxx","xxx",...]
    }

    ```
    returns `{}` {description}
    """
    writer = pd.ExcelWriter(outname)

    for sheet_name,val in data.items:
        pd.DataFrame(data[sheet_name]).to_excel(writer, index=False, sheet_name=sheet_name)

    writer.save()


filename = r'./data/BE-20.dfsu'

# 读取文件
dfsu = Dfsu(filename)

# 获取坐标
coordinates = dfsu.element_coordinates

X = coordinates[:,0]
Y = coordinates[:,1]
points = coordinates[:,0:2]
# print("points: ", points[0])


# 提取数据
data = dfsu.read()
# print(data)
item_data = data['Current speed'][-1]
item_data = np.round(item_data, 3)
print("item_data: ", item_data)

for index, each in enumerate(item_data):
    if np.isnan(each):
        item_data[index] = 0
        print(index)


# print("item_data: ", item_data.max())
# print("item_data: ", item_data.min())
# print("item_data: ", len(item_data))

# 初始化提取范围
xyz = pd.read_table('./data/BE-20.xyz', header=None, sep='\s+')
# x = np.linspace(xyz[0].min(), xyz[0].max(), 400)
# y = np.linspace(xyz[1].min(), xyz[1].max(), 400)

# 获取对角线索引
index = list(range(len(xyz)))
# print("index: ", len(index))

# numcols, numrows = 200, 200 # 200个步长
# xi = np.linspace(X.min(), X.max(), numcols)
# yi = np.linspace(Y.min(), Y.max(), numrows)
# xi,yi = np.meshgrid(xi,yi)

# cubic 插值

xi,yi = np.meshgrid(xyz[0], xyz[1])
cubic_z = griddata(points, item_data, (xi,yi), method='cubic')
cubic_z = pd.DataFrame(cubic_z).values[index,index]
print(cubic_z)

# item_data.dtype = 'float32'
# print("item_data: ", item_data.dtype)
# print(len(item_data))
# print(len(X))

# 科里金
# Kriging = OrdinaryKriging(X, Y, item_data, variogram_model='gaussian', nlags=6)
# Kriging_z, ss = Kriging.execute('grid', x, y)
# Kriging_z = pd.DataFrame(Kriging_z).values[index,index]
# print("Kriging_z: ", Kriging_z)



# print(v)
# l=[]
# for each in range(len(v)):
#     l.append(res[each:1][each])
# print(l)

nearest_z = griddata(points, item_data, (xi,yi), method='nearest')
nearest_z = pd.DataFrame(nearest_z).values[index,index]
print("nearest_z: ", nearest_z)

# print("nearest_z: ", nearest_z.T.max())
# print("nearest_z: ", nearest_z.T.min())


linear_z = griddata(points, item_data, (xi,yi), method='linear')
linear_z = pd.DataFrame(linear_z).values[index,index]
print("linear_z: ", linear_z)

# print("linear_z: ", linear_z.T.max())
# print("linear_z: ", linear_z.T.min())


# print("grid_z: ", len(grid_z))
# print("grid_z: ", grid_z.max())
# print("grid_z: ", grid_z.min())

# output = {
#     "x":xyz[0],
#     "y":xyz[1],
#     "cubic_z":cubic_z,
#     "Kriging_z":Kriging_z,
# }


# 输出
# writer = pd.ExcelWriter('./data/output.xlsx')

# pd.DataFrame(output).to_excel(writer, index=False, sheet_name="test")
# pd.DataFrame(cubic_z).to_excel(writer, index=False, sheet_name="cubic_z")
# pd.DataFrame(nearest_z).to_excel(writer, index=False, sheet_name="nearest_z")
# pd.DataFrame(linear_z).to_excel(writer, index=False, sheet_name="linear_z")
# pd.DataFrame(cubic_z.T).to_excel(writer, index=False, sheet_name="cubic_z.T")
# pd.DataFrame(nearest_z.T).to_excel(writer, index=False, sheet_name="nearest_z.T")
# pd.DataFrame(linear_z.T).to_excel(writer, index=False, sheet_name="linear_z.T")
#
# writer.save()

# contour_levels=np.arange(0.02)
# cn = plt.contour(xi, yi, grid_z, levels=contour_levels)
# plt.show()


# print("values: ", len(values))
# print("points: ", points)
