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

def test():
    # print(ImageColor.getrgb('#00000000'))
    tar = r'./test/test.png'
    img = Image.open(tar)
    # img.resize((img.width*2,img.height*2), Image.ANTIALIAS).save(f'./test_ANTIALIAS.png')
    # img.resize((img.width*2,img.height*2), Image.BILINEAR).save(f'./test_BILINEAR.png')
    # img.resize((img.width*2,img.height*2), Image.BICUBIC).save(f'./test_BICUBIC.png')
    # img.resize((img.width*2,img.height*2), Image.NEAREST).save(f'./test_NEAREST.png')
    # img.resize((img.width*2,img.height*2), Image.LANCZOS).save(f'./test_LANCZOS.png')

    M = Matrix()
    res = M.draw(tar,{
        'left_top':[150, 150],
        'right_top':[img.width, 0],
        'right_down':[img.width-150, img.height-150],
        'left_down':[0, img.height-99]
        })

    res.show()


class Matrix(object):
    def __init__(self, mode='absolute'):
        self.img = None
        self.mode = mode # absolute | relative 相对坐标或者绝对坐标
        self.transformImg = None


    def draw(self, img, xy=None):
        self.img = Image.open(img).convert('RGBA')
        img_w, img_h = self.img.width, self.img.height

        # 创建透明图层左背景
        bg = Image.new(size=self.img.size, color=(0,0,0,0), mode='RGBA')

        # 配置背景矩阵范围
        bg_range = [(0,0), (bg.width, 0), (bg.width, bg.height), (0, bg.height)]

        # 拼接参数作为仿射计算函数的入参
        nxy = self.convertXY(xy)

        transform = self.PerspectiveTransform(bg_range, nxy)

        new_img = self.img.transform(
            size=self.img.size,
            method=Image.PERSPECTIVE,
            data=transform,
            resample=Image.NEAREST,
            )


        return new_img


    def convertXY(self, xy):
        if isinstance(xy, dict):
            if self.mode == 'absolute': return [xy['left_top'], xy['right_top'], xy['right_down'], xy['left_down']]
            if self.mode == 'relative': return [
                xy['left_top'],
                (self.img.width - xy['right_top'][0], xy['right_top'][1]),
                (self.img.width - xy['right_down'][0] ,self.img.height - ['right_down'][1]),
                (xy['left_down'][0], self.height - xy['left_down'][1])
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
        A = np.matrix(matrix, dtype=np.float)
        B = np.array(background_xy).reshape(8)
        res = np.dot(np.linalg.inv(A.T * A) * A.T, B)
        return np.array(res).reshape(8)

if ( __name__ == "__main__"):
    test()

