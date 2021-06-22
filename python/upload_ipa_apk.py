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
                webbrowser.open(pgyer_ipa_download_url, new=1, autoraise=True)
        else:
            exit('\n=================包路径错误:' + package_path)

    @staticmethod
    def fir(package_path,
            icon_path,
            description,
            app_name,
            app_version,
            app_build,
            build_id,
            fir_api_token,
            fir_ipa_download_url,
            release_type=''):
        """
        上传fir
        ：package_path：包文件路径地址（本地文件地址）
        ：description： 本次更新描述信息
        """
        print('\n\n===========开始上传fir操作=app_name:%s=app_version:%s========' %
              (app_name, app_version))
        if package_path:
            # https://www.betaqr.com/docs 上报文档
            data = {'api_token': fir_api_token, 'bundle_id': build_id}
            # ios 或者 android,这里用release_type来判断区分了
            if release_type:
                data['type'] = 'ios'
            else:
                data['type'] = 'android'

            authAsk = requests.post(
                'http://api.bq04.com/apps',
                data=json.dumps(data),
                headers={'Content-Type': 'application/json'})
            if authAsk.status_code == 201:
                response = authAsk.json()
                uploadData = {
                    'key': response['cert']['binary']['key'],
                    'token': response['cert']['binary']['token'],
                    'x:name': app_name,
                    'x:version': app_version,
                    'x:build': app_build,
                    'x:changelog': description,
                }
                if release_type:
                    # 打包类型，只针对 iOS (Adhoc, Inhouse)（上传 ICON 时不需要）
                    uploadData['x:release_type'] = release_type
                uploadUrl = response['cert']['binary']['upload_url']
                # 上传包文件
                upload_file = requests.post(
                    uploadUrl,
                    data=uploadData,
                    files={'file': open(package_path, 'rb')})
                # 上传icon图标
                upload_icon = requests.post(
                    response['cert']['icon']['upload_url'],
                    data={
                        'key': response['cert']['icon']['key'],
                        'token': response['cert']['icon']['token']
                    },
                    files={'file': open(icon_path, 'rb')})

                if upload_file.status_code == 200 and upload_icon.status_code == 200:
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


if __name__ == '__main__':
    file_path = input('输入文件路径:')
    description = input('输入打包上传描述:')
    pgyer_api_key = input('蒲公英api_key:')
    pgyer_upload_url = input('蒲公英app的下载链接地址：')
    UploadIpaApk.pgyer(file_path, description,
                       '023dfffebb5e4f4b7f03898cd2b0aa62',
                       'https://www.pgyer.com/Tu0q')
