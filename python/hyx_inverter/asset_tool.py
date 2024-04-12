'''
Author: Cao Shixin
Date: 2023-02-02 14:53:48
LastEditors: Cao Shixin
LastEditTime: 2023-02-06 14:41:24
Description: 
'''
import os
import shutil

if __name__ == '__main__':
    source_asset_dir = input('拖入项目中打算加入项目的1倍png文件地址:')
    replace_name = input('放入项目之后的名称:')
    source_asset_dir = source_asset_dir.removeprefix("'")
    source_asset_dir = source_asset_dir.removesuffix("'")

    root_path = os.path.abspath(os.path.dirname(__file__)+os.path.sep+"..")
    project_asset_dir = root_path + '/assets/images'

    parent_dir = os.path.dirname(source_asset_dir)
    asset_name_type = source_asset_dir.replace(parent_dir+'/', '')
    asset_temp_arr = asset_name_type.split('.')
    asset_type: str = asset_temp_arr[-1]
    asset_name = asset_temp_arr[0]
    if asset_type.lower() != 'png':
        exit('Invalid asset type:'+asset_type)

    file_names = os.listdir(parent_dir)
    for filename in file_names:
        splits = filename.split('.')
        if splits[-1] == 'DS_Store':
            continue
        if len(splits) > 2:
            last = splits.pop()
            first = ''.join(splits)
            splits = [first, last]
        name = splits[0]
        type = splits[-1]

        real_names = name.split('@')
        if real_names[0] != asset_name or type != asset_type:
            continue

        target_file_path = project_asset_dir+'/'+replace_name+'.'+type
        if name.__contains__('2x'):
            target_file_path = project_asset_dir+'/2.0x/'+replace_name+'.'+type
        elif name.__contains__('3x'):
            target_file_path = project_asset_dir+'/3.0x/'+replace_name+'.'+type
        else:
            target_file_path = project_asset_dir+'/'+replace_name+'.'+type

        if os.path.exists(target_file_path):
            print('文件已经存在，中断拷贝操作，请手动移除项目资源中的文件：'+target_file_path)
        else:
            shutil.copy(parent_dir+'/'+filename,
                        target_file_path)
