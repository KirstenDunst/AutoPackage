# -*- coding: utf-8 -*-
'''
Author: Cao Shixin
Date: 2023-03-27 16:24:00
LastEditors: Cao Shixin
LastEditTime: 2023-03-27 16:25:40
Description: 
'''
import os
import time
import shutil


# 复制目标文件或目录到指定路径
def cp(src, dst):
    f = File(src)
    f2 = File(dst)
    if f.exists():
        if f2.exists():
            f2.delete()
        if f.isFile():
            f.copyFileTo(dst)
            return True
        elif f.isDir():
            f.copyTreeTo(dst)
            return True
    else:
        return False


# 将src移动至dst目录下。若dst目录不存在，则效果等同于src改名为dst。若dst目录存在，将会把src文件夹的所有内容移动至该目录下面
def mv(src, dst):
    return shutil.move(src, dst);


# 删除目标文件或目录
def rm(src):
    f = File(src)
    if f.exists():
        return f.delete()


# 返回当前工作目录
def pwd():
    return os.getcwd()


# 返回当前工作目录
def getpwd():
    return pwd()


# 生成压缩文件,目前支持的有：tar、zip、gztar、bztar
def pack(base_name, format, root_dir):
    shutil.make_archive(base_name, format, root_dir)


# 解压操作。
def unpack(zip_path, extract_dir):
    shutil.unpack_archive(zip_path, extract_dir)


separator = os.path.sep


class File(object):
    __path = ''

    def __init__(self, path):
        self.__path = path

    def __repr__(self, *args, **kwargs):
        return str({'file_name': self.__path, 'exit': self.exists(), 'isFile': self.isFile()})

    def __hash__(self, *args, **kwargs):
        return self.__path.__hash__(self, *args, **kwargs)

    def __le__(self, *args, **kwargs):
        return self.length()

    def getName(self):
        return os.path.basename(self.__path)

    def exists(self):
        return os.path.exists(self.__path)

    def mkdir(self):
        os.mkdir(self.__path)

    def makedirs(self):
        os.makedirs(self.__path)

    def mkdirs(self):
        os.makedirs(self.__path)

    def isDir(self):
        return os.path.isdir(self.__path)

    def isDirectory(self):
        return os.path.isdir(self.__path)

    def isFile(self):
        return os.path.isfile(self.__path)

    def delete(self):
        if self.isDir():
            if len(self.listFile()) == 0:
                # 删除空目录
                return os.rmdir(self.__path)
            else:
                # 删除有内容目录
                return shutil.rmtree(self.__path)
        else:
            return os.remove(self.__path)

    def length(self):
        return os.path.getsize(self.__path)

    def size(self):
        return os.path.getsize(self.__path)

    def rename(self, newPath):
        os.rename(self.__path, newPath)

    def copyFileTo(self, newPath):
        shutil.copy(self.__path, newPath)

    def copyFile(self, newPath):
        self.copyFileTo(newPath)

    # olddir和newdir都只能是目录，且newdir必须不存在
    def copyTreeTo(self, newPath):
        shutil.copytree(self.__path, newPath)

        # olddir和newdir都只能是目录，且newdir必须不存在

    def copyTree(self, newPath):
        self.copyTreeTo(newPath)

        # 移动文件/目录

    def moveTo(self, newPath):
        shutil.move(self.__path, newPath)

        #

    def listFile(self):
        if self.isFile():
            raise Exception("该文件不是目录", self.__path)
        childs = os.listdir(self.__path)
        ret = []
        for i in childs:
            ret.append(File(self.__path + os.path.sep + i))
        return ret

    def getPath(self):
        return self.__path

    # 当成空白文件
    def open(self, mode='r', encoding='utf-8'):
        return open(self.__path, mode, encoding=encoding)

    # 格式化输出时间
    def timeStamp2Time(self, timestamp):
        timeStruct = time.localtime(timestamp)
        return time.strftime('%Y-%m-%d %H:%M:%S', timeStruct)

    # 创建时间
    def getCreateTime(self, modify=True):
        if (modify):
            return self.timeStamp2Time(os.path.getctime(self.__path))
        return os.path.getctime(self.__path)

    # 修改时间
    def getModifyTime(self, modify=True):
        if (modify):
            return self.timeStamp2Time(os.path.getmtime(self.__path))
        return os.path.getmtime(self.__path)
