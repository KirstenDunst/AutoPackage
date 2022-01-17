"""
@Author: Cao Shixin
@Date: 2020-05-27 19:54:39
LastEditors: Cao Shixin
LastEditTime: 2020-12-14 16:31:24
@Description: 自动打包根项目，运行这个即可
@Email: cao_shixin@yahoo.com
@Company: BrainCo
"""
import os
from access_infor import AccessInformation
from git_branch import GitBranch
from upload_ipa_apk import UploadIpaApk
from main_setting import MainSettings
from auto_package_ios import AutoPackage
from file_folder_operate import FileFolderOperate
from buddy_plist import BuddyPlist
from buddy_plist import ApkInfo
from send_message import SendMessage


class Package(object):
    def __init__(self, *args):
        super(Package, self).__init__(*args)

    @staticmethod
    def package(description: str, upload_appstore: bool,
                package_environment: str, hf_settings: MainSettings):
        try:
            os.system('cd' + ' ' + hf_settings.project_base_path)
            submodule_file = hf_settings.project_base_path + '/modules'
            if os.path.exists(submodule_file):
                canUpdateModule = input(
                    '是否需要更新项目主依赖的submodule？T:更新，F:不更新。[T/F]')
                if canUpdateModule.upper() == 'T':
                    print('=========执行submodule更新========')
                    os.system(
                        'git submodule update --init --recursive && git submodule update --recursive --remote --rebase'
                    )

            print('-====================pubspec更新=================')
            os.system('flutter clean && flutter pub get')

            print('-====================编译Android包=================')
            FileFolderOperate.del_folder_all(hf_settings.android_package_path)
            FileFolderOperate.ensure_folder(hf_settings.android_package_path)
            os.system('flutter build apk --' + package_environment.lower() +
                      ' && mv ' + hf_settings.project_base_path +
                      '/build/app/outputs/flutter-apk/app-' +
                      package_environment.lower() + '.apk ' +
                      hf_settings.android_package_path)

            print('-====================编译iOS包=================')
            os.system('flutter build ios --' + package_environment.lower())
        except Exception as e:
            exit('出错了，出师不利，error：%s' % e)

        # 获取项目名
        project_name = FileFolderOperate.get_project_name(
            hf_settings.project_base_path)
        # 包导出的签名形式文件名获取
        package_sign_plist = AccessInformation.get_package_export_plist(
            upload_appstore, package_environment)
        AutoPackage(
            hf_settings.project_base_path, package_environment,
            hf_settings.ipa_package_path, '%s/%s' %
            (hf_settings.export_plist_father_path, package_sign_plist),
            project_name)

        print("===========开始准备上传操作，请注意！！！！============")
        # 包名
        package_name = FileFolderOperate.get_special_suffix_file_name(
            hf_settings.ipa_package_path, 'ipa')
        ipa_path = '%s/%s.ipa' % (hf_settings.ipa_package_path, package_name)
        print('ios包ipa路径：' + ipa_path)
        ipa_info_plist_path = hf_settings.ipa_package_path + '/archive.xcarchive/Products/Applications/' + project_name + '.app/Info.plist'
        ipa_info = BuddyPlist.getIpaInBrief(ipa_info_plist_path)
        print('ipa包简介信息：%s' % (ipa_info))

        apk_path = hf_settings.android_package_path + '/app-' + package_environment.lower(
        ) + '.apk'
        print('安卓包apk路径：' + apk_path)
        apk_info = ApkInfo.getApkInBrief(apk_path)
        print('apk包信息简介：%s' % (apk_info))

        if ipa_path and apk_path:
            if upload_appstore:
                print("\n\n===========开始上传AppStore===========")
                UploadIpaApk.appstore(ipa_path, hf_settings.APPSTORE_API_KEY,
                                      hf_settings.APPSTORE_API_ISSUER)
            else:
                if package_environment == 'Release':
                    UploadIpaApk.fir(apk_path, hf_settings.icon_path,
                                     description, apk_info['label'],
                                     apk_info['versionName'],
                                     apk_info['versionCode'],
                                     apk_info['packageName'],
                                     hf_settings.FIR_API_TOKEN,
                                     hf_settings.FIR_IPA_DOWNLOAD_URL)
                    UploadIpaApk.fir(ipa_path,
                                     hf_settings.icon_path,
                                     description,
                                     ipa_info['bundleName'],
                                     ipa_info['bundleVersion'],
                                     ipa_info['bundleBuild'],
                                     ipa_info['bundleId'],
                                     hf_settings.FIR_API_TOKEN,
                                     hf_settings.FIR_IPA_DOWNLOAD_URL,
                                     release_type='Adhoc')
                else:
                    UploadIpaApk.pgyer(apk_path, description,
                                       hf_settings.PGYER_API_KEY,
                                       hf_settings.PGYER_IPA_DOWNLOAD_URL)
                    UploadIpaApk.pgyer(ipa_path, description,
                                       hf_settings.PGYER_API_KEY,
                                       hf_settings.PGYER_IPA_DOWNLOAD_URL)
        else:
            exit("\n\n===========没有找到对应的ipa和apk===========")

        # 上传完成发送通知
        if upload_appstore:
            print(
                "\n\n===========上传AppStore完成，请前往App Store Connect查看==========="
            )
        else:
            linkUrl = hf_settings.FIR_IPA_DOWNLOAD_URL if package_environment == 'Release' else hf_settings.PGYER_IPA_DOWNLOAD_URL
            SendMessage.send_ding_talk_link(
                'https://oapi.dingtalk.com/robot/send?access_token=%s' %
                (hf_settings.DING_TALK_TOKEN),
                linkUrl,
                picUrl='https://app.brainco.cn/morpheus/mobile/icon.png',
                title='%sAndroid&iOS-%s-%s更新通知' %
                (ipa_info['bundleName'], ipa_info['bundleVersion'],
                 package_environment),
                text=description)


if __name__ == '__main__':

    hf_settings = MainSettings()
    # 自动打包上传描述信息
    description = ''
    # 获取打包环境
    package_environment = 'Release'
    # 获取远端的最新分支代码
    nearlyThreeMessage = GitBranch(hf_settings.project_base_path,
                                   hf_settings.export_plist_father_path,
                                   'focus_world 项目').branch_change()
    # 是否是上传appstore
    upload_appstore = False
    # 打包模式快速响应设置
    quick_package = AccessInformation.packaging_mode()
    if quick_package:
        # 平时用的快速打包方式，只用选一个git分支，默认profile模式，git最近三次commit，上传蒲公英
        package_environment = 'Profile'
        description = nearlyThreeMessage
        upload_appstore = False
    else:
        # 上传平台
        upload_appstore = AccessInformation.platform_upload_appstore()
        if upload_appstore:
            package_environment = 'Release'
        else:
            description = input("请输入打包版本更新内容(不输入回车默认读取git提交最近记录三条):")
            if len(description) == 0:
                description = nearlyThreeMessage
            package_environment = AccessInformation.get_package_environment()

    description = package_environment + '环境: ' + description

    Package().package(description, upload_appstore, package_environment,
                      hf_settings)
