"""
Author: your name
Date: 2020-08-20 15:49:22
LastEditTime: 2020-12-04 15:51:30
LastEditors: Cao Shixin
Description: 作内容迁移的文件替换操作
FilePath: /package_improve/replace_content.py
"""
import os
import shutil


class FileFolderOperate:
    @staticmethod
    def replace_text(file_path, origin_str, replace_str):
        """
        替换文件中的某一类文字替换
        """
        if os.path.exists(file_path):
            f1 = open(file_path, "r")
            content = f1.read()
            f1.close()
            t = content.replace(origin_str, replace_str)
            with open(file_path, "w") as f2:
                f2.write(t)
        else:
            exit("文件路径不存在")

    @staticmethod
    def replace_file(file_path_replace, file_path_new):
        """
        文件替换
        :file_path_replace: 要被替换的文件地址
        :file_path_new: 要替换成的文件地址
        """
        if not os.path.exists(file_path_new):
            exit("要替换成的文件地址不存在")
        if os.path.exists(file_path_replace):
            os.remove(file_path_replace)
        shutil.copy(file_path_new, file_path_replace)

    @staticmethod
    def replace_folder(folder_path_replace, folder_path_new):
        """
        文件夹替换
        :folder_path_replace: 要被替换的文件夹地址
        :folder_path_new: 要替换成的文件夹地址
        """
        FileFolderOperate.del_folder_all(folder_path_replace)
        FileFolderOperate.copy_folder_all(folder_path_new, folder_path_replace)

    @staticmethod
    def del_folder_all(filepath):
        """
        删除某一目录下的所有文件或文件夹
        :param filepath: 路径
        :return:
        """
        del_list = os.listdir(filepath)
        for f in del_list:
            file_path = os.path.join(filepath, f)
            if os.path.isfile(file_path):
                os.remove(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)

    @staticmethod
    def copy_folder_all(folder_path, target_folder):
        """
        将目标文件下的所有文件，文件夹拷贝到另一个文件夹下
        :folder_path: 有内容的文件夹路径
        :targetFolder: 要移到的目标文件夹路径
        """
        folder_path_files = os.listdir(folder_path)
        for file_name in folder_path_files:
            full_file_name = os.path.join(folder_path, file_name)
            if os.path.isfile(full_file_name):
                shutil.copy(full_file_name, target_folder)

    @staticmethod
    def ensure_file(file_path):
        """
        确认路径下文件存在，如果不存在会自动创建
        :file_path: 文件路径
        """
        # 将文件路径分割出来
        file_dir = os.path.split(file_path)[0]
        FileFolderOperate.ensure_folder(file_dir)
        if not os.path.exists(file_path):
            os.system(r'touch %s' % file_path)

    @staticmethod
    def ensure_folder(folder_path):
        """
        确认文件夹是否存在，没有存在会自动创建
        :folder_path: 文件夹路径
        """
        if not os.path.isdir(folder_path):
            os.makedirs(folder_path)

    @staticmethod
    def get_project_name(project_base_path):
        """获取工程的项目名"""
        return FileFolderOperate.get_special_suffix_file_name(
            project_base_path + '/ios/', 'xcodeproj')

    @staticmethod
    def get_special_suffix_file_name(package_parent_path, suffix):
        """获取特定文件夹下指定后缀的文件名
        package_parent_path：指定文件夹路径
        suffix：后缀
        """
        file_names = os.listdir(package_parent_path)
        contentSuffix = '.' + suffix
        for filename in file_names:
            if contentSuffix in filename:
                return filename.replace(contentSuffix, '')
        exit('请放置正确的iOS项目，并核对配置项中项目路径是否正确')
