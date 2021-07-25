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

import os

from core.mikepy import MikeIo
from pathlib import Path


def main(d=r'./'):
    p = Path(d)

    # 遍历目录，找出dfsu文件
    for each in p.glob('*.dfsu'):
        if not each.is_file(): continue
        M.read(str(each.resolve()), item="Current direction", title='流向')
        M.read(str(each.resolve()), item="Current speed", title='流速')

    if M : M.save('./data/result.xls')
    print(M)
    M.clean()


def test(tar = r'./data'):
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
    # main(tar)
    test()
