import json
import os
import re


def search_keyword_in_file(file_path:str, keyword:str, near_local_json_path:str):
    """Search for a keyword in a file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                if '.'+keyword+'.tr' in line:
                    return True
                elif 'LocaleKeys.'+keyword in line:
                    return True
        
        # 正则匹配换行的国际化key字段
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        pattern = fr'LocaleKeys\n\s+\.{keyword}'
        if re.search(pattern, content,flags=re.DOTALL):
            return True  
        
        # 检测近端配置文件是否存在
        if keyword.startswith('near'):
            key_clear = keyword.replace('near','')
            key_clear = (str(key_clear[0]).lower() + key_clear[1:len(key_clear)])
            # 过滤掉近端本地debug.json里面的国际化字段
            with open(near_local_json_path, 'r', encoding='utf-8') as file:
                for line in file:
                    if "\""+key_clear+"\"" in line:
                        return True
            # 过滤掉近端历史字符串写入key获取
            if file_path.__contains__('/near/'):
                with open(file_path, 'r', encoding='utf-8') as file:
                    for line in file:
                        if "'"+key_clear+"'" in line:
                            return True
                        if "\""+key_clear+"\"" in line:
                            return True
        
        
                    
    except Exception as e:
        print(f"Error reading {file_path}: {e}")

    return False

def traverse_and_search(directory:str, keyword:str, near_local_json_path:str):
    """Traverse the directory and search for the keyword in each file."""
    lowercase_key = (str(keyword[0]).lower() + keyword[1:len(keyword)])
    isUsed = False
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file == '.DS_Store':
                continue
            file_path = os.path.join(root, file)
            if search_keyword_in_file(file_path, lowercase_key, near_local_json_path):
                isUsed = True
    
    return isUsed

def checkUnUsedKeyArr(json:dict,frontKeys:list, near_local_json_path:str):
    tempArr = []
    for k, v in json.items():
        if str(v.__class__).__contains__('dict'):
            next_frontKeys = []
            next_frontKeys.extend(frontKeys)
            next_frontKeys.append(k)
            temp = checkUnUsedKeyArr(v,next_frontKeys, near_local_json_path)
            tempArr.extend(temp)
        else:
            key = ''
            if len(frontKeys) == 0 :
                key = k
            else:
                key = frontKeys[0]
                for item in frontKeys[1:]:
                    key = key + (item[0].upper() + item[1:len(item)])
                key = key + (k[0].upper() + k[1:len(k)])
            isUsed = traverse_and_search(root_path+'/lib/', key, near_local_json_path)
            if isUsed == False:
                key_arr_str = ''
                for item in frontKeys:
                    key_arr_str = key_arr_str + item + '_'
                key_arr_str = key_arr_str + k
                print(key_arr_str)
                tempArr.append(key_arr_str)
    return tempArr

def removeLocalesKeys(unUsedKeys:list,locals_dir:str):
    for root, dirs, files in os.walk(locals_dir):
        for file in files:
            if file == '.DS_Store'or file == 'locales.g.dart':
                continue
            file_path = os.path.join(root, file)
            with open(file_path, 'r') as f:
                json_content = f.read()
            temp_json_content:dict = json.loads(json_content)
            for item in unUsedKeys:
                keyArr:list = item.split('_')
                if len(keyArr) == 0:
                    temp_json_content.pop(item)
                else:
                    deal_json:dict = temp_json_content
                    for cell in keyArr[:-1]:
                       deal_json = deal_json[cell]
                    deal_json.pop(keyArr[-1])
            
            merge_json_data = json.dumps(temp_json_content,ensure_ascii=False,indent=2)    
            with open(file_path, 'w') as f:
                f.write(merge_json_data)
        

if __name__ == "__main__":
    # root_path = os.path.abspath(os.path.dirname(__file__)+os.path.sep+"..")
    root_path = input('请输入项目根目录文件地址:')
    root_path = root_path.removeprefix("'")
    root_path = root_path.removesuffix("'")
    root_path = root_path.removesuffix("/")
    locales_file_path = root_path + '/assets/locales/zh_CN.json'
    locals_dir = root_path + '/assets/locales/'
    near_local_json_path = root_path+'/assets/json/debug.json'
    with open(locales_file_path, 'r') as f:
        content = f.read()
    # 文件中的json
    json_content = json.loads(content)
    unUsedKeys = checkUnUsedKeyArr(json_content,[], near_local_json_path)

    # 清理无用key
    removeLocalesKeys(unUsedKeys, locals_dir)
    os.system('python3 ' + root_path + '/scripts/locales_tool.py')
