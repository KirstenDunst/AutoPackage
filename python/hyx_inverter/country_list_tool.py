# 注册使用的国家列表展示调整

import json
import os


if __name__ == '__main__':
    dir = input('输入待处理文件夹路径:')
    dir = dir.removeprefix("'")
    dir = dir.removesuffix("'")
    locals_dir = input('国际化文件夹路径:')
    locals_dir = locals_dir.removeprefix("'")
    locals_dir = locals_dir.removesuffix("'")
    
    local_save_key = 'countryName'
    
    trans_dict:dict = {}
    # 清单字典
    list_dict:dict = {}
    file_names = os.listdir(dir)
    for filename in file_names:
        splits = filename.split('.')
        if splits[-1] == 'json':
            file_path = os.path.join(dir, filename)
            with open(file_path, 'r',encoding='utf-8-sig') as f:
                content = f.read()
            # 文件中的json
            json_content:dict = json.loads(content)
            temp_list:list = json_content['data']
            add_country_locale:dict = {}
            temp_list_dict:dict = {}
            for item in temp_list:
                onlyKey:str = item['nation']
                # onlyKey = onlyKey.replace('(','')
                # onlyKey = onlyKey.replace(')','')
                # onlyKey = onlyKey.replace("'","")
                # onlyKey = onlyKey.replace(',',"")
                # onlyKey = onlyKey.replace('-',"")
                # onlyKey = onlyKey.replace('ç','c')
                # onlyKey = onlyKey.replace('ô',"o")
                # # key_split_arr = onlyKey.split(' ')
                # # first_split_key = key_split_arr[0]
                key_conbine = onlyKey.replace(" ","")
                if add_country_locale.__contains__(key_conbine):
                    print(key_conbine)
                add_country_locale[key_conbine] = item['nationName']
                local_key_use = (str(key_conbine[0]).upper() + key_conbine[1:len(key_conbine)])
                nationDict = {'nation':local_key_use}
                if temp_list_dict.__contains__(item['nodeCode']):
                    childs:list = temp_list_dict[item['nodeCode']]['nationList']
                    childs.append(nationDict)
                else:
                    temp_list_dict[item['nodeCode']] = {'nodeUrl':item['nodeUrl'],'nodeCode':item['nodeCode'],'nationList':[nationDict]}
            #执行一次即可
            if len(list_dict) == 0:
                list_dict = temp_list_dict
            trans_dict[splits[0]] = add_country_locale
                    
    
    
    for k,v in trans_dict.items():
        # 读取原数据，合并json
        file_path = locals_dir +'/' + k + '.json'
        with open(file_path, 'r') as f:
            json_content = f.read()
        temp_json_content:dict = json.loads(json_content)
        temp_json_content[local_save_key] = v
        # 写入文件
        merge_json_data = json.dumps(temp_json_content,ensure_ascii=False,indent=2)
        with open(file_path, 'w') as f:
            f.write(merge_json_data)
    
    qing_dan_content = []
    qing_dan_index = 1
    for k, v in list_dict.items():
        newDict = {}
        newDict.update(v)
        for ite in newDict['nationList']:
            ite['nationCode'] = qing_dan_index
            qing_dan_index = qing_dan_index+1
        qing_dan_content.append(newDict)
    qing_dan_path = locals_dir + '/country.json'
    qing_dan_data = json.dumps(qing_dan_content,ensure_ascii=False,indent=2)
    with open(qing_dan_path, 'w') as f1:
        f1.write(qing_dan_data)
    f1.close()
    