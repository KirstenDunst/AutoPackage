'''
Author: Cao Shixin
Date: 2021-06-10 13:58:14
LastEditors: Cao Shixin
LastEditTime: 2022-01-17 11:14:10
Description: 便捷获取包的一些配置信息
'''
import os
import re


class BuddyPlist:
    """
    便捷获取iOS的一些配置信息（主要是info里面的一些内容）
    """
    @staticmethod
    def getIpaInBrief(plist_file_path):
        bundleId = BuddyPlist.self_read(plist_file_path,
                                        "'Print :CFBundleIdentifier'")
        bundleName = BuddyPlist.self_read(plist_file_path,
                                          "'Print :CFBundleName'")
        bundleVersion = BuddyPlist.self_read(
            plist_file_path, "'Print :CFBundleShortVersionString'")
        bundleBuild = BuddyPlist.self_read(plist_file_path,
                                           "'Print :CFBundleVersion'")
        return {
            'bundleId': bundleId.replace('\n', ''),
            'bundleName': bundleName.replace('\n', ''),
            'bundleVersion': bundleVersion.replace('\n', ''),
            'bundleBuild': bundleBuild.replace('\n', ''),
        }

    @staticmethod
    def getIpaInDetail(plist_file_path):
        """
        将plist内部的信息打印出来
        """
        return BuddyPlist.self_read(plist_file_path, 'print')

    @staticmethod
    def self_read(plist_file_path, param):
        """
        任意操作
        """
        out = os.popen('/usr/libexec/PlistBuddy -c %s %s' %
                       (param, plist_file_path))
        result = out.read()
        return result


class ApkInfo:
    """获取apk的信息"""
    @staticmethod
    def getApkInBrief(apkPath):
        '''
        简介包信息
        '''
        content = ApkInfo.getApkInDetail(apkPath)
        match = re.compile(
            "package: name='(\S+)' versionCode='(\d+)' versionName='(\S+)' compileSdkVersion='(\d+)'"
        ).match(content)
        if not match:
            raise Exception("apk can't get brief")
        match_label = re.search("application: label='(\S+)'", content, flags=0)
        if not match_label:
            raise Exception("apk can't get label")
        # 包名
        packageName = match.group(1)
        # build
        versionCode = match.group(2)
        # version
        versionName = match.group(3)
        compileSdkVersion = match.group(4)
        # 应用名
        label = match_label.group(1)
        return {
            'packageName': packageName,
            'versionCode': versionCode,
            'versionName': versionName,
            'compileSdkVersion': compileSdkVersion,
            'label': label
        }

    @staticmethod
    def getApkInDetail(apkPath):
        '''
        详细获取包的所有信息
        return： 字符串类型
        '''
        out = os.popen('aapt dump badging %s' % (apkPath))
        result = out.read()
        return result


if __name__ == '__main__':

    apk_path = input('apk文件路径：')
    content = ApkInfo.getApkInBrief(apkPath=apk_path)
    print('结果信息:%s' % (content))

    plist_path = input('测试plist的路径：')
    all_content = BuddyPlist.getIpaInDetail(plist_path)
    print('detail_all: ' + all_content)

    result1 = BuddyPlist.getIpaInBrief(plist_path)
    print('brief: ' + result1)
