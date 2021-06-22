'''
Author: Cao Shixin
Date: 2021-06-10 13:58:14
LastEditors: Cao Shixin
LastEditTime: 2021-06-22 17:00:47
Description: 使用信息获取
'''

class AccessInformation:
    """用户信息获取"""

    @staticmethod
    def packaging_mode():
        '''打包模式快速响应处理'''
        platform = input('是否是一般打包模式？或输入Q退出：[T/F/Q]:')
        if platform.upper() == 'T':
            return True
        elif platform.upper() == 'F':
            return False
        elif platform.upper() == 'Q':
            exit()
        else:
            exit('输入不合法，请重新运行main.py重新开始')
        

    @staticmethod
    def platform_upload_appstore():
        """获取打包上报平台"""
        platform = input('准备上传到哪里？ AppStore? 三方托管平台Third?。或输入Q退出：[A/T/Q]:')
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
        page_environment = input('准备打包什么环境？ Profile? Release? Debug。或输入Q退出：[P/R/D/Q]:')
        if page_environment.upper() == 'P':
            return 'Profile'
        elif page_environment.upper() == 'R':
            return 'Release'
        elif page_environment.upper() == 'D':
            return 'Debug'
        elif page_environment.upper() == 'Q':
            exit()
        else:
            exit('输入不合法，请重新运行main.py重新开始')

    @staticmethod
    def get_package_export_plist(upload_appstore, package_environment):
        """打包配置文件"""
        if upload_appstore:
            return "ExportOptions_AppStore"
        else:
            if package_environment == 'Debug':
                return "ExportOptions_Develop"
            else:
                return "ExportOptions_AdHoc"
