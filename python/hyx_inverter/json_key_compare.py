import json

from common_tool import CommonTool

if __name__ == "__main__":
    one_json = input("输入第一个json文件地址:")
    other_json = input("输入第二个json文件地址:")
    one_json_path = one_json.removeprefix("'")
    one_json_path = one_json_path.removesuffix("'")
    other_json_path = other_json.removeprefix("'")
    other_json_path = other_json_path.removesuffix("'")

    with open(one_json_path, "r") as onefile:
        one_json_data = onefile.read()
    with open(other_json_path, "r") as otherfile:
        other_json_data = otherfile.read()

    one_json_content = json.loads(one_json_data)
    one_json_content = CommonTool.tranformDict(one_json_content, "")
    other_json_content = json.loads(other_json_data)
    other_json_content = CommonTool.tranformDict(other_json_content, "")

    one_json_keys = list(one_json_content.keys())
    other_json_keys = list(other_json_content.keys())

    for key in one_json_content:
        if other_json_keys.__contains__(key):
            one_json_keys.remove(key)
            other_json_keys.remove(key)

    print("执行结果(对应第一个json:第二个json两者所特有的key数组):")
    print(str(other_json_keys) + ":" + str(one_json_keys))
