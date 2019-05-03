#!/usr/bin/env python
# -*- coding: utf-8  -*-

import io
import os
import random
import qrcode
import base64
import requests

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from PIL import ImageFilter
from . import func

from qrcode.constants import ERROR_CORRECT_H

from ..settings_manager import settings


_letter_cases = "abcdefghjkmnpqrstuvwxy"  # 小写字母，去除可能干扰的i，l，o，z
_upper_cases = _letter_cases.upper()  # 大写字母
_numbers = ''.join(map(str, range(3, 10)))  # 数字
init_chars = ''.join((_letter_cases, _upper_cases, _numbers))

def download_img(url, root_path='/tmp/img/', headers=None):
    try:
        if not url:
            return ''
        img_ext = 'png'
        filename = ''
        binary_data = b''
        if url[0:22]=='data:image/png;base64,':
            from binascii import a2b_base64
            data = bytes(url[22:], encoding='utf8')
            binary_data = a2b_base64(data)
            filename = func.md5(binary_data)
            img_ext = 'png'
        else:
            if url[0:2]=='//':
                url = 'https:'+url
            url = url.replace('\\','')
            r = requests.get(url, headers=headers, timeout=30000)
            binary_data = r.content
            filename = func.md5(url.split('/')[-1])
            img_ext = r.headers['Content-Type'].split('/')[1]
        # end if
        path = root_path + filename
        if not os.path.exists(root_path):
            os.makedirs(root_path)
        img_file = '%s.%s' % (path, img_ext, )
        if not os.path.exists(img_file):
            with open(img_file,'wb') as f:
                f.write(binary_data)
        return (img_file, img_ext)
    except TimeoutError as e:
        print(url)
    except Exception as e:
        print(url)
        raise e

def create_validate_code(
    size=(120, 40),
    chars=init_chars,
    img_type="GIF",
    mode="RGB",
    bg_color=(255, 255, 255),
    fg_color=(0, 0, 255),
    font_size=14,
    font_type="CORBEL.TTF",
    length=4,
    draw_lines=True,
    n_line=(1, 4),
    draw_points=True,
    point_chance=2):
        """
        @todo: 生成验证码图片
        @param size: 图片的大小，格式（宽，高），默认为(120, 40)
        @param chars: 允许的字符集合，格式字符串
        @param img_type: 图片保存的格式，默认为GIF，可选的为GIF，JPEG，TIFF，PNG
        @param mode: 图片模式，默认为RGB
        @param bg_color: 背景颜色，默认为白色
        @param fg_color: 前景色，验证码字符颜色，默认为蓝色#0000FF
        @param font_size: 验证码字体大小
        @param font_type: 验证码字体，默认为 CORBEL.ttf
        @param length: 验证码字符个数
        @param draw_lines: 是否划干扰线
        @param n_lines: 干扰线的条数范围，格式元组，默认为(1, 4)，只有draw_lines为True时有效
        @param draw_points: 是否画干扰点
        @param point_chance: 干扰点出现的概率，大小范围[0, 100]
        @return: [0]: PIL Image实例
        @return: [1]: 验证码图片中的字符串
        """

        width, height = size # 宽， 高
        img = Image.new(mode, size, bg_color) # 创建图形
        draw = ImageDraw.Draw(img) # 创建画笔

        if not os.path.isfile(font_type):
            font_type = '%s/%s' % (settings.STATIC_PATH, 'fonts/CORBEL.TTF')
        def get_chars():
                """生成给定长度的字符串，返回列表格式"""
                return random.sample(chars, length)

        def create_lines():
                """绘制干扰线"""
                line_num = random.randint(*n_line) # 干扰线条数

                for i in range(line_num):
                        # 起始点
                        begin = (random.randint(0, size[0]), random.randint(0, size[1]))
                        #结束点
                        end = (random.randint(0, size[0]), random.randint(0, size[1]))
                        draw.line([begin, end], fill=(0, 0, 0))

        def create_points():
                """绘制干扰点"""
                chance = min(100, max(0, int(point_chance))) # 大小限制在[0, 100]

                for w in range(width):
                        for h in range(height):
                                tmp = random.randint(0, 100)
                                if tmp > 100 - chance:
                                        draw.point((w, h), fill=(0, 0, 0))

        def create_strs():
                """绘制验证码字符"""
                c_chars = get_chars()
                strs = ' %s ' % ' '.join(c_chars) # 每个字符前后以空格隔开

                font = ImageFont.truetype(font_type, font_size)
                font_width, font_height = font.getsize(strs)

                draw.text(((width - font_width) / 3, (height - font_height) / 3),
                                        strs, font=font, fill=fg_color)

                return ''.join(c_chars)

        if draw_lines:
                create_lines()
        if draw_points:
                create_points()
        strs = create_strs()

        # 图形扭曲参数
        params = [
            1 - float(random.randint(1, 2)) / 100,
            0,
            0,
            0,
            1 - float(random.randint(1, 10)) / 100,
            float(random.randint(1, 2)) / 500,
            0.001,
            float(random.randint(1, 2)) / 500,
        ]
        img = img.transform(size, Image.PERSPECTIVE, params) # 创建扭曲

        img = img.filter(ImageFilter.EDGE_ENHANCE_MORE) # 滤镜，边界加强（阈值更大）

        return img, strs

def _create_qrcode(data, imgFn):
    qr = qrcode.QRCode(
        version=1,
        #设置容错率为最高
        error_correction=qrcode.ERROR_CORRECT_H,
        box_size=6,
        border=2,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image()
    #设置二维码为彩色
    img = img.convert("RGBA")
    icon = Image.open(imgFn)
    w, h = img.size
    factor = 4
    size_w = int(w / factor)
    size_h = int(h / factor)
    icon_w, icon_h = icon.size
    if icon_w > size_w:
        icon_w = size_w
    if icon_h > size_h:
        icon_h = size_h
    icon = icon.resize((icon_w, icon_h), Image.ANTIALIAS)
    w = int((w - icon_w) / 2)
    h = int((h - icon_h) / 2)
    icon = icon.convert("RGBA")
    newimg = Image.new("RGBA", (icon_w + 8, icon_h + 8), (255, 255, 255))
    img.paste(newimg, (w-4, h-4), newimg)
    img.paste(icon, (w, h), icon)
    return img

def qrcode_base64_img(data, logo):
    img = _create_qrcode(data, logo)
    #创建一个文件流
    imgio = io.BytesIO()
    img.save(imgio, 'png')
    qrcode_img = "data:image/png;base64,%s" % base64.b64encode(imgio.getvalue()).decode('utf-8')
    return qrcode_img
