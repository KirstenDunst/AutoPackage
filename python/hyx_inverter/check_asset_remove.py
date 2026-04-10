# 移除flutter项目无用文件，方法，国际化，重复国际化的操作
import json
import os
import subprocess
import locales_delete
import re
from collections import defaultdict

from pathlib import Path
from common_tool import CommonTool


# 校验国际化，无用资源移除
def check_locales_unused():
    print(">>>check_locales_unused")
    root_path = os.path.abspath(os.path.dirname(__file__) + os.path.sep + "..")
    file_path = root_path + "/assets/locales/zh_CN.json"
    with open(file_path, "r") as f:
        content = f.read()
    # 文件中的json
    json_content = json.loads(content)
    json_content = CommonTool.tranformDict(json_content)

    un_used_key = ""
    for key in json_content.keys():
        parts = key.split(".")
        if parts[0] in ["near", "countryName"]:
            continue
        if len(parts) == 1:
            part = parts[0]
            transformed_parts = str(part[0]).lower() + part[1 : len(part)]
        else:
            # 保持第一个部分不变，其余部分首字母大写
            transformed_parts = [parts[0]] + [
                str(part[0]).upper() + part[1 : len(part)] for part in parts[1:]
            ]
        lowercase_key = "".join(transformed_parts).strip()

        try:
            result = subprocess.run(
                [
                    "rg",
                    lowercase_key,
                    root_path + "/lib/",
                    "-g",
                    "!*.json",
                    "-g",
                    "!*.g.dart",
                ],
                capture_output=True,
                text=True,
            )
            # rg 返回码：0 = 有匹配, 1 = 没匹配, 其他 = 错误
            if result.returncode == 1:
                print(lowercase_key)  # 没命中
                add = key if len(un_used_key) == 0 else ("," + key)
                un_used_key = un_used_key + add
        except FileNotFoundError:
            print("请先安装 rg (ripgrep)")
    print(un_used_key)
    locales_delete.locales_delete(un_used_key)


# 校验国际化，重复的翻译（以中文判断，是否删除需用户自己决定）
def check_locales_repet():
    print(">>>check_locales_repet")
    root_path = os.path.abspath(os.path.dirname(__file__) + os.path.sep + "..")
    file_path = root_path + "/assets/locales/zh_CN.json"
    with open(file_path, "r") as f:
        content = f.read()
    # 文件中的json
    json_content = json.loads(content)
    json_content = CommonTool.tranformDict(json_content)
    same_chinese = []
    repetition_arr = []
    for key in json_content.keys():
        parts = key.split(".")
        if parts[0] in ["near", "countryName"]:
            continue
        value = json_content[key]
        if value in same_chinese:
            repetition_arr.append(value)
        else:
            same_chinese.append(value)

    print(repetition_arr)


# 校验无用的图片资源（指定文件夹扫描项目）
def check_asset_unused():
    print(">>>check_asset_unused")
    # 代码拼接的无法判断


# 校验无用的文件
def check_unused_file():
    print(">>>check_unused_file")
    root_path = os.path.abspath(os.path.dirname(__file__) + os.path.sep + "..")
    root_dir = root_path + "/lib/"
    has_unused_file = False
    for root, dirs, files in os.walk(root_dir, topdown=False):
        # 如果当前目录没有文件且没有子目录 → 删除
        if not dirs and not files:
            os.rmdir(root)

        for f in files:
            file_path = os.path.join(root, f)
            filename = os.path.basename(file_path)
            if filename.startswith("."):
                continue
            result = subprocess.run(
                ["rg", filename, root_path + "/lib/"],
                capture_output=True,
                text=True,
            )
            if result.returncode == 1:
                has_unused_file = True
                # 没命中
                print(f"File: {file_path}:0:0")
                # 移除文件
                Path(file_path).unlink()
    if has_unused_file:
        # 有未使用的文件移除之后，可能里面拖着其他的未使用的文件，所以需要递归一直检测
        check_unused_file()


# 校验无用的方法(针对无继承的类扫描)

# 方法白名单
WHITELIST = {
    "initState",
    "dispose",
    "build",
    "toString",
}


# 提取方法
def extract_methods(content):
    # 简单匹配 class 内方法
    pattern = re.compile(r"class\s+\w+\s*{([\s\S]*?)}", re.MULTILINE)
    method_pattern = re.compile(
        r"(?:void|int|String|bool|double|Future<.*?>)\s+(\w+)\s*\("
    )
    methods = []
    for class_body in pattern.findall(content):
        for match in method_pattern.findall(class_body):
            if match not in WHITELIST:
                methods.append(match)
    return methods


# 主逻辑
def find_unused_methods():
    root_path = os.path.abspath(os.path.dirname(__file__) + os.path.sep + "..")
    root_dir = root_path + "/lib/"
    dart_files = []
    for root_dir, _, files in os.walk(root_dir):
        for f in files:
            if f.endswith(".dart"):
                dart_files.append(os.path.join(root_dir, f))

    file_contents = {}
    all_text = ""

    # 读取所有文件
    for f in dart_files:
        with open(f, "r", encoding="utf-8") as fp:
            content = fp.read()
            file_contents[f] = content
            all_text += content + "\n"
    method_usage = defaultdict(int)

    # 统计方法出现次数
    for f, content in file_contents.items():
        methods = extract_methods(content)
        for m in methods:
            count = len(re.findall(r"\b{}\b".format(m), all_text))
            method_usage[(f, m)] = count

    # 找未使用
    unused = []
    for (f, m), count in method_usage.items():
        if count <= 1:
            unused.append((f, m))
    return unused


def check_unused_func():
    print(">>>check_unused_func")
    unused_methods = find_unused_methods()
    print("未使用的方法：\n")
    for f, m in unused_methods:
        print(f"{m}  ->  {f}")


if __name__ == "__main__":
    # check_unused_file()
    # check_unused_func()
    # check_locales_unused()
    check_locales_repet()
