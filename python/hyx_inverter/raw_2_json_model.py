import json
import os


class FileFolderOperate:
    @staticmethod
    def contain_text(file_path, target_string) -> bool:
        """
        是否包含某个内容
        """
        if os.path.exists(file_path):
            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    content = file.read()
                    if target_string in content:
                        return True
                return False
            except FileNotFoundError:
                print(f"The file {file_path} does not exist.")
                return False
            except Exception as e:
                print(f"An error occurred: {e}")
                return False
        else:
            exit("文件路径不存在")

    @staticmethod
    def trans_json_2_model(raw_key: str, raw_content: dict, isRequired: bool):
        nowClassContent = ""
        cellClassContent = ""

        type = raw_content["type"] if raw_content.__contains__("type") else ""
        description = (
            raw_content["description"]
            if raw_content.__contains__("description")
            else ""
        )
        nowClassContent += "  //"
        nowClassContent += description if description != None else ""
        nowClassContent += "\n  final "
        required: list = (
            raw_content["required"] if raw_content.__contains__("required") else []
        )
        if type == "object":
            object_cell_name = FileFolderOperate.firstByteUpper(raw_key) + "NetModel"
            nowClassContent += object_cell_name

            properties: dict = (
                raw_content["properties"]
                if raw_content.__contains__("properties")
                else {}
            )
            object_back, object_arr = FileFolderOperate.trans_json_2_model_cell(
                object_cell_name, properties, required
            )
            cellClassContent += object_back
            for item in object_arr:
                cellClassContent += item

        elif type == "array":
            items: dict = (
                raw_content["items"] if raw_content.__contains__("items") else {}
            )
            item_type_trans = FileFolderOperate.baseTypeTrans(items["type"])
            if len(item_type_trans) > 1:
                nowClassContent += "List<"
                nowClassContent += item_type_trans
                nowClassContent += ">"
            else:
                arr_cell_name = FileFolderOperate.firstByteUpper(raw_key) + "NetModel"
                nowClassContent += "List<"
                nowClassContent += arr_cell_name
                nowClassContent += ">"
                # 这里暂时没有考虑数组套数组，所以这里只有object
                arr_back, arrback_arr = FileFolderOperate.trans_json_2_model_cell(
                    arr_cell_name,
                    items["properties"] if items.__contains__("properties") else {},
                    items["required"] if items.__contains__("required") else [],
                )
                cellClassContent += arr_back
                for item in arrback_arr:
                    cellClassContent += item
        else:
            type_trans = FileFolderOperate.baseTypeTrans(type)
            nowClassContent += type_trans

        # nowClassContent += (''if isRequired else '?')
        # 项目需要这里都设置可为空(根据文档的话用上面注释部分)
        nowClassContent += "?"

        nowClassContent += " "
        nowClassContent += raw_key
        nowClassContent += ";\n"

        return nowClassContent, cellClassContent

    @staticmethod
    def trans_json_2_model_cell(class_name: str, raw_content: dict, required: list):
        sub_content_arr = []
        cellClassContent = "\n@JsonSerializable()\nclass "
        cellClassContent += class_name
        cellClassContent += "{\n"
        content_temp = "  "
        content_temp += class_name
        content_temp += "("
        for key, value in raw_content.items():
            arr_back_content, arr_back_subcontent = (
                FileFolderOperate.trans_json_2_model(
                    key, value, required.__contains__(key)
                )
            )
            sub_content_arr.append(arr_back_subcontent)
            cellClassContent += arr_back_content
            content_temp += "\n      this."
            content_temp += key
            content_temp += ","

        cellClassContent += "\n"
        cellClassContent += content_temp
        cellClassContent += ");\n\n"
        cellClassContent += "  factory "
        cellClassContent += class_name
        cellClassContent += ".fromJson(Map<String, dynamic> json) => _$"
        cellClassContent += class_name
        cellClassContent += "FromJson(json);\n\n"

        cellClassContent += "  Map<String, dynamic> toJson() => _$"
        cellClassContent += class_name
        cellClassContent += "ToJson(this);\n}\n"

        return cellClassContent, sub_content_arr

    @staticmethod
    def firstByteUpper(content: str) -> str:
        return content[0].upper() + content[1:]

    @staticmethod
    def baseTypeTrans(key: str) -> str:
        trans_map = {
            "string": "String",
            "number": "num",
            "integer": "int",
            "boolean": "bool",
        }
        return trans_map[key] if trans_map.__contains__(key) else ""


if __name__ == "__main__":
    root_path = os.path.abspath(os.path.dirname(__file__) + os.path.sep + "..")
    source_dir = root_path + "/assets/json/"
    todo_json_file = source_dir + "raw.json"
    if os.path.exists(todo_json_file):
        os.remove(todo_json_file)
    file = open(todo_json_file, "w")
    file.write("{\n}")  # 写入内容信息
    file.close()

    is_continue = input(
        "已创建待转化json模型的raw(data包含的内部raw) json文件,路径assets/json/raw.json,填写完成后输入C以继续:"
    )
    if not is_continue.upper() == "C":
        os.remove(todo_json_file)
        exit("您已中断执行")
    with open(todo_json_file, "r", encoding="utf-8") as f:
        raw_json: dict = json.load(f)

    save_model_path = input("转化之后的模型存储的dart文件位置:")
    save_model_path = save_model_path.removeprefix("'")
    save_model_path = save_model_path.removesuffix("'")
    base_model_name = input("层级根模型名称[大驼峰规则eg: DeviceHisNetModel]:")
    with open(save_model_path, "r") as f:
        content = f.read()
    save_file_name = os.path.basename(save_model_path)

    head_input = "import 'package:json_annotation/json_annotation.dart';"
    part_input = "part '" + save_file_name.replace(".dart", ".g.dart") + "';"
    contain_header = FileFolderOperate.contain_text(save_model_path, head_input)
    contain_part = FileFolderOperate.contain_text(save_model_path, part_input)

    new_content = ""
    if contain_header == False:
        new_content += head_input
        new_content += "\n"
    if contain_part == False:
        new_content += part_input
        new_content += "\n"

    new_content += content
    new_content += "\n"

    if not base_model_name.endswith("NetModel"):
        base_model_name += "NetModel"

    base_dict = {}
    if raw_json.__contains__("properties"):
        # object类型
        base_dict = raw_json
    elif raw_json.__contains__("items"):
        # array类型
        base_dict = raw_json["items"]
    trans_content, sub_content_arr = FileFolderOperate.trans_json_2_model_cell(
        FileFolderOperate.firstByteUpper(base_model_name),
        base_dict["properties"],
        base_dict["required"] if base_dict.__contains__("required") else [],
    )
    new_content += trans_content
    for item in sub_content_arr:
        new_content += item

    with open(save_model_path, "w") as f:
        f.write(new_content)

    os.remove(todo_json_file)
