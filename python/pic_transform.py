# -*- coding: utf-8 -*
'''
Author: Cao Shixin
Date: 2022-04-13 09:24:05
LastEditors: Cao Shixin
LastEditTime: 2022-10-26 18:10:05
Description: 
'''
import os
import whatimage
import pyheif
import traceback
from PIL import Image


class PicTransform:
    # 图片解码
    # byteIo为解码数据
    # filename 为传入的文件名保存时使用
    @staticmethod
    def decodeImageFromHeicToPng(bytesIo, filename):
        try:
            fmt = whatimage.identify_image(bytesIo)
            print(fmt)
            if fmt in ['heic']:
                i = pyheif.read_heif(bytesIo)
                pi = Image.frombytes(mode=i.mode, size=i.size, data=i.data)
                pi.save(filename, format="png")
                # PicTransform.compress_image(filename)
                print("文件转换成功并保存到：" + filename)
        except:
            traceback.print_exc()

    @staticmethod
    def compress_image(infile, outfile='', mb=500, step=10, quality=80):
        """不改变图片尺寸压缩到指定大小
        :param infile: 压缩源文件
        :param outfile: 压缩文件保存地址
        :param mb: 压缩目标,KB
        :param step: 每次调整的压缩比率
        :param quality: 初始压缩比率
        :return: 压缩文件地址，压缩文件大小
        """
        o_size = os.path.getsize(infile) / 1024
        if o_size <= mb:
            return infile, o_size
        if not outfile:
            dir, suffix = os.path.splitext(infile)
            outfile = '{}-out{}'.format(dir, suffix)
        while o_size > mb:
            im = Image.open(infile)
            im.save(outfile, quality=quality)
            if quality - step < 0:
                break
            quality -= step
            o_size = os.path.getsize(outfile) / 1024
        return outfile, os.path.getsize(outfile) / 1024

    @staticmethod
    def resize_image(infile, outfile='', x_s=1376):
        """修改图片尺寸
        :param infile: 图片源文件
        :param outfile: 重设尺寸文件保存地址
        :param x_s: 设置的宽度
        :return:
        """
        im = Image.open(infile)
        x, y = im.size
        y_s = int(y * x_s / x)
        out = im.resize((x_s, y_s), Image.ANTIALIAS)
        outfile = PicTransform.get_outfile(infile, outfile)
        out.save(outfile)

    # 读取图片文件
    # filename为要打开的文件路径
    @staticmethod
    def readImage(filename):
        with open(filename, 'rb') as f:
            data = f.read()
        return data

    # 遍历path指定文件夹下的所有HEIC文件并转换为PNG文件
    @staticmethod
    def convertImagesFromHeicToPng(path):
        filenames = os.listdir(path)
        if not os.path.exists(path + '/png'):
            os.makedirs(path + '/png')
        for name in filenames:
            filename = path + "/" + name  # 完成路径
            print('当前转换文件：' + filename)
            data = PicTransform.readImage(filename)  # 读取图像文件
            PicTransform.decodeImageFromHeicToPng(
                data, path + '/png/' + name.split('.')[0] + '.png')  # 转换


if __name__ == '__main__':
    path = input('输入需要处理的文件夹路径：')
    # PicTransform.convertImagesFromHeicToPng(path=path)

    filenames = os.listdir(path)
    if not os.path.exists(path + '/new'):
        os.makedirs(path + '/new')
    for name in filenames:
        subTip = name.split('.')[-1]
        if ['png', 'webp', 'jpg', 'jpeg'].__contains__(subTip.lower()):
            filename = path + "/" + name  # 完成路径
            print('当前转换文件：' + filename)
            PicTransform.compress_image(filename,
                                        outfile=path + '/new/' + name,
                                        mb=500)
            # im = Image.open(filename)
            # im.save(path + '/new/' + name, quality=40)
