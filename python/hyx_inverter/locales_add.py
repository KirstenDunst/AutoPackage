from copy import deepcopy
import requests
import hashlib
import time
import uuid
import os
import json
import httpx
import pandas as pd
from io import BytesIO
from locales_tool import trans_to_const
from common_tool import CommonTool


class Authentication:
    """
    添加鉴权相关参数 -
        appKey : 应用ID
        salt : 随机值
        curtime : 当前时间戳(秒)
        signType : 签名版本
        sign : 请求签名
        @param appKey    您的应用ID
        @param appSecret 您的应用密钥
        @param paramsMap 请求参数表
    """

    @staticmethod
    def addAuthParams(appKey, appSecret, params):
        q = params.get("q")
        if q is None:
            q = params.get("img")
        salt = str(uuid.uuid1())
        curtime = str(int(time.time()))
        sign = Authentication.calculateSign(appKey, appSecret, q, salt, curtime)
        params["appKey"] = appKey
        params["salt"] = salt
        params["curtime"] = curtime
        params["signType"] = "v3"
        params["sign"] = sign

    """
        计算鉴权签名 -
        计算方式 : sign = sha256(appKey + input(q) + salt + curtime + appSecret)
        @param appKey    您的应用ID
        @param appSecret 您的应用密钥
        @param q         请求内容
        @param salt      随机值
        @param curtime   当前时间戳(秒)
        @return 鉴权签名sign
    """

    @staticmethod
    def calculateSign(appKey, appSecret, q, salt, curtime):
        strSrc = appKey + Authentication.getInput(q) + salt + curtime + appSecret
        return Authentication.encrypt(strSrc)

    @staticmethod
    def encrypt(strSrc):
        hash_algorithm = hashlib.sha256()
        hash_algorithm.update(strSrc.encode("utf-8"))
        return hash_algorithm.hexdigest()

    @staticmethod
    def getInput(input):
        if input is None:
            return input
        inputLen = len(input)
        return (
            input
            if inputLen <= 20
            else input[0:10] + str(inputLen) + input[inputLen - 10 : inputLen]
        )


def capitalize_first_word(word_str: str):
    words = word_str.split()
    words[0] = words[0].capitalize()
    return " ".join(words)


def trans_world_filter(trans_world: str) -> str:
    # 微逆，逆变器翻译公司定制化(主要针对英文翻译)
    need_trans_dict = {
        "inverse ": "inverter ",
        "inverses ": "inverters ",
        "Inverse ": "Inverter ",
        "Inverses ": "Inverters ",
    }
    result = trans_world
    for k, v in need_trans_dict.items():
        result = result.replace(k, v)
    return result


def fetch_excel_from_url(url):
    """
    从指定的URL获取Excel文件并读取其内容。
    参数: url (str): Excel文件的URL。
    返回值: DataFrame: 包含Excel数据的DataFrame。
    """
    try:
        # 发送GET请求下载Excel文件
        response = requests.get(url)
        response.raise_for_status()  # 如果请求失败则抛出异常
        # 使用BytesIO读取Excel文件内容
        excel_data = BytesIO(response.content)
        # 读取Excel数据到DataFrame
        df = pd.read_excel(excel_data)
        print("总表数据获取完成")
        return df
    except requests.exceptions.RequestException as e:
        print(f"请求失败: {e}")
        return None
    except Exception as e:
        print(f"读取Excel文件失败: {e}")
        return None


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


def cloud_trans_dict(add_dict: dict, cloud_key_arr: list) -> dict:
    new_dict = {}
    for ak, av in add_dict.items():
        if str(av.__class__).__contains__("dict"):
            cloud_key_arr.append(ak)
            result = cloud_trans_dict(av, cloud_key_arr)
            new_dict[ak] = result
        else:
            cloud_key = ""
            if len(cloud_key_arr) == 0:
                cloud_key = ak
            else:
                cloud_key = ".".join(cloud_key_arr)
                cloud_key += "." + ak
            result = create_plantform_trans(av, cloud_key)
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
    for k,v in result.items():
       if k in language_dict:
           back[language_dict[k]] = v 
    return back


