'''
Author: Cao Shixin
Date: 2021-06-10 13:58:14
LastEditors: Cao Shixin
LastEditTime: 2022-01-17 11:14:21
Description: 获取项目里的一些配置信息
'''
from xml.etree.ElementTree import fromstring

class ProjectConfigurationRead(object):
    """
    读取项目里面的一些配置信息,目前只支持iOS
    """

    def __init__(self, plist_file_path):
        super(ProjectConfigurationRead, self).__init__()
        # 项目配置json，将配置里面的xml设置转化成json，方便后面文件的对应参数取值
        self.project_info_json = {}
        plistContentStr = open(plist_file_path, 'r').read()  # 读取plist文件
        plistXMLTree = fromstring(plistContentStr)  # 转换成XML树
        self.__convert_tree_to_dict(plistXMLTree, self.project_info_json)
        print('读取解析%s' % self.project_info_json)

    def __convert_tree_to_dict(self, tree, d):
        for index, item in enumerate(tree):  # 遍历整棵XML树
            if item.tag == 'key':  # 如果该item的tag为'key'
                # 根据下一个结点的tag值不同，放在dict的不同位置上
                if tree[index + 1].tag == 'string':
                    d[item.text] = tree[index + 1].text
                elif tree[index + 1].tag == 'true':
                    d[item.text] = True
                elif tree[index + 1].tag == 'false':
                    d[item.text] = False
                elif tree[index + 1].tag == 'dict':
                    self.__convert_tree_to_dict(tree[index + 1], d)  # 递归下去
            elif item.tag == 'dict':
                self.__convert_tree_to_dict(item, d)

    def get_project_bundle_name(self):
        """获取项目的显示名称"""
        if 'CFBundleName' in self.project_info_json:
            print('项目bundle名称：%s' % (self.project_info_json['CFBundleName']))
            return self.project_info_json['CFBundleName']


if __name__ == '__main__':
    plist_path = input('请输入plist文件的本地文件路径地址：')

    result = ProjectConfigurationRead(plist_path)
