'''
Author: Cao Shixin
Date: 2021-06-26 18:27:22
LastEditors: Cao Shixin
LastEditTime: 2022-04-07 16:50:58
Description: 
'''

import hashlib
import os

class MD5Helper(object):
    def __init__(self, *args):
        super(MD5Helper, self).__init__(*args)

    @staticmethod
    def get_file_md5(file_path):
        if os.path.isfile(file_path):
            with open(file_path, 'rb') as f:
                md5obj = hashlib.md5()
                md5obj.update(f.read())
                _hash = md5obj.hexdigest()
            return str(_hash).lower()
        else:
            return None

    @staticmethod
    def md5_convert(string):
        """计算字符串md5值
            :param string: 输入字符串
            :return: 字符串md5
        """
        m = hashlib.md5()
        m.update(string.encode())
        return m.hexdigest()