def create_plantform_trans(to_translate: str, local_key: str) -> dict:
    version = get_version_from_file()
    r = httpx.post(
        url="https://ops-system-dev.hyxicloud.com/ops-platform/langNameClient/test/devLangNameAdd",
        json={
            "nameKey": local_key,
            "nameZh": to_translate,
            "remark": version,
            "clientType": 1,
        },
        timeout=httpx.Timeout(timeout=20.0),
    ).text
    print(r)

    result_json = json.loads(r)
    if result_json["success"] == True:
        data: dict = result_json["data"]
        return data
    else:
        exit("Error:" + to_translate + ":翻译时候出错!")


def createRequest(to_translate: str, language_to: str) -> str:
    if language_to == "ZH":
        return to_translate

    r = httpx.post(
        url="http://127.0.0.1:1188/translate",
        data=json.dumps(
            {"text": to_translate, "source_lang": "ZH", "target_lang": language_to}
        ),
        timeout=httpx.Timeout(timeout=10.0),
    ).text
    result_json = json.loads(r)
    if result_json["code"] == 200:
        # 应对突然出现的特殊字符
        result_str: str = result_json["data"]
        if len(result_str.split(" ")) > 5:
            # 短句只对首单词首字母大写
            result_str = capitalize_first_word(result_str)
        else:
            # title()每个单词的首字母大写，非字母后的第一个字母将转换为大写字母
            result_str = result_str.title()

        if language_to == "EN":
            result_str = trans_world_filter(result_str)
        print(
            "Result:" + to_translate + "-->" + language_to + ":" + result_str
        )  # The output text
        return result_str
    else:
        print("Error:" + to_translate + ":翻译为语言" + language_to + "的时候出错!")
        print(
            "需要手动翻译拷贝替换对应语言的json空字符串,然后再手动执行locales_tool.py脚本生成字符常量"
        )
        return ""


def doCall(url, header, params, method):
    if "get" == method:
        return requests.get(url, params)
    elif "post" == method:
        return requests.post(url, params, header)


def trans_to_new_dict(
    old_dict: dict[str, str],
    language_to: str,
    dataframe: pd.DataFrame | None,
    excel_index_dict: dict[str, int],
) -> dict:
    newDict = {}
    language_arr = list(excel_index_dict.keys())
    for k, v in old_dict.items():
        if str(v.__class__).__contains__("dict"):
            result_dict = trans_to_new_dict(v, language_to, dataframe, excel_index_dict)
            newDict[k] = result_dict
        else:
            trans_value = ""
            if dataframe is not None:
                position = dataframe[dataframe["中文"] == v].index
                if not position.empty and language_to in language_arr:
                    rowIndex = position[0]
                    columnIndex = excel_index_dict[language_to]
                    try:
                        result = dataframe.iloc[int(rowIndex), int(columnIndex)]
                        if not pd.isna(result):
                            trans_value = result
                            print(
                                f"{v}-->{language_to}:(翻译总表位置:row(excel表里面的真实行数需要自行+2):{rowIndex},column:{columnIndex}):{trans_value}"
                            )
                    except Exception as e:
                        print(f"获取内容过程中出现错误: {e}")

            if trans_value == None or trans_value == "":
                newDict[k] = createRequest(v, language_to)
            else:
                newDict[k] = trans_value

    return newDict


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


# 局限性：只替换value为“”的原数据（用于临时加语言，不够的已经用空字符占位了，然后用机翻补充替换掉）
def json_replace_empty(old_dict: dict, add_dict: dict):
    newDict = {}
    newDict.update(old_dict)
    for k, v in add_dict.items():
        if old_dict.__contains__(k):
            if str(v.__class__).__contains__("dict") and str(
                old_dict[k].__class__
            ).__contains__("dict"):
                result_dict = json_replace_empty(old_dict[k], v)
                newDict[k] = result_dict
            else:
                if old_dict[k] == "":
                    newDict[k] = v
    return newDict


