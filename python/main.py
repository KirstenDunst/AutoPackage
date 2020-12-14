'''
@Author: Cao Shixin
@Date: 2020-05-27 19:54:39
LastEditors: Cao Shixin
LastEditTime: 2020-12-08 18:41:19
@Description: 自动打包根项目，运行这个即可
@Email: cao_shixin@yahoo.com
@Company: BrainCo
'''
import os
from access_infor import AccessInformation
from git_branch import GitBranch
from upload_ipa_apk import UploadIpaApk
from main_setting import MainSettings
from auto_package_ios import AutoPackage
from file_folder_operate import FileFolderOperate
from buddy_plist import BuddyPlist

if __name__ == '__main__':

    hf_settings = MainSettings()
    # 自动打包
    description = ''

    # 获取远端的最新分支代码
    GitBranch(hf_settings.project_base_path, 'flutter world 项目')

    # 获取项目名
    project_name = FileFolderOperate.get_project_name(
        hf_settings.project_base_path)

    # 获取打包环境s
    package_envior = 'Release'
    # 上传平台
    upload_appstore = AccessInformation.platform_upload_AppStore()
    if not upload_appstore:
        description = input("请输入打包版本更新内容:")
        package_envior = AccessInformation.get_packaging_enviorment()
        description = package_envior + '环境: ' + description

    # 根据环境来判定是否需要开启文件替换
    if package_envior != 'Release':
        FileFolderOperate.replaceText(
            hf_settings.project_base_path + '/lib/provider/app_provider.dart',
            '_appstoreReview = localReview;', '_appstoreReview = false;')
        # FileFolderOperate.replaceText(hf_settings.project_base_path+'/lib/ui/widget/config_entry_widget.dart','!kReleaseMode','true')

    # 包导出的签名形式文件名获取
    package_sign_plist = AccessInformation.get_package_export_plist(
        upload_appstore)

    try:
        os.system('cd' + ' ' + hf_settings.project_base_path)
        submodule_file = hf_settings.project_base_path + '/modules'
        if os.path.exists(submodule_file):
            canUpdateModule = input('是否需要更新项目主依赖的submodule？T:更新，F:不更新。[T/F]')
            if canUpdateModule.upper() == 'T':
                print('=========执行submodule更新========')
                os.system(
                    'git submodule update --init --recursive && git submodule update --recursive --remote --rebase'
                )

        # pubspec_lock_file_path = hf_settings.project_base_path + '/pubspec.lock'
        # if os.path.exists(pubspec_lock_file_path):
        #     print('-----------删除pubspec的lock文件------------')
        #     os.remove(pubspec_lock_file_path)

        print('-====================pubspec更新=================')
        os.system('flutter pub get && flutter build ios --' +
                  package_envior.lower())
    except Exception as e:
        exit('出错了，出师不利，什么问题：' + e)

    project_name = FileFolderOperate.get_project_name(
        hf_settings.project_base_path)
    AutoPackage(hf_settings.project_base_path, package_envior,
                hf_settings.package_path, package_sign_plist, project_name)

    print("===========开始准备上传操作，请注意！！！！============")
    # 包名
    package_name = FileFolderOperate.get_special_suffix_file_name(
        hf_settings.package_path, 'ipa')
    ipa_path = '%s/%s.ipa' % (hf_settings.package_path, package_name)
    print("路径：" + ipa_path)
    if ipa_path:
        if upload_appstore:
            print("\n\n===========开始上传AppStore===========")
            UploadIpaApk.appstore(ipa_path)
        else:
            if package_envior == 'Release':
                package_info_plist_path = ipa_path + '/archive.xcarchive/Products/Applications/' + project_name + '/info.plist'
                app_name = BuddyPlist.getBundleName
                app_version = BuddyPlist.getBundleVersion
                app_build_num = BuddyPlist.getBundleBuild
                print('\n\n===========开始上传fir操作=app_name:%s=app_version:%s=app_build_num:%s========'%(app_name,app_version,app_build_num))
                UploadIpaApk.fir(ipa_path, description, app_name, app_version, app_build_num)
            else:
                print("\n\n===========开始上传蒲公英操作===========")
                UploadIpaApk.pugongying(ipa_path, description)
    else:
        exit("\n\n===========没有找到对应的ipa===========")
