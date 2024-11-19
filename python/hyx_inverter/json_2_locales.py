# 适用于发布前将线上平台运维国际化覆盖本地国际化文件

import json
import os

from locales_tool import trans_to_const


def recursive_replace(flat_key: str, value, nested_obj: dict):
    """递归将 flat_json 的值替换到 nested_json 的对应位置"""
    if flat_key in nested_obj:
        nested_obj[flat_key] = value
    else:
        key_arr = flat_key.split(".")
        first_key = key_arr[0]
        if first_key in nested_obj and str(
            nested_obj[first_key].__class__
        ).__contains__("dict"):
            recursive_replace(
                flat_key.replace(first_key + ".", "", 1),
                value,
                nested_obj[first_key],
            )


if __name__ == "__main__":
    root_path = os.path.abspath(os.path.dirname(__file__) + os.path.sep + "..")
    locales_dir = root_path + "/assets/locales/"
    remote_json_path = input("输入云端下载将要覆盖项目国际化文件地址:")
    remote_json_path = remote_json_path.removeprefix("'")
    remote_json_path = remote_json_path.removesuffix("'")

    # 中转map
    languageTransMap = {
        "de": "de_DE",
        "en": "en_US",
        "es": "es_ES",
        "fr": "fr_FR",
        "it": "it_IT",
        "ja": "ja_JP",
        "nl": "nl_NL",
        "pl": "pl_PL",
        "pt": "pt_PT",
        "ro": "ro_RO",
        "zh": "zh_CN",
    }

    with open(remote_json_path, "r") as f:
        remote_json_content = f.read()
    remote_json: dict = json.loads(remote_json_content)
    f.close()

    language_locales = {}
    file_list = os.listdir(locales_dir)
    for file_name in file_list:
        if file_name.endswith(".json"):
            if file_name.__contains__("_"):
                file_path = os.path.join(locales_dir, file_name)
                with open(file_path, "r") as f:
                    content = f.read()
                # 文件中的json
                json_content = json.loads(content)
                f.close()

                language_locales[file_name.split("_")[0]] = json_content
            else:
                continue
        else:
            continue

    for k, v in remote_json.items():
        local_map:dict = v['local']
        for lk, lv in language_locales.items():
            if lk in local_map:
                recursive_replace(k,local_map[lk],lv)
    
    for ek,ev in language_locales.items():
        local_file_name = languageTransMap[ek]
        file_path = os.path.join(locales_dir, local_file_name + ".json")
        with open(file_path, "w") as f2:
            f2.write(json.dumps(ev, ensure_ascii=False, indent=2))
        f2.close()

    trans_to_const()
