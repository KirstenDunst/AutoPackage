

import os
import subprocess
import sys

# 只取工作区和暂存区有改动的文件（不包含 untracked）
def get_uncommitted_files():
    result = subprocess.run(
        ['git', 'diff','--cached', '--name-only'],
        stdout=subprocess.PIPE, text=True
    )
    files = result.stdout.strip().split('\n') if result.stdout.strip() else []
    return files

# 只取工作区和暂存区有改动的文件（不包含 untracked）
def get_uncommitted_files1():
    result = subprocess.run(
        ['git', 'diff', '--name-only'],
        stdout=subprocess.PIPE, text=True
    )
    files = result.stdout.strip().split('\n') if result.stdout.strip() else []
    return files

# # 获取未 commit 文件列表
# def get_uncommitted_files1():
#     result = subprocess.run(
#         ['git', 'status', '--porcelain'],
#         stdout=subprocess.PIPE,
#         text=True
#     )
#     lines = result.stdout.strip().split('\n') if result.stdout.strip() else []
#     files = [line[3:] for line in lines if line]  # 跳过前缀状态码，只取文件名
#     return files

if __name__ == "__main__":
    project_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    files = get_uncommitted_files()
    format_arr = []
    for f in files:
        file_path = os.path.join(project_path, f)
        if (file_path.endswith('.dart')):
            format_arr.append(f)
            subprocess.run(f'dart format {file_path}', shell=True)
    
    all_files = get_uncommitted_files1()
    for f1 in all_files:
        # 检测到已经commit的文件有变更
        if (f1 in format_arr):
            sys.exit(1)  # 1 表示失败，0 表示成功
    

