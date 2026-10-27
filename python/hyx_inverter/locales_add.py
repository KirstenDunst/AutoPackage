import os
import json
import httpx
from locales_tool import trans_to_const
from common_tool import CommonTool


def get_version_from_file():
    root_path = os.path.abspath(os.path.dirname(__file__) + os.path.sep + "..")
    with open(root_path + "/pubspec.yaml", "r") as file:
        for line in file:
            if "version:" in line:
                version = line.split("version:")[1].strip()
                if version.__contains__("+"):
                    version = version.split("+")[0]
                return version
    return None

# 去除key中的首尾空格
def remove_dict_key_empty(map: dict) -> dict:
    new_dict = {}
    for k, v in map.items():
        check_key = k.strip()
        if isinstance(v, dict):
            new_dict[check_key] = remove_dict_key_empty(v)
        elif isinstance(v, list):
            new_dict[check_key] = [remove_dict_key_empty(item) if isinstance(item, dict) else item for item in v]
        else:
            new_dict[check_key] = v
    return new_dict

def cloud_trans_dict(add_dict: dict, cloud_key_arr: list) -> dict:
    new_dict = {}
    for ak, av in add_dict.items():
        if len(av) == 2 and av["zh"] != None and av["en"] != None:
            cloud_key = ""
            if len(cloud_key_arr) == 0:
                cloud_key = ak
            else:
                cloud_key = ".".join(cloud_key_arr)
                cloud_key += "." + ak
            result = create_plantform_trans(av["zh"], av["en"], cloud_key)
            new_dict[ak] = result
        else:
            cloud_key_arr.append(ak)
            result = cloud_trans_dict(av, cloud_key_arr)
            new_dict[ak] = result
    return new_dict


def cloud_trans_dict_cn(add_dict: dict, cloud_key_arr: list) -> dict:
    new_dict = {}
    for ak, av in add_dict.items():
        if isinstance(av, str):
            cloud_key = ""
            if len(cloud_key_arr) == 0:
                cloud_key = ak
            else:
                cloud_key = ".".join(cloud_key_arr)
                cloud_key += "." + ak
            result = create_plantform_trans(av, "", cloud_key)
            new_dict[ak] = result
        else:
            cloud_key_arr.append(ak)
            result = cloud_trans_dict_cn(av, cloud_key_arr)
            new_dict[ak] = result
    return new_dict


def key_local_2_add_json(key_local_dict: dict, language_dict: dict) -> dict:
    result = {}

    # 把最里面一层的多语言国际化的key翻出来排在最外层
    def recurse(inner_dict, path):
        for key, value in inner_dict.items():
            if isinstance(value, dict):
                recurse(value, path + [key])
            else:
                # 创建新的最外层key，如果不存在就初始化为一个空字典
                if key not in result:
                    result[key] = {}
                # 根据路径构造嵌套字典
                current = result[key]
                for p in path[:-1]:
                    if p not in current:
                        current[p] = {}
                    current = current[p]
                current[path[-1]] = value

    # 从根节点递归展开
    recurse(key_local_dict, [])

    back = {}
    for k, v in result.items():
        if k in language_dict:
            back[language_dict[k]] = v
    return back


def create_plantform_trans(
    zh_translate: str, en_translate: str, local_key: str
) -> dict:
    version = get_version_from_file()
    ask_json = {
        "nameKey": local_key,
        "nameZh": zh_translate,
        # 用英文翻译小语种，en：使用英文翻译，zh：使用中文翻译
        "sourceLanguage": "zh",
        "remark": version,
        "clientType": 1,
    }
    if len(en_translate) > 0:
        ask_json["nameEn"] = en_translate
        ask_json["sourceLanguage"] = "en"
    r = httpx.post(
        url="https://ops-system-dev.hyxicloud.com/ops-platform/langNameClient/test/devLangNameAdd",
        json=ask_json,
        timeout=httpx.Timeout(timeout=20.0),
    ).text
    print(r)

    result_json = json.loads(r)
    if result_json["success"] == True:
        data: dict = result_json["data"]
        return data
    else:
        print("Error:" + zh_translate + ":翻译时候出错!")
        return {}


def json_add(old_dict: dict, add_dict: dict):
    newDict = {}
    newDict.update(old_dict)
    for k, v in add_dict.items():
        if old_dict.__contains__(k):
            if str(v.__class__).__contains__("dict") and str(
                old_dict[k].__class__
            ).__contains__("dict"):
                result_dict = json_add(old_dict[k], v)
                newDict[k] = result_dict
        else:
            newDict[k] = v
    return newDict


def use_cloud_to_trans(chinese_json_add: dict, source_dir: str, is_cn_trans: bool):
    trans_key_local = (
        cloud_trans_dict(chinese_json_add, [])
        if not is_cn_trans
        else cloud_trans_dict_cn(chinese_json_add, [])
    )
    trans_dict = key_local_2_add_json(trans_key_local, CommonTool.getLocalDict())
    add_trans_locale(trans_dict, source_dir)


def add_trans_locale(trans_dict: dict, source_dir: str):
    for k, v in trans_dict.items():
        # 读取原数据，合并json
        file_path = source_dir + k + ".json"
        if not os.path.exists(file_path):
            file = open(file_path, "w")
            file.close()

        with open(file_path, "r") as f0:
            json_content = f0.read()
        temp_json_content: dict = (
            {} if len(json_content) == 0 else json.loads(json_content)
        )
        f0.close()
        temp_json_content = json_add(temp_json_content, v)

        # 写入文件
        merge_json_data = json.dumps(temp_json_content, ensure_ascii=False, indent=2)
        with open(file_path, "w") as f1:
            f1.write(merge_json_data)
        f1.close()


# 网易有道智云翻译服务api调用demo
# api接口: https://openapi.youdao.com/api
if __name__ == "__main__":
    root_path = os.path.abspath(os.path.dirname(__file__) + os.path.sep + "..")
    source_dir = root_path + "/assets/locales/"
    todo_json_file = source_dir + "todo.json"

    if os.path.exists(todo_json_file):
        os.remove(todo_json_file)
    file = open(todo_json_file, "w")

    file.write(json.dumps({"": {"zh": "", "en": ""}}, ensure_ascii=False, indent=2))
    file.close()

    is_continue = input(
        "已创建待添加中文国际化json,路径assets/locales/todo.json,填写完成后输入C以继续:"
    )
    if not is_continue.upper() == "C":
        os.remove(todo_json_file)
        exit("您已中断执行")
    with open(todo_json_file, "r") as f:
        json_content_todo = f.read()
    chinese_json_add = json.loads(json_content_todo)
    
    # 去除key中的空格
    chinese_json_add = remove_dict_key_empty(chinese_json_add)

    use_cloud_to_trans(chinese_json_add, source_dir, False)

    trans_to_const()
    os.remove(todo_json_file)
