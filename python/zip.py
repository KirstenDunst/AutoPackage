'''
Author: Cao Shixin
Date: 2019-08-27 15:14:09
LastEditors: Cao Shixin
LastEditTime: 2022-04-08 10:29:37
Description: 
'''
#压缩、解压缩 文件
import os
import zipfile


class ZipUnZip:
    @staticmethod
    def unzip(input_path, output_path):
        """
        解压缩指定文件夹
        :param input_path: zip文件路径
        :param output_path: 解压到的父级文件夹目录
        """
        f = zipfile.ZipFile(input_path, 'r')
        for file in f.namelist():
            f.extract(file, output_path)

    def zip(dirpath, outFullName):
        """
        压缩指定文件夹
        :param dirpath: 目标文件夹路径
        :param outFullName: 压缩文件保存路径+xxxx.zip
        """
        zip = zipfile.ZipFile(outFullName, "w", zipfile.ZIP_DEFLATED)
        for path, dirnames, filenames in os.walk(dirpath):
            # 去掉目标跟路径，只对目标文件夹下边的文件及文件夹进行压缩
            fpath = path.replace(dirpath, '')

            for filename in filenames:
                zip.write(os.path.join(path, filename),
                          os.path.join(fpath, filename))
        zip.close()
