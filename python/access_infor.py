"""
@Author: Cao Shixin
@Date: 2020-05-27 16:12:57
LastEditors: Cao Shixin
LastEditTime: 2020-12-08 18:30:45
@Description: 使用信息获取
@Email: cao_shixin@yahoo.com
@Company: BrainCo
"""


class AccessInformation:
    """用户信息获取"""

    @staticmethod
    def platform_upload_appstore():
        """获取打包上报平台"""
        platform = input('准备上传到哪里？ AppStore? 三方托管平台Third?。或输入Q退出：[A/T/Q]')
        if platform.upper() == 'A':
            return True
        elif platform.upper() == 'T':
            return False
        elif platform.upper() == 'Q':
            exit()
        else:
            exit('输入不合法，请重新运行main.py重新开始')

    @staticmethod
    def get_package_environment():
        """获取当前打包的环境"""
        page_environment = input('准备打包什么环境？ Profile? Release?。或输入Q退出：[P/R/Q]')
        if page_environment.upper() == 'P':
            return 'Profile'
        elif page_environment.upper() == 'R':
            return 'Release'
        elif page_environment.upper() == 'Q':
            exit()
        else:
            exit('输入不合法，请重新运行main.py重新开始')

    @staticmethod
    def get_package_export_plist(upload_appstore):
        """打包适用环境"""
        if upload_appstore:
            return "ExportOptions_AppStore"
        else:
            return "ExportOptions_AdHoc"
