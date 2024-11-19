import json

from common_tool import CommonTool

if __name__ == "__main__":
    chinese_locale_file = input("筛查value重复的json文件地址:")
    chinese_locale_file = chinese_locale_file.removeprefix("'")
    chinese_locale_file = chinese_locale_file.removesuffix("'")

    # 读取中文国际化json
    with open(chinese_locale_file, "r") as f:
        content = f.read()
    # 文件中的json
    json_content: dict = json.loads(content)
    direct_chinese_dict = CommonTool.tranformDict(json_content, "")

    duplicates = set()

    for k, v in direct_chinese_dict.items():
        if v in duplicates:
            print(f"Duplicate value fount:{v}")
        duplicates.add(v)
