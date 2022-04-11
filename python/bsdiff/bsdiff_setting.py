'''
Author: Cao Shixin
Date: 2019-11-28 15:10:01
LastEditors: Cao Shixin
LastEditTime: 2022-04-11 16:33:01
Description: 
'''
#处理差异文件


class DiffSetting(object):
    def __init__(self, base_path):
        """初始化"""
        super(DiffSetting, self).__init__()
        # 差量处理根目录  '/Users/caoshixin/Desktop/AutoPackage/starkidapp_hotfix/'
        # 里面区分develop or release/version/number/(zip and patch Directoy)/patchs
        self.base_path = base_path

        # bsdiff 文件的上级目录
        self.bsdiff_path = '/Users/caoshixin/Desktop/AutoPackage/AutoPackage/python/bsdiff/bsdiff'

        # 资源清单文件基础map
        self.manifest_map = {'type': '', 'entry': 'page'}
        # 资源清单文件名
        self.mainfest_name = 'resource-bundle.manifest'

        # oss控制清单基础文件
        self.oss_map = {
            'bundlePlatform': 'flutter',
            'bundleType': 'web',
            'desc': '有升级',
            'entireBundleUrl': '替换为远端全量包url',
            'forceUpdate': True,
            'patchRootUrl': 'patch远端目录url,结尾不带/'
        }
        # oss控制清单文件名
        self.oss_name = 'update-manifest.json'
