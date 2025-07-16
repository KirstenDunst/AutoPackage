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
    def branch_change(self, branch_name=''):
        """执行分支切换"""
        temp_branch_dict = self.__get_branchedits()
        temp_branch_list = self.__get_branchelists()

        if not branch_name == '':
            branch_name_origin = branch_name
        else:
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
        if branch_name == '':
            ensureAgain = input("请再次确认当前分支是否有没有提交的修改，选择分支将会清除本地修改,输入T继续、Q退出：[T/Q]")
        else:
            ensureAgain = 'T'
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
            os.system('git checkout ' + branch_name_local +
                      ' && git config pull.rebase false && git pull')

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
    
    # 获取当前分支名称
    def get_current_branch():
        result = subprocess.run(['git', 'rev-parse', '--abbrev-ref', 'HEAD'],
                                stdout=subprocess.PIPE, text=True)
        return result.stdout.strip()

    # 核对分支是否在远端存在
    def check_remote_branch_exists(branch):
        result = subprocess.run(['git', 'ls-remote', '--heads', 'origin', branch],
                                stdout=subprocess.PIPE, text=True)
        return bool(result.stdout.strip())

    # 获取分支未提交的commit hash数组
    def get_unpushed_commits(branch):
        result = subprocess.run(['git', 'log', f'origin/{branch}..{branch}', '--pretty=format:%H'],
                                stdout=subprocess.PIPE, text=True)
        commits = result.stdout.strip().split('\n') if result.stdout.strip() else []
        return commits

    # 获取分支最近几次的commit hash数组
    def get_recent_commits(n):
        result = subprocess.run(['git', 'log', f'-n {n}', '--pretty=format:%H'],
                                stdout=subprocess.PIPE, text=True)
        commits = result.stdout.strip().split('\n') if result.stdout.strip() else []
        return commits

    # 获取commit中改动的文件名称数组
    def get_files_in_commit(commit_hash):
        result = subprocess.run(['git', 'diff-tree', '--no-commit-id', '--name-only', '-r', commit_hash],
                                stdout=subprocess.PIPE, text=True)
        files = result.stdout.strip().split('\n') if result.stdout.strip() else []
        return files
