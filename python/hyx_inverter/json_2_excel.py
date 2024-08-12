import json
import os

from openpyxl import Workbook

from excel_json_tool import ExcelTool

if __name__ == '__main__':
    locale_dir = input('json文件所在文件夹地址:')
    locale_dir = locale_dir.removeprefix("'")
    locale_dir = locale_dir.removesuffix("'")
    
    out_excel_dir = input('输出文件的文件夹路径:')
    out_excel_file = os.path.join(out_excel_dir,'transform.xlsx')
    
    if not os.path.exists(locale_dir):
        exit('文件夹地址异常：'+locale_dir)
    
    trans_dict:dict = {}
    file_names = os.listdir(locale_dir)
    for filename in file_names:
        splits = filename.split('.')
        if splits[-1] == 'json':
            file_path = os.path.join(locale_dir, filename)
            with open(file_path, 'r') as f:
                content = f.read()
            # 文件中的json
            json_content:dict = json.loads(content)
            trans_dict[splits[0]] = ExcelTool.transToDirectDict(json_content,'')
    
    excel_title = ['中文','英语','德语','西班牙语','法语','葡萄牙语','意大利语','波兰语','荷兰语','日语']
    language_code_arr = ['zh_CN', 'en_US','de_DE','es_ES','fr_FR','pt_PT','it_IT','pl_PL','nl_NL','ja_JP']
    
    outwb = Workbook()
    outws = outwb.worksheets[0] 
    outws.append(excel_title)
        
    for k, v in trans_dict['zh_CN'].items():
        a_list = [v]
        for language_code in language_code_arr[1:]:
            if language_code in trans_dict.keys():
                a_list.append(trans_dict[language_code][k])
        outws.append(a_list)       
            
    if os.path.exists(out_excel_file):
        os.remove(out_excel_file)
    outwb.save(out_excel_file)