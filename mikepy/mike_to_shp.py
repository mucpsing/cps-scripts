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

import os
import mikeio

import geopandas as gpd

from mikeio import Mesh, Dfsu

def to_shp(tar:str, output=None) -> str:
    """
    @Description 将dfsu、mesh文件的边界作为面几何的shp导出

    - param tar    :{str}    仅支持dfsu或者mesh结尾的文件
    - param output :{params} 输出名，不需要带后缀

    returns `{str}` 如果成功，则返回shp的绝对路径，否则返回空

    """
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

    # res = to_shp(filename,'bg')
    # if res: print('成功')

    t = Dfsu(filename).read(items=["Current speed"], time_steps=-1)

    print(t)
    print(mikeio.__version__)
    print(t.shape)

    geo = t.to_2d_geometry()
    print(type(geo))
