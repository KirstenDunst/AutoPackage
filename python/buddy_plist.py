'''
Author: Cao Shixin
Date: 2020-12-06 15:20:38
LastEditors: Cao Shixin
LastEditTime: 2020-12-08 18:20:37
Description: 便捷获取iOS的一些配置信息
'''
import os


class BuddyPlist:
    """
    便捷获取iOS的一些配置信息（主要是info里面的一些内容）
    """
    @staticmethod
    def get_print_plist(plist_path):
        """
        将plist内部的信息打印出来
        """
        return BuddyPlist.self_read(plist_path, 'print')

    @staticmethod
    def getBundleID(plist_path):
        """
        获取BundId : CFBundleIdentifier
        """
        return BuddyPlist.self_read(plist_path, "'Print :CFBundleIdentifier'")

    @staticmethod
    def getBundleName(plist_path):
        """
        获取BundName : CFBundleName
        """
        return BuddyPlist.self_read(plist_path, "'Print :CFBundleName'")

    @staticmethod
    def getBundleVersion(plist_path):
        """
        获取BundleVersion : CFBundleShortVersionString
        """
        return BuddyPlist.self_read(plist_path,
                                    "'Print :CFBundleShortVersionString'")

    @staticmethod
    def getBundleBuild(plist_path):
        """
        获取BundBuild : CFBundleVersion
        """
        return BuddyPlist.self_read(plist_path, "'Print :CFBundleVersion'")

    @staticmethod
    def self_read(plist_path, param):
        """
        任意操作
        """
        out = os.popen('/usr/libexec/PlistBuddy -c %s %s' %
                       (param, plist_path))
        result = out.read()
        return result


if __name__ == '__main__':
    plist_path = input('测试plist的路径：')
    all_content = BuddyPlist.get_print_plist(plist_path)
    print('all_content: ' + all_content)

    result1 = BuddyPlist.getBundleID(plist_path)
    print('BundleID: ' + result1)

    result2 = BuddyPlist.getBundleName(plist_path)
    print('bundleName: ' + result2)

    result3 = BuddyPlist.getBundleVersion(plist_path)
    print('BundleVersion: ' + result3)

    result4 = BuddyPlist.getBundleBuild(plist_path)
    print('BundleBuild: ' + result4)
