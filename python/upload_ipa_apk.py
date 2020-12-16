"""
@Author: Cao Shixin
@Date: 2020-05-27 19:54:39
LastEditors: Cao Shixin
LastEditTime: 2020-12-14 15:58:50
@Description: 包上传工具
@Email: cao_shixin@yahoo.com
@Company: BrainCo
"""
import os
import webbrowser
import requests
import json


class UploadIpaApk:
    """
    上传包处理
    """

    @staticmethod
    def pgyer(package_path, description, api_key, pgyer_ipa_download_url):
        """
        上传蒲公英
        ：package_path：包文件路径地址（本地文件地址）
        ：description： 本次更新描述信息
        """
        print("\n\n===========开始上传蒲公英操作===========")
        if package_path:
            # https://www.pgyer.com/doc/api 具体参数可以进去里面查看,
            url = 'https://www.pgyer.com/apiv2/app/upload'
            data = {
                '_api_key': api_key,
                'installType': '1',
                'buildUpdateDescription': description
            }
            files = {'file': open(package_path, 'rb')}
            r = requests.post(url, data=data, files=files)
            if r.status_code == 200:
                # 打开浏览器
                webbrowser.open(pgyer_ipa_download_url,
                                new=1,
                                autoraise=True)
        else:
            exit('\n=================包路径错误:' + package_path)

    @staticmethod
    def fir(package_path, description, app_name, app_version, app_build, build_id, fir_api_token, fir_ipa_download_url):
        """
        上传fir
        ：package_path：包文件路径地址（本地文件地址）
        ：description： 本次更新描述信息
        """
        print('\n\n===========开始上传fir操作=app_name:%s=app_version:%s========' %
              (app_name, app_version))
        if package_path:
            # https://www.betaqr.com/docs 上报文档
            data = {
                'api_token': fir_api_token,
                'type': 'ios',
                'bundle_id': build_id
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
                    exit('\n===============fir上报ipa错误===============')
            else:
                exit('\n================fir获取上报路径错误=================')
        else:
            exit('\n====================包路径错误:' + package_path)

    @staticmethod
    def appstore(package_path, app_id, app_secret):
        """
        上传appstore
        ：package_path：包路径
        """
        os.system('xcrun altool --upload-app -f ' + package_path + ' -u ' +
                  app_id + ' -p ' + app_secret)
