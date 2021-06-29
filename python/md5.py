'''
Author: Cao Shixin
Date: 2021-06-26 18:27:22
LastEditors: Cao Shixin
LastEditTime: 2021-06-26 18:31:18
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
                content = f.read()
            md5_obj = hashlib.md5()
            md5_obj.update(str(content).encode(encoding='utf8'))
            hash_code = md5_obj.hexdigest()
            md5 = str(hash_code).lower()
            return md5
        else:
            return None