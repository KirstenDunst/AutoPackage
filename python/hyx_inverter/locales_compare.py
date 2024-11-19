# 国际化对比，用于平台运维国际化文件从一个环境往另一个环境导入时做比对得出增量国际化使用


import json
import os

from common_tool import CommonTool


if __name__ == "__main__":
    compare_dir = input(
        """请创建一个空文件夹,将源文件命名为a.json,待比对文件命名为b.json(例如：从dev环境迁移到test环境，则dev环境下载的文件命名为a.json, test环境下载的文件命名为b.json),\n
执行完成之后会多生成3个文件，分别为:\n
a_b.json (a.json比b.json多的国际化,无则没有此文件)\n
b_a.json (b.json比a.json多的国际化,无则没有此文件)\n
a_b_local.json (a_b.json与当前分支的本地国际化比对，存在本地国际化的key过滤,无则没有此文件 即：导入test环境的json文件)\n
请输入这个空文件夹地址:"""
    )
    compare_dir = compare_dir.removeprefix("'")
    compare_dir = compare_dir.removesuffix("'")

    a_json_path = compare_dir + "/a.json"
    with open(a_json_path, "r") as fa:
        a_content = fa.read()
    a_json_content: dict = json.loads(a_content)
    fa.close()

    b_json_path = compare_dir + "/b.json"
    with open(b_json_path, "r") as fb:
        b_content = fb.read()
    b_json_content: dict = json.loads(b_content)
    fb.close()

    # 至少有中文
    a_keys = list(a_json_content.keys())

    a_b_dict = {}
    for ele in a_keys:
        if ele in b_json_content:
            b_json_content.pop(ele)
        else:
            a_b_dict[ele] = a_json_content[ele]

    a_b_path = compare_dir + "/a_b.json"
    if os.path.exists(a_b_path):
        os.remove(a_b_path)
    a_b_local_path = compare_dir + "/a_b_local.json"
    if os.path.exists(a_b_local_path):
        os.remove(a_b_local_path)
    b_a_path = compare_dir + "/b_a.json"
    if os.path.exists(b_a_path):
        os.remove(b_a_path)

    if len(a_b_dict) > 0:
        # 核对翻译不能有空
        for k, v in a_b_dict.items():
            if "" in v["local"].values():
                exit(f"a_b_json中{k}下local中有value是空字符串存在")

        with open(a_b_path, "w") as fab:
            fab.write(json.dumps(a_b_dict, ensure_ascii=False, indent=2))
        fab.close()

        # 核对本地locales的key
        root_path = os.path.abspath(os.path.dirname(__file__) + os.path.sep + "..")
        zh_local_path = root_path + "/assets/locales/zh_CN.json"
        with open(zh_local_path, "r") as fzh:
            zh_local_content = fzh.read()
        zh_local_json_content = json.loads(zh_local_content)
        fzh.close()
        zh_local_json_content = CommonTool.tranformDict(zh_local_json_content)
        
        a_b_local = {}
        for tk, tv in a_b_dict.items():
            if tk in zh_local_json_content:
                a_b_local[tk] = tv

        if len(a_b_local) > 0:
            with open(a_b_local_path, "w") as fabl:
                fabl.write(json.dumps(a_b_local, ensure_ascii=False, indent=2))
            fabl.close()

    if len(b_json_content) > 0:
        with open(b_a_path, "w") as fba:
            fba.write(json.dumps(b_json_content, ensure_ascii=False, indent=2))
        fba.close()
