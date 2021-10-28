# -*- coding: utf-8 -*-
#
# @Author: CPS
# @email: 373704015@qq.com
# @Date:
# @Last Modified by: CPS
# @Last Modified time: 2021-10-28 23:50:31.856789
# @file_path "D:\CPS\MyProject\python-tools\mikepy"
# @Filename "mesh_to_shp.py"
# @Description: 功能描述
#
import geopandas as gpd
import os

from mikeio import Mesh, Dfsu


def to_shp(tar:str, output=None) -> str:
    try:
        if not os.path.exists(tar):raise FileExistsError('文件不存在')

        if tar.endswith('.dfsu'):
            dfs = Dfsu(tar)
        elif tar.endswith('.mesh'):
            dfs = Mesh(tar)

        if not dfs:return ""

        name,ext = os.path.basename(tar).split('.')
        base_path = os.path.abspath(os.path.dirname(tar))

        if output:name = output
        out_name = os.path.join(base_path, f'{name}.shp')

        shp = dfs.to_shapely()
        buffer = shp.buffer(0)

        gdf = gpd.GeoSeries([buffer])
        gdf.to_file(out_name)
        return out_name

    except Exception as e:
        print(f'发生错误了: {e}')
        return ""


if ( __name__ == "__main__"):
    filename = r'./test/10%-af.dfsu'
    res = to_shp(filename,'bg')

    if res: print('成功')
