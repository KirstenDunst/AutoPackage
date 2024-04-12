import os
import re


def process_regex(pattern, folder_path:str):
    # 在这里，您可以执行与正则表达式相关的操作
    compiled_pattern = re.compile(pattern)
    match_file_list = []
    
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file == '.DS_Store':
                continue
            full_file_path = os.path.join(root, file)
            with open(full_file_path, 'r') as f:
                content = f.read()
                matches = compiled_pattern.findall(content)
                if len(matches) > 0:
                    match_file_list.append(full_file_path)
        for dir in dirs:
            tempArr = process_regex(pattern,os.path.join(root, dir))
            match_file_list += tempArr
    return match_file_list

def assets_paths(folder_path:str):
    file_paths:list[list[str]] = []
    #深入遍历，会一层一层遍历完
    for root, dirs, files in os.walk(folder_path):
        if root.__contains__('2.0x')|root.__contains__('3.0x') | root.__contains__('locales'):
            print('过滤掉不用计算')
        else:
            for file in files:
                name = file.split('.')[0]
                names = name.split('_')
                relative_path = root.replace(folder_path,'')
                arr = relative_path.split('/')
                arr.remove('')
                if len(arr)>0:
                    # 根据项目来，本项目assets的文件没有一级文件，都是在二级文件夹中存放，且项目常量也是二级文件夹的命名，所以过滤掉以及文件夹用于文件常量的查找
                    if ['svg','json','images','gif'].__contains__(arr[0]):
                        arr.pop(0)
                    for item in names:
                        arr += item.split('-')
                    file_paths.append(arr)
    return file_paths


if __name__ == '__main__':
    project_path = input('请输入项目根目录:')
    project_path = project_path.removeprefix("'")
    project_path = project_path.removesuffix("'")
    assets_path = input('请输入项目资源根目录eg[assets的路径]:')
    assets_path = assets_path.removeprefix("'")
    assets_path = assets_path.removesuffix("'")
    
    file_paths:list[list[str]] = assets_paths(assets_path)
    check_dic = {}
    for arr in file_paths:
        if len(arr) == 0:
            continue
        name = arr[0]
        for step in arr[1:]:
            name += step.title()
        if len(name) > 0 and  not check_dic.__contains__(name):
            check_dic[name] = 1
            result = process_regex('\.'+name,project_path)
            check_dic[name] = result
            if len(result) == 0:
                print(name)