# -*- coding: utf-8 -*-
#
# @Author: CPS
# @email: 373704015@qq.com
# @Date: 2021-07-24 11:50:02.306507
# @Last Modified by: CPS
# @Last Modified time: 2021-07-24 11:50:02.306507
# @file_path "D:\CPS\MyProject\python\matrix"
# @Filename "main.py"
# @Description: 功能描述
#
from PIL import Image,ImageColor

def test(tar = r'./test/test.png'):
    xy={ 'left_top':[50, 150] }
    Matrix(tar).config(xy=xy, mode='relative').draw().show()

class Matrix(object):
    relative_xy_template = {
        'left_top':[0, 0],
        'right_top':[0, 0],
        'right_down':[0, 0],
        'left_down':[0, 0]
    }

    def __init__(self, img, mode='absolute'):
        self.mode = mode # absolute | relative 相对坐标或者绝对坐标
        self.transform_img = None

        self.xy_list = []
        self.img = Image.open(img).convert('RGBA')
        self.xy_obj = {
            'left_top':[0, 0],
            'right_top':[self.img.width, 0],
            'right_down':[self.img.width, self.img.height],
            'left_down':[0, self.img.height]
        }

    def config(self, xy=None, mode=None):
        if mode:
            self.mode = mode

        if xy:

            self.xy_list = self.convertXY(xy)

        return self

    def result(self):
        return self.transform_img

    def save(self, output):
        self.transform_img.save(output)

    def show(self):
        if self.transform_img : self.transform_img.show()
        return self

    def draw(self):
        # 配置背景矩阵范围
        bg_range = [(0,0), (self.img.width, 0), (self.img.width, self.img.height), (0, self.img.height)]

        # # 拼接参数作为仿射计算函数的入参
        transform = self.PerspectiveTransform(bg_range, self.xy_list)

        self.transform_img = self.img.transform(
            size=self.img.size,
            method=Image.PERSPECTIVE,
            data=transform,
            resample=Image.NEAREST)

        return self


    """
    : Description 将四点坐标转换为数组，然后使用np更好的计算仿射
    :
    : param  self:{type}  {description}
    : param  xy:{type}    {description}
    :
    : returns {} {description}
    :
    """
    def convertXY(self, xy):
        if isinstance(xy, dict):
            if self.mode == 'absolute':
                self.xy_obj.update(xy)
                return [self.xy_obj['left_top'], self.xy_obj['right_top'], self.xy_obj['right_down'], self.xy_obj['left_down']]
            if self.mode == 'relative':
                # 使用更新对象的方式，入参不用每个位置都输入坐标，更自由
                nxy = Matrix.relative_xy_template
                nxy.update(xy)
                return [
                    nxy['left_top'],
                    (self.img.width + nxy['right_top'][0], nxy['right_top'][1]),
                    (self.img.width + nxy['right_down'][0] , self.img.height + nxy['right_down'][1]),
                    (nxy['left_down'][0], self.img.height + nxy['left_down'][1])
                ]

        # 返回测试坐标
        return [[50, 50], [250, 250], [300, 300], [50, 350]]

    """
    : Description 坐标点顺序： [left_top, right_top, right_down, left_down]
    :
    : param  background_xy:{list}  背景原尺寸的四角坐标，[(0, 0), (img_width, 0), (img_width, img_height), (0, img_height)]
    : param  front_xy:{list}       需要仿射的新坐标，    [[95, 134], [95, 134], [195, 209], [195, 209]]
    :
    : returns {narray} 二维数据，每一维带8个元素
    :
    """
    @staticmethod
    def PerspectiveTransform(background_xy, front_xy):
        import numpy as np
        matrix=[]
        for p1, p2 in zip(front_xy, background_xy):
            matrix.append([p1[0], p1[1], 1, 0, 0, 0, -p2[0] * p1[0], -p2[0] * p1[1]])
            matrix.append([0, 0, 0, p1[0], p1[1], 1, -p2[1] * p1[0], -p2[1] * p1[1]])
        A = np.matrix(matrix, dtype=np.float64)
        B = np.array(background_xy).reshape(8)
        res = np.dot(np.linalg.inv(A.T * A) * A.T, B)
        return np.array(res).reshape(8)

if ( __name__ == "__main__"):
    test()
else:
    # 接收参数
    import sys
    all_pamas = sys.argv


