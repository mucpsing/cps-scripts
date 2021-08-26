# -*- coding: utf-8 -*-
#
# @Author: CPS
# @email: 373704015@qq.com
# @Date: 2021-07-17 12:01:50.534088
# @Last Modified by: CPS
# @Last Modified time: 2021-07-17 12:01:50.534088
# @file_path "D:\CPS\MyProject\test"
# @Filename "main.py"
# @Description: 功能描述 - 读取 dfsu文件，输出指定的数据为xls
#

from core.mikepy import MikeIo
from pathlib import Path


def main(d:str=r'./') -> None:
    p = Path(d)

    # 遍历目录，找出dfsu文件
    for each in p.glob('*.dfsu'):
        if not each.is_file(): continue
        M.read(str(each.resolve()), item="Current direction", title='流向')
        M.read(str(each.resolve()), item="Current speed", title='流速')

    if M : M.save('./data/result.xls')
    print(M)
    M.clean()


def test(tar:str = r'./data') -> None:
    global M
    p = Path(tar)
    for each in p.glob('*.dfsu'):
        if not each.is_file(): continue
        M.read(str(each.resolve()), item="Current direction", title='流向')
        M.read(str(each.resolve()), item="Current speed", title='流速')


    if M : M.save('./data/result.xls')
    print(M)
    M.clean()
    
M=None
M=MikeIo()
if ( __name__ == "__main__"):
    from os import path

    BE20 = './data/BE-20.xyz'
    north200 = './data/sg-north-20.xyz'
    soutu200 = './data/south200.xyz'

    xyz = "./data/提取范围.xyz"

    tar1 = "./data/AF100.dfsu"
    tar2 = "./data/north100.dfsu"



    M.set_xy(xyz)
    # M.read(tar1, item="Current speed", column_name='AF100', sheet_name='s1')
    # M.read(tar2, item="Current speed", column_name='north100', sheet_name='s1')
    # M.sub('north100','AF100', sheet_name="s1", column_name="north100_C")
    # M.save('./data/test.xls')

    sheet_name = "s1"
    # item = "Current direction"

    item = "Current speed"
    p = Path('./data/')
    for each in p.glob('*.dfsu'):
        column_name,ext = path.basename(each.resolve()).split('.')
        M.read(each.resolve(), item="Current speed", column_name=column_name, sheet_name=sheet_name)
        # M.read(each.resolve(), item="Current direction", column_name=column_name, sheet_name=sheet_name)

    M.sub('AF20','BE-20', sheet_name=sheet_name, column_name="C20")
    M.sub('sg-north-20','BE-20', sheet_name=sheet_name, column_name="north_C20")
    M.sub('sg-south-20','BE-20', sheet_name=sheet_name, column_name="south_C20")

    M.sub('BE-YX50','AF50', sheet_name=sheet_name, column_name="C50")
    M.sub('north50','AF50', sheet_name=sheet_name, column_name="north_C50")
    M.sub('sg-south-50','AF50', sheet_name=sheet_name, column_name="south_C50")

    M.sub('be100','AF100', sheet_name=sheet_name, column_name="C100")
    M.sub('north100','AF100', sheet_name=sheet_name, column_name="north_C100")
    M.sub('sg-south-100','AF100', sheet_name=sheet_name, column_name="south_C100")

    M.sub('BE-200','AF200', sheet_name=sheet_name, column_name="C200")
    M.sub('north200','AF200', sheet_name=sheet_name, column_name="north_C200")
    M.sub('south200','AF200', sheet_name=sheet_name, column_name="south_C200")

    M.save(f'./data/{item}.xls')
    M.clean()
