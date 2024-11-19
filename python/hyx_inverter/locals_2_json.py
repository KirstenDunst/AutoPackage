import json
import os

from common_tool import CommonTool


if __name__ == "__main__":
    locals_path = input("请输入国际化文件夹目录:")
    save_file_path = input("请输入生成json的文件地址:")

    locals_path = locals_path.removeprefix("'")
    locals_path = locals_path.removesuffix("'")
    save_file_path = save_file_path.removeprefix("'")
    save_file_path = save_file_path.removesuffix("'")

    language_locales = {}
    file_list = os.listdir(locals_path)
    for file_name in file_list:
        if file_name.endswith(".json"):
            if file_name.__contains__("_"):
                file_path = os.path.join(locals_path, file_name)
                with open(file_path, "r") as f:
                    content = f.read()
                # 文件中的json
                json_content = json.loads(content)
                f.close()

                language_locales[file_name.split("_")[0]] = CommonTool.tranformDict(
                    json_content, ""
                )
            else:
                continue
        else:
            continue

    local_dict: dict = list(language_locales.values())[0]
    save_dict = {}
    for k, v in local_dict.items():
        cell_dict = {"remark": ""}
        local_dict = {}
        for lk, lv in language_locales.items():
            local_dict[lk] = lv[k] +'12'
        cell_dict["local"] = local_dict
        save_dict[k] = cell_dict

    with open(save_file_path, "w") as f1:
        f1.write(json.dumps(save_dict, ensure_ascii=False, indent=2))
    f1.close()
