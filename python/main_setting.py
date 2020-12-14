'''
@Author: Cao Shixin
@Date: 2020-05-28 09:31:14
LastEditors: Cao Shixin
LastEditTime: 2020-12-04 14:09:44
@Description: 基础设置
@Email: cao_shixin@yahoo.com
@Company: BrainCo
'''


class MainSettings():
    """常用设置"""
    def __init__(self):
        """初始化"""
        super(MainSettings, self).__init__()
        # 项目地址路径flutter
        self.project_base_path = '/Users/caoshixin/公司/ProjectDev/focus_world'
        # 包成立之后的存放位置
        self.package_path = '/Users/caoshixin/Desktop/AutoPackage/ipa/focus_world'
