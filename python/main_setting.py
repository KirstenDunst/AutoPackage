"""
@Author: Cao Shixin
@Date: 2020-05-28 09:31:14
LastEditors: Cao Shixin
LastEditTime: 2020-12-04 14:09:44
@Description: 基础设置
@Email: cao_shixin@yahoo.com
@Company: BrainCo
"""


class MainSettings(object):
    """常用设置"""

    def __init__(self):
        """初始化"""
        super(MainSettings, self).__init__()
        # 项目地址路径flutter
        self.project_base_path = '/Users/caoshixin/公司/ProjectDev/focus_world'
        # 包导出的配置型文件存放父级目录地址
        self.export_plist_father_path = '/Users/caoshixin/Desktop/AutoPackage'
        # 包成立之后的存放位置
        self.package_path = '/Users/caoshixin/Desktop/AutoPackage/ipa/focus_world'

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
        # appstore
        self.APPSTORE_APP_ID = 'X'
        # 注意这里的密码是授权码，并不是明文登陆密码
        self.APPSTORE_APP_ID_SECRET = 'X'
