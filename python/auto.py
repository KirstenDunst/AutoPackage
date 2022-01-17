'''
Author: Cao Shixin
Date: 2022-01-14 17:36:28
LastEditors: Cao Shixin
LastEditTime: 2022-01-17 11:13:01
Description: 定时打包调用
'''
from main_setting import MainSettings
from git_branch import GitBranch
from main import Package

# from file_folder_operate import FileFolderOperate

if __name__ == '__main__':
    
    hf_settings = MainSettings()
    # test_path = hf_settings.export_plist_father_path + '/test.txt'
    # FileFolderOperate.ensure_file(test_path)
    # str = "abcd"
    # with open(test_path, mode='a+', encoding="utf-8") as w:
    #     w.write(str + "\n")
    
    temp_path_file = hf_settings.export_plist_father_path + '/nearly_git_commit.txt'
    content = ''
    if temp_path_file:
        with open(temp_path_file) as file_obj:
            content = file_obj.read()

    # 获取远端的最新分支代码,返回最近三次提交记录log
    nearlyThreeMessage = GitBranch(
        hf_settings.project_base_path, hf_settings.export_plist_father_path,
        'morpheus_app 项目').branch_change(branch_name='origin/develop')
    if not content == nearlyThreeMessage:
        Package().package(nearlyThreeMessage, False, 'Profile', hf_settings)
    else:
        print('暂无新提交代码，忽略本次打包')
