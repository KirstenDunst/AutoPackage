'''
Author: Cao Shixin
Date: 2019-08-27 15:14:09
LastEditors: Cao Shixin
LastEditTime: 2022-04-11 18:31:42
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
        """
        zip_file = zipfile.ZipFile(input_path)
        if os.path.isdir(output_path):
            pass
        else:
            os.mkdir(output_path)
        for names in zip_file.namelist():
            zip_file.extract(names, output_path)
        zip_file.close()

    def zip(dirpath, outFullName):
        """
        压缩指定文件夹
        :param dirpath: 目标文件夹路径
        :param outFullName: 压缩文件保存路径+xxxx.zip
        """
        zipf = zipfile.ZipFile(outFullName, 'w')
        pre_len = len(os.path.dirname(dirpath))
        for parent, dirnames, filenames in os.walk(dirpath):
            for filename in filenames:
                pathfile = os.path.join(parent, filename)
                arcname = pathfile[pre_len:].strip(os.path.sep)  # 相对路径
                zipf.write(pathfile, arcname)
        zipf.close()
