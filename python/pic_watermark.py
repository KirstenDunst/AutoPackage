# coding:utf-8
'''
Author: Cao Shixin
Date: 2022-03-31 10:17:25
LastEditors: Cao Shixin
LastEditTime: 2022-03-31 10:53:03
Description: 给图片加文字水印
'''

import os
import shutil
from PIL import Image, ImageDraw, ImageFont


def add_text_to_image(image, text):
    font = ImageFont.truetype('/Users/caoshixin/Desktop/HappyZcool-2016.ttf',
                              36)

    # 添加背景
    new_img = Image.new('RGBA', (image.size[0] * 3, image.size[1] * 3),
                        (0, 0, 0, 0))
    new_img.paste(image, image.size)

    # 添加水印
    font_len = len(text)
    rgba_image = new_img.convert('RGBA')
    text_overlay = Image.new('RGBA', rgba_image.size, (255, 255, 255, 0))
    image_draw = ImageDraw.Draw(text_overlay)

    for i in range(0, rgba_image.size[0], font_len * 40 + 100):
        for j in range(0, rgba_image.size[1], 200):
            image_draw.text((i, j), text, font=font, fill=(0, 0, 0, 50))
    text_overlay = text_overlay.rotate(45)
    image_with_text = Image.alpha_composite(rgba_image, text_overlay)

    # 裁切图片
    image_with_text = image_with_text.crop(
        (image.size[0], image.size[1], image.size[0] * 2, image.size[1] * 2))
    return image_with_text


if __name__ == '__main__':
    # img = Image.open("/Users/caoshixin/Desktop/ball_contacted.png")
    # im_after = add_text_to_image(img, u'测试使用')
    # im_after.save(u'测试使用.png')

    file_directory = input('请输入需要处理的文件夹目录：')
    if not os.path.isdir(file_directory + '_new'):
        os.makedirs(file_directory + '_new')
    folder_path_files = os.listdir(file_directory)
    for file_name in folder_path_files:
        if file_name.split('.')[-1] in ['jpeg','jpg','png','webp']:
            full_file_name = os.path.join(file_directory, file_name)
            img = Image.open(full_file_name)
            im_after = add_text_to_image(img, u'开星果')
            im_after.save(u'%s/%s' % (file_directory + '_new', file_name))
