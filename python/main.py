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
    package_environment = 'Release'
    # 上传平台
    upload_appstore = AccessInformation.platform_upload_appstore()
    if not upload_appstore:
        description = input("请输入打包版本更新内容:")
        package_environment = AccessInformation.get_package_environment()
        description = package_environment + '环境: ' + description
        # 开启文件替换
        FileFolderOperate.replace_text(
            hf_settings.project_base_path + '/lib/provider/app_provider.dart',
            '_appstoreReview = localReview;', '_appstoreReview = false;')

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
                  package_environment.lower())
    except Exception as e:
        exit('出错了，出师不利，什么问题：%s' % e)

    project_name = FileFolderOperate.get_project_name(hf_settings.project_base_path)
    AutoPackage(hf_settings.project_base_path, package_environment, hf_settings.package_path,
                '%s/%s' % (hf_settings.export_plist_father_path, package_sign_plist), project_name)

    print("===========开始准备上传操作，请注意！！！！============")
    # 包名
    package_name = FileFolderOperate.get_special_suffix_file_name(
        hf_settings.package_path, 'ipa')
    ipa_path = '%s/%s.ipa' % (hf_settings.package_path, package_name)
    print("路径：" + ipa_path)

    package_info_plist_path = hf_settings.package_path + '/archive.xcarchive/Products/Applications/' + project_name + '.app/Info.plist'
    app_name = BuddyPlist.get_bundle_name(package_info_plist_path)
    app_version = BuddyPlist.get_bundle_version(package_info_plist_path)
    app_build_num = BuddyPlist.get_bundle_build(package_info_plist_path)
    app_build_id = BuddyPlist.get_bundle_id(package_info_plist_path)

    if ipa_path:
        if upload_appstore:
            print("\n\n===========开始上传AppStore===========")
            # 项目里面已经处理release模式自动上传bugly符号表
            # python.symbol_table.SymbolTable.bugly(
            #     hf_settings.package_path + '/' + project_name + '.app.dSYM',
            #     app_build_id, '%s%s' % (app_version, app_build_num), hf_settings.BUGLY_APP_ID, hf_settings.BUGLY_APP_KEY)
            UploadIpaApk.appstore(ipa_path, hf_settings.APPSTORE_APP_ID, hf_settings.APPSTORE_APP_ID_SECRET)
        else:
            if package_environment == 'Release':
                UploadIpaApk.fir(ipa_path, description, app_name, app_version, app_build_num, app_build_id,
                                 hf_settings.FIR_API_TOKEN, hf_settings.FIR_IPA_DOWNLOAD_URL)
            else:
                UploadIpaApk.pgyer(ipa_path, description, hf_settings.PGYER_API_KEY, hf_settings.PGYER_IPA_DOWNLOAD_URL)
    else:
        exit("\n\n===========没有找到对应的ipa===========")
