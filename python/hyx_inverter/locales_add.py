import requests
import hashlib
import time
import uuid
import os
import json
import httpx
from locales_tool import trans_to_const


class Authentication:
    '''
    添加鉴权相关参数 -
        appKey : 应用ID
        salt : 随机值
        curtime : 当前时间戳(秒)
        signType : 签名版本
        sign : 请求签名
        @param appKey    您的应用ID
        @param appSecret 您的应用密钥
        @param paramsMap 请求参数表
    '''   
    @staticmethod
    def addAuthParams(appKey, appSecret, params):
        q = params.get('q')
        if q is None:
            q = params.get('img')
        salt = str(uuid.uuid1())
        curtime = str(int(time.time()))
        sign = Authentication.calculateSign(appKey, appSecret, q, salt, curtime)
        params['appKey'] = appKey
        params['salt'] = salt
        params['curtime'] = curtime
        params['signType'] = 'v3'
        params['sign'] = sign

    '''
        计算鉴权签名 -
        计算方式 : sign = sha256(appKey + input(q) + salt + curtime + appSecret)
        @param appKey    您的应用ID
        @param appSecret 您的应用密钥
        @param q         请求内容
        @param salt      随机值
        @param curtime   当前时间戳(秒)
        @return 鉴权签名sign
    '''
    @staticmethod
    def calculateSign(appKey, appSecret, q, salt, curtime):
        strSrc = appKey + Authentication.getInput(q) + salt + curtime + appSecret
        return Authentication.encrypt(strSrc)

    @staticmethod
    def encrypt(strSrc):
        hash_algorithm = hashlib.sha256()
        hash_algorithm.update(strSrc.encode('utf-8'))
        return hash_algorithm.hexdigest()

    @staticmethod 
    def getInput(input):
        if input is None:
            return input
        inputLen = len(input)
        return input if inputLen <= 20 else input[0:10] + str(inputLen) + input[inputLen - 10:inputLen]


def createRequest(to_translate:str, language_to:str) -> str:
    if language_to == 'ZH':
        return to_translate

    r = httpx.post(url = "http://127.0.0.1:1188/translate", data = json.dumps({
        "text": to_translate,
        "source_lang": "ZH",
        "target_lang": language_to
    })).text
    result_json = json.loads(r)
    if result_json['code'] == 200:
        # 应对突然出现的特殊字符
        result_str:str = result_json['data']
        # title()每个单词的首字母大写，非字母后的第一个字母将转换为大写字母
        result_str = result_str.title()
        print('Result:'+to_translate +'-->'+language_to + ':'+result_str) # The output text
        return result_str
    else:
        print('Error:' + to_translate+':翻译为语言'+language_to+'的时候出错!')
        print('需要手动翻译拷贝替换对应语言的json空字符串,然后再手动执行locales_tool.py脚本生成字符常量')
        return ''        


def doCall(url, header, params, method):
    if 'get' == method:
        return requests.get(url, params)
    elif 'post' == method:
        return requests.post(url, params, header)

def trans_to_new_dict(old_dict:dict, language_to:str) -> dict:
    newDict = {}
    for k, v in old_dict.items():
        if str(v.__class__).__contains__('dict'):
            result_dict = trans_to_new_dict(v,language_to)
            newDict[k] = result_dict
        else:
            newDict[k] = createRequest(v, language_to) 
    return newDict


def json_add(old_dict:dict, add_dict:dict):
    newDict = {}
    newDict.update(old_dict)
    for k, v in add_dict.items():
        if old_dict.__contains__(k):
            if str(v.__class__).__contains__('dict') and str(old_dict[k].__class__).__contains__('dict'):
              result_dict = json_add(old_dict[k],v)
              newDict[k] = result_dict
        else:
            newDict[k] = v
        
    return newDict

# 网易有道智云翻译服务api调用demo
# api接口: https://openapi.youdao.com/api
if __name__ == '__main__':
    root_path = os.path.abspath(os.path.dirname(__file__)+os.path.sep+"..")
    source_dir = root_path + '/assets/locales/'
    todo_json_file = source_dir + 'todo.json'
    if os.path.exists(todo_json_file):
        os.remove(todo_json_file)
    file = open(todo_json_file,'w')
    file.write("{\n}") #写入内容信息
    file.close()
        
    is_continue = input('已创建待添加中文国际化json,路径assets/locales/todo.json,填写完成后输入C以继续:')
    if not is_continue.upper() == 'C':
        os.remove(todo_json_file)
        exit('您已中断执行')
    with open(todo_json_file, 'r') as f:
        json_content_todo = f.read()
    chinese_json_add = json.loads(json_content_todo)
    language_dict = {'DE':'de_DE','EN':'en_US','ES':'es_ES','FR':'fr_FR','IT':'it_IT','PL':'pl_PL','PT':'pt_PT','ZH':'zh_CN'}
    trans_dict:dict = {}
    for k, v in language_dict.items():
        trans_dict[v] = trans_to_new_dict(chinese_json_add, k)
        
    for k, v in trans_dict.items():
        # 读取原数据，合并json
        file_path = source_dir + k + '.json'
        with open(file_path, 'r') as f:
            json_content = f.read()
        temp_json_content:dict = json.loads(json_content)
        temp_json_content = json_add(temp_json_content,v)
        # 写入文件
        merge_json_data = json.dumps(temp_json_content,ensure_ascii=False,indent=2)
        with open(file_path, 'w') as f:
            f.write(merge_json_data)        
    
    trans_to_const()
    os.remove(todo_json_file)  
    
