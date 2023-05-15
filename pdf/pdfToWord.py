# -*- coding: utf-8 -*-
#
# @Author: CPS
# @email: 373704015@qq.com
# @Date: 2023-03-20 10:25:24.734788
# @Last Modified by: CPS
# @Last Modified time: 2023-03-20 10:25:24.734788
# @file_path "W:\CPS\IDE\SublimeText\JS_SublmieText\Data\Packages\cps-fileheader"
# @Filename "main.py"
# @Description: pdf文件导出成word
#
import os, sys

sys.path.append("..")

from os import path
from pathlib import Path
from pydantic import BaseModel

from pdf2docx import Converter


def main(pdf_path: str, docx_path):
    cv = Converter(pdf_path)
    cv.convert(docx_path, start=0, end=None)
    cv.close()


if __name__ == "__main__":
    pdf_path = r"Z:\work\2023\改图\2021年海南水文测站超标洪水测报预案询价邀请函--珠江水文水资源勘测中心(1).pdf"
    output_path = r"./test.docx"

    main(pdf_path, output_path)
