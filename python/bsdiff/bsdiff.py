'''
Author: Cao Shixin
Date: 2019-11-29 17:22:10
LastEditors: Cao Shixin
LastEditTime: 2022-04-11 16:32:35
Description: 
'''
# 导入文件
import json
import os
import shutil
import sys
import time
from turtle import update

sys.path.append('/Users/caoshixin/Desktop/AutoPackage')
from AutoPackage.python.bsdiff.bsdiff_setting import DiffSetting
from AutoPackage.python.md5 import MD5Helper
from AutoPackage.python.access_infor import AccessInformation
from AutoPackage.python.zip import ZipUnZip


def hotfix_run(hf_settings: DiffSetting, hot_version, hot_evior,
               need_deal_zip_path: str):
    """执行热更新差分包处理"""
    base_path = hf_settings.base_path + '/' + hot_evior + '/' + hot_version + '/'

    # 执行计算当前需要添加的文件目录(一次计算出来的，从低到高处理,每个版本设定最大1000个热更新包)
    current_number = 0
    while current_number <= 1000:
        last_path = base_path + str(current_number)
        if not os.path.exists(last_path):
            break
        else:
            current_number += 1

    print('资源存放路径：' + last_path)
    os.makedirs(last_path)

    zip_name = need_deal_zip_path.split('/')[-1].split('.')[0]
    origin_zip_path = last_path + '/' + zip_name + '_origin.zip'
    shutil.copy(need_deal_zip_path, origin_zip_path)
    # 解压缩
    ZipUnZip.unzip(origin_zip_path, last_path + '/')

    unzip_directory = last_path + '/' + zip_name
    # 遍历形成清单文件
    checksum_json = {}
    for parent, dirnames, filenames in os.walk(unzip_directory,
                                               followlinks=True):
        for filename in filenames:
            # 遍历所有的文件名filename
            # 文件的绝对路径
            file_path = os.path.join(parent, filename)
            # 文件的相对路径
            relative_path = str(file_path).replace(unzip_directory + '/', '')
            # 排除mac的文件夹生成的配置信息
            if filename == '.DS_Store':
                os.remove(file_path)
            elif filename in [
                    'resource-bundle.manifest', 'last-commit', 'www.zip'
            ]:
                print(filename + ':不计入资源完备文件的md5值')
            else:
                checksum_json[relative_path] = MD5Helper.get_file_md5(
                    file_path)

    hf_settings.manifest_map['checksum'] = checksum_json
    version_str = hot_version + '.' + time.strftime("%Y%m%d%H%M%S",
                                                    time.localtime())
    hf_settings.manifest_map['version'] = version_str
    manifest_name = unzip_directory + '/' + hf_settings.mainfest_name
    with open(manifest_name, 'w', encoding='utf-8') as f_obj:
        json.dump(hf_settings.manifest_map,
                  f_obj,
                  ensure_ascii=False,
                  indent=4)
    print('保存清单文件成功')

    # 压缩生成新的zip文件
    ZipUnZip.zip(unzip_directory, last_path + '/' + zip_name + '.zip')

    manifest_md5 = MD5Helper.get_file_md5(manifest_name)

    # 移除过程中zip文件以及中转文件
    shutil.rmtree(last_path + '/' + zip_name)
    os.remove(origin_zip_path)

    now_zip_path = last_path + '/' + zip_name + '.zip'
    now_zip_md5 = MD5Helper.get_file_md5(now_zip_path)

    if current_number != 0:
        # # 获取包含py的文件夹位置
        # now_file_path = os.path.dirname(os.path.realpath(__file__))
        if not os.path.exists(setting.bsdiff_path + '/Makefile'):
            os.system('cd' + ' ' + setting.bsdiff_path + '/bsdiff' +
                      ' && make')

        patch_path = last_path + '/' + 'patch'
        if not os.path.exists(patch_path):
            os.makedirs(patch_path)

        # 循环差量包生成制作
        for number in range(0, current_number, 1):
            print('差量包生成文件夹次数：' + str(number))
            old_zip_path = base_path + str(number) + '/' + zip_name + '.zip'
            old_zip_md5 = MD5Helper.get_file_md5(old_zip_path)
            if now_zip_md5 != old_zip_md5:
                now_patch_path = last_path + '/patch/' + old_zip_md5 + '.patch'
                # 差量包生成器
                os.system(setting.bsdiff_path + '/bsdiff ' + old_zip_path +
                          ' ' + now_zip_path + ' ' + now_patch_path)
            else:
                print('当前%s和最新的zip包内容一样, 请确认最新包是否正确？' % (number))
    else:
        now_zip_path = base_path + '0/' + zip_name + '.zip'

    # oss清单文件
    hf_settings.oss_map['bundleArchiveChecksum'] = now_zip_md5
    hf_settings.oss_map['bundleManifestChecksum'] = manifest_md5
    hf_settings.oss_map['version'] = hot_version
    update_json = last_path + '/' + hf_settings.oss_name
    with open(update_json, 'w', encoding='utf-8') as f_obj:
        json.dump(hf_settings.oss_map, f_obj, ensure_ascii=False, indent=4)
    print('保存oss配置资源样例文件成功')


if __name__ == '__main__':

    hot_fix_base = '/Users/caoshixin/Desktop/AutoPackage/starkidapp_hotfix'
    # hot_fix_base = input('输入热更新操作的跟文件目录：')
    setting = DiffSetting(hot_fix_base)
    # evior = 'develop'
    evior = AccessInformation.get_diff_evior()
    # hot_version = '3.1.0'
    hot_version = input('差分处理版本号：')

    # need_deal_zip_path = '/Users/caoshixin/Desktop/dist.zip'
    need_deal_zip_path = input('需要进行操作的zip文件路径:')

    hotfix_run(setting, hot_version, evior, need_deal_zip_path)
