'''
Author: Cao Shixin
Date: 2021-06-10 13:58:14
LastEditors: Cao Shixin
LastEditTime: 2022-01-17 11:20:28
Description: 基础设置
'''

class MainSettings(object):
    """常用设置"""

    def __init__(self):
        """初始化"""
        super(MainSettings, self).__init__()
        # 项目地址路径flutter
        self.project_base_path = '/Users/caoshixin/公司/ProjectDev/focus_world'
        # 包导出的配置型文件存放父级目录地址
        self.export_plist_father_path = '/Users/caoshixin/Desktop/AutoPackage/focusworld'
        # 包成立之后 ios包的存放位置
        self.ipa_package_path = '/Users/caoshixin/Desktop/AutoPackage/ipa'
        # 安卓包存放位置
        self.android_package_path = '/Users/caoshixin/Desktop/AutoPackage/focusworld/apk'
        # 定时打包plist文件名
        self.regular_launchctl_name = 'com.launchctl.morpheus.plist'

        # 专属消息发送信息
        # 发送人的地址
        self.QQ_FROM_ADDRESS = 'XXXXXXXXXXXXXXXXXXXX@qq.com'
        # 邮箱密码换成他提供的16位授权码
        self.QQ_PASSWORD = 'XXXXXXXXXXXXXXXXXXXX'
        # 收件人地址,可以是多个的
        self.QQ_TO_ADDRESS = 'XXXXXXXXXXXXXXXXXXXX@qq.com'
        # 因为我是使用QQ邮箱..
        self.QQ_SMTP_SERVER = 'smtp.qq.com'
        # 钉钉access_token
        self.DING_TALK_TOKEN = 'XXXXXXXXXXXXXXXXXXXX'
        # bugly的app_id
        self.BUGLY_APP_ID = 'X'
        # bugly的app_key
        self.BUGLY_APP_KEY = 'X'
        # 蒲公英的APP地址
        self.PGYER_IPA_DOWNLOAD_URL = 'https://www.pgyer.com/XXXXX'
        # fir下载安装包路径地址
        self.FIR_IPA_DOWNLOAD_URL = 'http://d.firim.top/XXXXX'
        # 蒲公英账号API_KEY
        self.PGYER_API_KEY = 'X'
        # fir token
        self.FIR_API_TOKEN = 'X'
         # fir 上传需要额外上传icon   应用icon地址
        self.icon_path = '/Users/caoshixin/Desktop/AutoPackage/focusworld/icon.png'
        # appstore
        self.APPSTORE_API_KEY = 'X'
        # 注意这里的密码是授权码，并不是明文登陆密码
        self.APPSTORE_API_ISSUER = 'X'
