"""
@Author: your name
@Date: 2020-05-27 16:12:57
LastEditTime: 2020-12-14 14:36:02
LastEditors: Cao Shixin
@Description: iOS自动打包并导出工具
@FilePath: /package/git_branch_change.py
"""
import os
import subprocess
import time


class AutoPackage(object):
    """自动打包并导出文件"""

    def __init__(self, project_base_path, package_envior, package_path,
                 package_plist_file, project_name):
        # flutter项目根路径
        self.project_base_path = project_base_path
        # 打包的ipa生成路径（父级目录即可）
        self.package_path = package_path
        # 打包环境
        self.package_envior = package_envior
        # 手动打包配置文件信息文件地址
        self.package_plist_file = package_plist_file
        # 项目的文件名
        self.project_name = project_name
        self.package()

    def package(self):
        """
        打包只调用这个方法就好了
        """
        self.clean()
        # 删除之前的文件
        subprocess.call(['rm', '-rf', '%s' % self.package_path])
        time.sleep(1)
        # 创建文件夹存放打包文件
        subprocess.call(['mkdir', '-p', '%s' % self.package_path])
        time.sleep(1)
        self.archive()
        self.export_ipa()

    def clean(self):
        """
        项目初始化清理
        """
        print("\n\n===========开始clean操作===========")
        start = time.time()
        clean_command = 'xcodebuild clean -workspace %s/ios/%s.xcworkspace -scheme %s -configuration %s' % (
            self.project_base_path, self.project_name, self.project_name,
            self.package_envior)
        clean_command_run = subprocess.Popen(clean_command, shell=True)
        clean_command_run.wait()
        end = time.time()
        # Code码
        clean_result_code = clean_command_run.returncode
        if clean_result_code != 0:
            print("=======clean失败,用时:%.2f秒=======" % (end - start))
            exit('\n---------------clean失败了---------------')
        else:
            print("=======clean成功,用时:%.2f秒=======" % (end - start))

    def archive(self):
        """
        archive操作
        """
        print("\n\n===========开始archive操作===========")
        start = time.time()
        archive_command = 'xcodebuild archive -workspace %s/ios/%s.xcworkspace -scheme %s -configuration %s -archivePath %s/archive' % (
            self.project_base_path, self.project_name, self.project_name,
            self.package_envior, self.package_path)
        archive_command_run = subprocess.Popen(archive_command, shell=True)
        archive_command_run.wait()
        end = time.time()
        # Code码
        archive_result_code = archive_command_run.returncode
        if archive_result_code != 0:
            print("=======archive失败,用时:%.2f秒=======" % (end - start))
            exit('\n---------------archive失败---------------')
        else:
            print("=======archive成功,用时:%.2f秒=======" % (end - start))

    def export_ipa(self):
        """
        导出ipa包
        """
        # 导出IPA
        print("\n\n===========开始export操作===========")
        print("\n\n==========请你耐心等待一会~===========")
        start = time.time()

        export_command = 'xcodebuild -exportArchive -archivePath %s/archive.xcarchive -exportPath %s -exportOptionsPlist %s.plist' % (
            self.package_path, self.package_path,
            self.package_plist_file)
        print('===========%s' % export_command)
        export_command_run = subprocess.Popen(export_command, shell=True)

        export_command_run.wait()
        end = time.time()
        # Code码
        export_result_code = export_command_run.returncode
        if export_result_code != 0:
            print("=======导出IPA失败,用时:%.2f秒=======" % (end - start))
            exit('\n---------------导出IPA失败---------------')
        else:
            print("=======导出IPA成功,用时:%.2f秒=======" % (end - start))
            # 删除archive.xcarchive文件
            # subprocess.call(
            #     ['rm', '-rf',
            #      '%s/archive.xcarchive' % (self.package_path)])