def use_cloud_to_trans(chinese_json_add: dict, source_dir: str):
    language_dict = {
        "de": "de_DE",
        "en": "en_US",
        "es": "es_ES",
        "fr": "fr_FR",
        "it": "it_IT",
        "pl": "pl_PL",
        "pt": "pt_PT",
        "zh": "zh_CN",
        "nl": "nl_NL",
        "ja": "ja_JP",
        "ro": "ro_RO",
    }

    trans_key_local = cloud_trans_dict(chinese_json_add, [])
    trans_dict = key_local_2_add_json(trans_key_local, language_dict)
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
        # 大批缺少内容补充
        # temp_json_content = json_replace_empty(temp_json_content,v)

        # 写入文件
        merge_json_data = json.dumps(temp_json_content, ensure_ascii=False, indent=2)
        with open(file_path, "w") as f1:
            f1.write(merge_json_data)
        f1.close()


def use_deepLX_trans(chinese_json_add: dict, source_dir: str):
    # 获取翻译过的云文件
    dataframe = fetch_excel_from_url(
        "https://hyxipower.oss-cn-hangzhou.aliyuncs.com/locales/locales_trans_all.xlsx"
    )

    language_dict = {
        "DE": "de_DE",
        "EN": "en_US",
        "ES": "es_ES",
        "FR": "fr_FR",
        "IT": "it_IT",
        "PL": "pl_PL",
        "PT": "pt_PT",
        "ZH": "zh_CN",
        "NL": "nl_NL",
        "JA": "ja_JP",
        "RO": "ro_RO",
    }
    # 中文：ZH，英语：EN，德语：DE，西班牙语：ES，法语：FR，葡萄牙语：PT，意大利语：IT，波兰语：PL，日本语：JA，荷兰语：NL，罗马尼亚语：RO
    excel_index_dict = {
        "ZH": 0,
        "EN": 1,
        "DE": 2,
        "ES": 3,
        "FR": 4,
        "PT": 5,
        "IT": 6,
        "PL": 7,
        "JA": 8,
        "NL": 9,
        "RO": 10,
    }
    trans_dict: dict = {}
    deal_dict: dict = {}
    for k, v in language_dict.items():
        trans_map = trans_to_new_dict(chinese_json_add, k, dataframe, excel_index_dict)
        trans_dict[v] = trans_map
        deal_dict[k.lower()] = CommonTool.tranformDict(trans_map)

    add_trans_locale(trans_dict, source_dir)

    upload_json = {}
    version = get_version_from_file()
    for ak, av in deal_dict.items():
        for tk, tv in av.items():
            if tk in upload_json:
                upload_json[tk]["local"].update({ak: tv})
            else:
                upload_json[tk] = {"remark": version, "local": {ak: tv}}
    with open(source_dir + "uploadCloud.json", "w") as fu:
        fu.write(json.dumps(upload_json, ensure_ascii=False, indent=2))
    fu.close()


# 网易有道智云翻译服务api调用demo
# api接口: https://openapi.youdao.com/api
if __name__ == "__main__":
    root_path = os.path.abspath(os.path.dirname(__file__) + os.path.sep + "..")
    source_dir = root_path + "/assets/locales/"
    todo_json_file = source_dir + "todo.json"
    if os.path.exists(todo_json_file):
        os.remove(todo_json_file)
    file = open(todo_json_file, "w")
    file.write("{\n}")  # 写入内容信息
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

    use_cloud_trans = input("是否使用云平台翻译[Y|N]:")
    if use_cloud_trans.upper() == "Y":
        use_cloud_to_trans(chinese_json_add, source_dir)
    elif use_cloud_trans.upper() == "N":
        # 云平台出现问题，使用本地翻译，并暂存批量导入文件存放在uploadCloud.json中
        use_deepLX_trans(chinese_json_add, source_dir)
    else:
        exit("输入不合法，请重新运行此脚本")

    trans_to_const()
    os.remove(todo_json_file)
