'''
Author: Cao Shixin
Date: 2020-12-14 11:16:43
LastEditors: Cao Shixin
LastEditTime: 2020-12-14 16:44:35
Description: iOS上报符号表，bugly、友盟、
'''
import requests
import os

BUGLY_APP_ID = 'X'  # bugly的appid
BUGLY_APP_KEY = 'X'  # bugly的appkey


class SymbolTable:
    """
    上报符号表
    """
    @staticmethod
    def bugly(dsym_path, bundleId, productVersion):
        """
        上报bugly符号表
        """
        if dsym_path:
            print('\n==============开始处理bugly符号表================\n')
            father_path = os.path.dirname(os.path.realpath(__file__))
            symbol_file_name = bundleId + productVersion + '.zip'
            os.system('java -jar ' + father_path + '/buglySymboliOS.jar -i ' +
                      dsym_path + ' -o ' + symbol_file_name)
            print('\n==============处理完毕开始上传bugly符号表================\n')
            # https://bugly.qq.com/docs/user-guide/symbol-configuration-ios具体参数可以进去里面查看,
            url = 'https://api.bugly.qq.com/openapi/file/upload/symbol'
            data = {
                'api_version': '1',
                'symbolType': '2',
                'app_id': BUGLY_APP_ID,
                'app_key': BUGLY_APP_KEY,
                'bundleId': bundleId,
                'productVersion': productVersion,
                'fileName': bundleId + productVersion + '.dSYM.zip',
            }
            files = {
                'file':
                open(os.path.dirname(dsym_path) + symbol_file_name, 'rb')
            }
            r = requests.post(url, data=data, files=files)
            if r.status_code == 200:
                print('\n=============上报bugly符号表成功============\n')
        else:
            exit('\n/////////符号表操作对象dsym路径不存在:' + dsym_path)
