'''
Author: Cao Shixin
Date: 2022-01-17 09:47:44
LastEditors: Cao Shixin
LastEditTime: 2022-01-17 11:22:38
Description: 定时任务执行脚本，执行一次即可，开启和关闭
'''
import os
from access_infor import AccessInformation
from main_setting import MainSettings
from file_folder_operate import FileFolderOperate

if __name__ == '__main__':
    open_or_close = AccessInformation.regular_packing()
    hf_settings = MainSettings()
    if open_or_close:
        # 清除历史遗留，保证记录都是本次的
        # out_log = hf_settings.export_plist_father_path + '/auto-out.log'
        # err_log = hf_settings.export_plist_father_path + '/auto-err.log'
        # if os.path.exists(out_log):
        #     os.remove(out_log)
        # if os.path.exists(err_log):
        #     os.remove(err_log)
        # FileFolderOperate.ensure_file(out_log)
        # FileFolderOperate.ensure_file(err_log)
        os.system('cd ~/Library/LaunchAgents')
        FileFolderOperate.replace_file(
            os.path.abspath('.') + '/' + hf_settings.regular_launchctl_name,
            hf_settings.export_plist_father_path + '/' +
            hf_settings.regular_launchctl_name)
        os.system('launchctl load ' + hf_settings.regular_launchctl_name)
    else:
        # 关闭定时任务
        # load:开启，unlopad：关闭，start：立即开启一次，stop：停止任务
        os.system('cd ~/Library/LaunchAgents && launchctl unload ' +
                  hf_settings.regular_launchctl_name)
