'''
@Author: Cao Shixin
@Date: 2020-05-27 16:12:57
LastEditors: Cao Shixin
LastEditTime: 2020-12-08 18:30:45
@Description: 使用信息获取
@Email: cao_shixin@yahoo.com
@Company: BrainCo
'''


class AccessInformation:
    """用户信息获取"""
    @staticmethod
    def platform_upload_AppStore():
        """获取打包上报平台"""
        platform = input('准备上传到哪里？ AppStore? 三方托管平台Third?。或输入Q退出：[A/T/Q]')
        if platform.upper() == 'A':
            upload_platform = True
        elif platform.upper() == 'T':
            upload_platform = False
        elif platform.upper() == 'Q':
            exit()
        else:
            exit('输入不合法，请重新运行main.py重新开始')
        return upload_platform

    @staticmethod
    def get_packaging_enviorment():
        """获取当前打包的环境"""
        page_envir = input('准备打包什么环境？ Profile? Release?。或输入Q退出：[P/R/Q]')
        if page_envir.upper() == 'P':
            envir_dir_name = 'Profile'
        elif page_envir.upper() == 'R':
            envir_dir_name = 'Release'
        elif page_envir.upper() == 'Q':
            exit()
        else:
            exit('输入不合法，请重新运行main.py重新开始')
        return envir_dir_name

    @staticmethod
    def get_package_export_plist(upload_appstore):
        """打包适用环境"""
        if upload_appstore:
            envior_package = "ExportOptions_AppStore"
        else:
            envior_package = "ExportOptions_AdHoc"
        return envior_package
