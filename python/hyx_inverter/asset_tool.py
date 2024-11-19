"""
Author: Cao Shixin
Date: 2023-02-02 14:53:48
LastEditors: Cao Shixin
LastEditTime: 2023-02-06 14:41:24
Description: 
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
    def transform_ic_front_name(ic_front_name):
        words = ic_front_name.split("_")
        transformed_words = [words[0]] + [word.capitalize() for word in words[1:]]
        transformed_string = "".join(transformed_words)
        return transformed_string

    @staticmethod
    def file_copy(source_file_path, target_file_path, isForce):
        if os.path.exists(target_file_path):
            if force_save:
                os.remove(target_file_path)
            else:
                exit(
                    "文件已经存在，中断拷贝操作，请手动移除项目资源中的文件："
                    + target_file_path
                )
        shutil.copy(source_file_path, target_file_path)


if __name__ == "__main__":
    source_asset_dir = input("拖入项目中打算加入项目的1倍png文件或者svg文件地址:")
    replace_name = input("放入项目之后的名称:")
    save_type = input("放入哪个项目 A(所有),O(oem),H(主项目):")
    is_force_save = input(
        "是否强制存储在资源目录Y(强制),N(不强制,检测目标文件夹下有同名称则中断):"
    )
    force_save = False
    if is_force_save.upper() == "Y":
        force_save = True
    elif is_force_save.upper() == "N":
        force_save = False
    else:
        exit("输入不合法,请重新执行命令")

    save_oem = False
    save_hyx = False
    save_unsync = False
    if save_type.upper() == "A":
        save_oem = True
        save_hyx = True
        save_unsync = True
    elif save_type.upper() == "O":
        save_oem = True
    elif save_type.upper() == "H":
        save_hyx = True
    else:
        exit("输入不合法,请重新执行命令")

    source_asset_dir = source_asset_dir.removeprefix("'")
    source_asset_dir = source_asset_dir.removesuffix("'")
    source_asset_dir = source_asset_dir.replace("\\", "")
    source_asset_dir = source_asset_dir.strip()

    root_path = os.path.abspath(os.path.dirname(__file__) + os.path.sep + "..")
    project_asset_h_dir = root_path + "/assets_hyx/images"
    project_asset_o_dir = root_path + "/assets_oem/images"
    project_asset_unsync_dir = root_path + "/assets/unsynxed"

    parent_dir = os.path.dirname(source_asset_dir)
    asset_name_type = source_asset_dir.replace(parent_dir + "/", "")
    asset_name_type = asset_name_type.strip()
    asset_temp_arr = asset_name_type.split(".")
    asset_type: str = asset_temp_arr[-1]
    asset_name = asset_temp_arr[0]
    if not ["png", "svg"].__contains__(asset_type.lower()):
        exit("Invalid asset type:" + asset_type)

    if asset_type.lower() == "svg":
        class_name = "InverterSvg"
        dir_name = "svg"
        source_file_path = source_asset_dir
        project_svg_h_dir = root_path + "/assets_hyx/svg"
        project_svg_o_dir = root_path + "/assets_oem/svg"
        if save_hyx:
            target_file_path = project_svg_h_dir + "/" + replace_name + ".svg"
            FileFolderOperate.file_copy(source_file_path, target_file_path, force_save)

        if save_oem:
            target_file_path = project_svg_o_dir + "/" + replace_name + ".svg"
            FileFolderOperate.file_copy(source_file_path, target_file_path, force_save)
    else:
        class_name = "InverterImages"
        dir_name = "images"
        file_names = os.listdir(parent_dir)
        for filename in file_names:
            splits = filename.split(".")
            if splits[-1] == "DS_Store":
                continue
            if len(splits) > 2:
                last = splits.pop()
                first = "".join(splits)
                splits = [first, last]
            name = splits[0]
            type = splits[-1]

            real_names = name.split("@")
            if real_names[0] != asset_name or type != asset_type:
                continue
            source_file_path = parent_dir + "/" + filename
            if save_hyx:
                target_file_path = project_asset_h_dir + "/" + replace_name + "." + type
                if name.__contains__("2x"):
                    target_file_path = (
                        project_asset_h_dir + "/2.0x/" + replace_name + "." + type
                    )
                elif name.__contains__("3x"):
                    target_file_path = (
                        project_asset_h_dir + "/3.0x/" + replace_name + "." + type
                    )
                else:
                    target_file_path = (
                        project_asset_h_dir + "/" + replace_name + "." + type
                    )

                FileFolderOperate.file_copy(
                    source_file_path, target_file_path, force_save
                )

            if save_oem:
                target_file_path = project_asset_o_dir + "/" + replace_name + "." + type
                if name.__contains__("2x"):
                    target_file_path = (
                        project_asset_o_dir + "/2.0x/" + replace_name + "." + type
                    )
                elif name.__contains__("3x"):
                    target_file_path = (
                        project_asset_o_dir + "/3.0x/" + replace_name + "." + type
                    )
                else:
                    target_file_path = (
                        project_asset_o_dir + "/" + replace_name + "." + type
                    )

                FileFolderOperate.file_copy(
                    source_file_path, target_file_path, force_save
                )

    unsync_file_path = (
        project_asset_unsync_dir + "/" + replace_name + "." + asset_type.lower()
    )
    if save_unsync:
        if not os.path.exists(project_asset_unsync_dir):
            os.makedirs(project_asset_unsync_dir, exist_ok=True)
        FileFolderOperate.file_copy(
            parent_dir + "/" + asset_name_type, unsync_file_path, force_save
        )
    elif save_type.upper() == "O":
        # 单独为oem添加，校验差异化文件存在的话删除（目前以主项目为准，默认按照oem都是后出的资源）
        if os.path.exists(unsync_file_path):
            os.remove(unsync_file_path)

    if save_type.upper() == "A":
        origin_text = (
            "class "
            + class_name
            + " {\n  static final String _assets = '${F.assets}/';\n  static String prefix = '${_assets}"
            + dir_name
            + "/';"
        )
        add_text = (
            "\n  static String "
            + FileFolderOperate.transform_ic_front_name(replace_name)
            + " = '${prefix}"
            + replace_name
            + "."
            + asset_type.lower()
            + "';"
        )
        FileFolderOperate.replace_text(
            root_path + "/lib/constant/assets.dart",
            origin_str=origin_text,
            replace_str=origin_text + add_text,
        )
