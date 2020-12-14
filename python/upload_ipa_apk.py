'''
@Author: Cao Shixin
@Date: 2020-05-27 19:54:39
LastEditors: Cao Shixin
LastEditTime: 2020-12-06 15:01:52
@Description: 包上传工具
@Email: cao_shixin@yahoo.com
@Company: BrainCo
'''
import os
import webbrowser
import requests
import json
from access_infor import AccessInformation

pugongying_ipa_download_url = 'https://www.pgyer.com/XXXXX'  # 蒲公英的APP地址
fir_ipa_download_url = 'http://d.firim.top/XXXXX'  # fir下载安装包路径地址

# 蒲公英账号API_KEY
API_KEY = 'XXXXXXXXXXXXXXXXXXX'

# fir token
FIR_API_TOKEN = 'XXXXXXXXXXXXXXXXXXXXXXX'

# appstore
DEVELOP_APPID = 'XXXXXXXXXXXXXXXXXXXXX'
DEVELOP_APPID_SECRET = 'XXXXXXXXXXXXXXXXXXXXXXX'  # 注意这里的密码是授权码，并不是明文登陆密码


class UploadIpaApk:
    """
    上传包处理
    """
    @staticmethod
    def pugongying(package_path, description):
        """
        上传蒲公英
        ：package_path：包文件路径地址（本地文件地址）
        ：description： 本次更新描述信息
        """
        if package_path:
            # https://www.pgyer.com/doc/api 具体参数可以进去里面查看,
            url = 'https://www.pgyer.com/apiv2/app/upload'
            data = {
                '_api_key': API_KEY,
                'installType': '1',
                'buildUpdateDescription': description
            }
            files = {'file': open(package_path, 'rb')}
            r = requests.post(url, data=data, files=files)
            if r.status_code == 200:
                # 打开浏览器
                webbrowser.open(pugongying_ipa_download_url,
                                new=1,
                                autoraise=True)
        else:
            exit('包路径错误:' + package_path)

    @staticmethod
    def fir(package_path, description, app_name, app_version, app_build):
        """
        上传fir
        ：package_path：包文件路径地址（本地文件地址）
        ：description： 本次更新描述信息
        """
        print("路径：" + package_path)
        if package_path:
            # https://www.betaqr.com/docs 上报文档
            data = {
                'api_token': FIR_API_TOKEN,
                'type': 'ios',
                'bundle_id': 'tech.brainco.focusimprove'
            }
            authAsk = requests.post(
                'http://api.bq04.com/apps',
                data=json.dumps(data),
                headers={'Content-Type': 'application/json'})
            if authAsk.status_code == 201:
                response = authAsk.json()
                files = {'file': open(package_path, 'rb')}
                uploadData = {
                    'key': response['cert']['binary']['key'],
                    'token': response['cert']['binary']['token'],
                    'x:name': app_name,
                    'x:version': app_version,
                    'x:build': app_build,
                    'x:release_type': 'Adhoc',
                    'x:changelog': description,
                }
                uploadUrl = response['cert']['binary']['upload_url']
                upload = requests.post(uploadUrl, data=uploadData, files=files)
                print(upload.text)
                print(upload.status_code)
                if upload.status_code == 200:
                    # 打开浏览器
                    webbrowser.open(fir_ipa_download_url,
                                    new=1,
                                    autoraise=True)
                else:
                    exit('fir上报ipa错误')
            else:
                exit('fir获取上报路径错误')
        else:
            exit('包路径错误:' + package_path)

    @staticmethod
    def appstore(package_path):
        """
        上传appstore
        ：package_path：包路径
        """
        os.system('xcrun altool --upload-app -f ' + package_path + ' -u ' +
                  DEVELOP_APPID + ' -p ' + DEVELOP_APPID_SECRET)


if __name__ == '__main__':
    """打包提交检测"""
    # 上传平台
    upload_appstore = AccessInformation.platform_upload_AppStore()
    ipa_path = input('请输入要上传ipa包的本机地址路径,[或Q退出]：')
    if ipa_path.upper() == 'Q':
        exit()
    if not ipa_path:
        exit("\n\n===========没有找到对应的ipa===========")
    if upload_appstore:
        print("\n\n===========开始上传AppStore===========")
        UploadIpaApk.appstore(ipa_path)
    else:
        print("\n\n===========开始上传蒲公英操作===========")
        UploadIpaApk.pugongying(ipa_path, '上传的新包')
