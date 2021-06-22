"""
@Author: your name
@Date: 2020-05-27 16:12:57
LastEditTime: 2020-12-04 15:38:54
LastEditors: Cao Shixin
@Description: 代码的分支切换
@FilePath: /package/git_branch_change.py
"""

import os
import subprocess


class GitBranch(object):
    """
    git的分支切换和代码拉取
    """
    def __init__(self, project_path, temp_git_commit_path, project_alarm):
        # 项目根路径
        self.project_path = project_path
        # 临时保存git commit文件地址
        self.temp_git_commit_path = temp_git_commit_path
        # 提示语
        self.project_alarm = project_alarm

    # 执行分支切换操作
    def branch_change(self):
        """执行分支切换"""
        temp_branch_dict = self.__get_branchedits()
        temp_branch_list = self.__get_branchelists()

        branch_str = ''
        for key, value in temp_branch_dict.items():
            branch_str += (key + " : " + value + "\n")

        branch_select_key = input('请选择你想要打包使用的' + self.project_alarm +
                                  '远端代码分支\n' + branch_str + ':')
        branch_name_origin = temp_branch_dict[branch_select_key]
        branch_name_local = branch_name_origin.replace('origin/', '')
        print('选中的分支名：' + branch_name_origin)
        try:
            # 转到工程路径下
            os.chdir(self.project_path)
        except Exception as e:
            print("工程路径出错：%s" % e)
            exit()
        print(temp_branch_list)

        ensureAgain = input("请再次确认当前分支是否有没有提交的修改，选择分支将会清除本地修改,输入T继续、Q退出：[T/Q]")
        if ensureAgain.upper() == 'T':
            os.system('git reset --hard && git clean -df')
        elif ensureAgain.upper() == 'Q':
            exit()
        else:
            exit("输入不合法，请重新运行main.py重新开始")

        if branch_name_local not in temp_branch_list:
            # 同步远端最新的分支，更新本地远端的分支显示数据，拉取分支到本地
            os.system('git fetch origin && git remote update origin --prune')
            os.system('git checkout -b ' + branch_name_local + ' ' +
                      branch_name_origin)
        else:
            os.system('git checkout ' + branch_name_local + ' && git config pull.rebase false && git pull')

        # 在拉取代码耗时过程中不会执行下面的代码，代码拉取成功之后才会向下继续执行，保存最近三次提交的commit记录
        temp_path_file = self.temp_git_commit_path + '/nearly_git_commit.txt'
        os.system(
            "git log -3 --graph --pretty=format:'%s' --abbrev-commit --date=relative >"
            + temp_path_file)
        with open(temp_path_file) as file_obj:
            content = file_obj.read()
        return content

    def __get_branchedits(self):
        try:
            # 转到工程路径下
            os.chdir(self.project_path)
        except Exception as e:
            print("工程路径出错：%s" % e)
            exit()
        branches_str = subprocess.check_output(["git", "branch",
                                                "-r"]).decode()
        # 终端运行“git branch”命令，并且将终端的输出str转存到branches_str里
        branches = branches_str.split('\n')
        # 使用str的split方法将其按照'\n'分割
        branch_dict = {}
        step = 0
        for branch in branches[0:-1]:
            branch_dict[str(step)] = branch.lstrip('* ')
            step += 1
            # 使用str的lstrip方法将字符串的前的空格和当前branch前的“*”标记去除
        return branch_dict

    def __get_branchelists(self):
        try:
            # 转到工程路径下
            os.chdir(self.project_path)
        except Exception as e:
            print("工程路径出错：%s" % e)
            exit()
        branches_str = subprocess.check_output(["git", "branch",
                                                "-l"]).decode()
        # 终端运行“git branch”命令，并且将终端的输出str转存到branches_str里
        branches = branches_str.split('\n')
        # 使用str的split方法将其按照'\n'分割
        branch_local_list = []
        for branch in branches[0:-1]:
            branch_local_list.append(branch.lstrip('* '))
            # 使用str的lstrip方法将字符串的前的空格和当前branch前的“*”标记去除
        return branch_local_list
