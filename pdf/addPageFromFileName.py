# -*- coding: utf-8 -*-
#
# @Author: CPS
# @email: 373704015@qq.com
# @Date: 2023-02-24 10:53:22.189861
# @Last Modified by: CPS
# @Last Modified time: 2023-02-24 10:53:22.189861
# @file_path "W:\CPS\IDE\SublimeText\JS_SublmieText\Data\Packages\cps-fileheader"
# @Filename "main.py"
# @Description: 功能描述
#
import os, sys, json

from os import path
from pathlib import Path
from pydantic import BaseModel

import fitz
from fitz import Point

font_name = {"宋体": "SimSun"}
font_path = {"宋体": r"C:\Windows\Fonts\simsun.ttc"}


def print_json(obj: dict):
    print(json.dumps(obj, indent="  ", ensure_ascii=False))


class FontInfo(BaseModel):
    font_size: int | float
    font_name: str
    font_path: str


def get_title_position(
    title: str | float | int, font_opts: FontInfo, page_width: float, page_height: float
) -> Point:
    """
    @Description 以`fitz.Point()`的类型返回文本的居中位置，可以直接作为`page.insert_text()`的第一个参数

    - param title       :{str}   要插入的标题
    - param font_size   :{float} {description}
    - param page_width  :{float} {description}
    - param page_height :{float} {description}

    @returns `{ Point}` {description}

    """
    temp_doc = fitz.open()
    temp_page = temp_doc.new_page(width=page_width, height=page_height)
    temp_page.insert_text(
        fitz.Point(0, font_opts.font_size),
        text=title,
        fontname=font_opts.font_name,
        fontfile=font_opts.font_path,
        fontsize=font_opts.font_size,
    )
    text_info = temp_page.get_text("dict")
    center_w = page_width / 2 - (
        text_info["blocks"][0]["lines"][0]["spans"][0]["bbox"][2] / 2
    )
    center_h = page_height / 2 - (
        text_info["blocks"][0]["lines"][0]["spans"][0]["bbox"][3] / 2
    )

    return fitz.Point(center_w, center_h)


def main(pdf_path: str):
    p = Path(pdf_path)

    title = path.splitext(p.name)[0]
    output_path = path.join(path.dirname(pdf_path), f"{title}_01.pdf")
    font_info = FontInfo(
        font_size=22,
        font_name="SimSun",
        font_path=r"C:\Windows\Fonts\simsun.ttc",
    )

    # 页面最大尺寸
    doc = fitz.open(pdf_path)
    max_h = max_w = 0
    for each_page in doc:
        page_info = each_page.get_text("dict", sort=False)
        if page_info["width"] < page_info["height"]:
            page_w = page_info["width"]
            page_h = page_info["height"]
        else:
            page_w = page_info["height"]
            page_h = page_info["width"]

        if page_w > max_w:
            max_w = page_info["width"]

        if page_h > max_h:
            max_h = page_info["height"]

    new_doc = fitz.open()
    new_page = new_doc.new_page(width=max_w, height=max_h)
    new_page.insert_text(
        get_title_position(title, font_info, max_w, max_h),
        text=title,
        fontname=font_info.font_name,
        fontfile=font_info.font_path,
        fontsize=font_info.font_size,
    )

    new_doc.save(
        output_path,
        deflate=1,
        deflate_images=1,
        deflate_fonts=1,
        clean=1,
        linear=1,
        expand=0,
    )
    # empty_doc.saveIncr(output_path1)


if __name__ == "__main__":
    target_floder = r"Z:\work\2023\项目\江西千吨万人图纸\设计图合并"
    p = Path(target_floder)

    # 先给每个pdf添加后缀00
    # for pdf_path in p.glob("**/*.pdf"):
    #     t = Path(pdf_path)
    #     new_name = f"{path.splitext(t.name)[0]}_00.pdf"
    #     print("修改名字为: ", pdf_path)

    # 遍历目录
    for pdf_path in p.glob("**/*.pdf"):
        main(pdf_path)

    # print(os.listdir(r"C:\Windows\fonts"))
