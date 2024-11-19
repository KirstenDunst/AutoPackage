# 用于批量删除所有国际化中的指定字段

import json
import os


def check_remove_key(json_content: dict, remove_key: str) -> dict:
    newDict = {}
    new_remove_key = remove_key.lower()
    for k, v in json_content.items():
        k_lower = k.lower()
        if str(v.__class__).__contains__("dict"):
            if new_remove_key.startswith(k_lower):
                dealDict = check_remove_key(v, new_remove_key.removeprefix(k_lower))
                newDict.update({k: dealDict})
            else:
                newDict.update({k: v})
        else:
            if k_lower != new_remove_key:
                newDict[k] = v
    return newDict


if __name__ == "__main__":
    keys = input("输入需要删除的国际化key,多个之间用英文逗号隔开:")
    locale_keys = keys.split(",")

    if len(locale_keys) == 0:
        exit("请按照规则输入国际化key内容")

    root_path = os.path.abspath(os.path.dirname(__file__) + os.path.sep + "..")
    source_dir = root_path + "/assets/locales/"

    file_list = os.listdir(source_dir)
    for file_name in file_list:
        if file_name.endswith(".json"):
            if file_name.__contains__("_"):
                file_path = os.path.join(source_dir, file_name)
                with open(file_path, "r") as f:
                    content = f.read()
                # 文件中的json
                json_content = json.loads(content)
                f.close()

                for item in locale_keys:
                    json_content = check_remove_key(json_content, item)

                with open(file_path, "w") as f1:
                    f1.write(json.dumps(json_content, ensure_ascii=False, indent=2))
                f1.close()
            else:
                continue
        else:
            continue
