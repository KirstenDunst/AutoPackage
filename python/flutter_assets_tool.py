'''
Author: Cao Shixin
Date: 2022-08-03 15:54:07
LastEditors: Cao Shixin
LastEditTime: 2022-10-26 15:27:45
Description: 给flutter项目添加assets的资源到项目中
'''
import os


class FlutterAssetsTool(object):
    def __init__(self, project_path, assets_path, asset_file_path):
        # flutter 项目根路径
        self.pubspec_path = project_path + '/pubspec.yaml'
        # 资源文件夹最外层路径
        self.assets_path = assets_path
        # 项目引用资源文件的路径
        self.asset_file_path = asset_file_path

    def generated(self):
        asset_dir_names = self.assets_path.split('/')
        while '' in asset_dir_names:
            asset_dir_names.remove('')
        asset_dir_name = asset_dir_names[-1]
        print(asset_dir_name)
        f0 = open(self.asset_file_path, "r")
        f0Content = f0.read()
        f0.close()
        if not f0Content.__contains__("const String _assets = '" +
                                      asset_dir_name + "/';"):
            t0 = f0Content.__add__("const String _assets = '" +
                                   asset_dir_name + "/';\n")
            with open(self.asset_file_path, "w") as f0Add:
                f0Add.write(t0)
        for root, dirs, files in os.walk(self.assets_path):
            while '.DS_Store' in files:
                files.remove('.DS_Store')
            print('root_dir:', root)  # 当前路径
            print('sub_dirs:', dirs)  # 子文件夹
            print('files:', files)  # 文件名称，返回list类型
            self.__write__(files=files,
                           root=root,
                           asset_dir_name=asset_dir_name)

    def __write__(self, files, root: str, asset_dir_name):
        if root == self.assets_path:
            if len(files) > 0:
                # 添加到yaml文件
                for item in files:
                    yamlAdd = '- ' + asset_dir_name + '/' + item
                    f1 = open(self.pubspec_path, "r")
                    content = f1.read()
                    f1.close()
                    if not content.__contains__(yamlAdd):
                        t = content.replace('assets:',
                                            'assets:\n    ' + yamlAdd)
                        with open(self.pubspec_path, "w") as f2:
                            f2.write(t)
        else:
            sub: str = root.replace(self.assets_path, '')
            yamlAdd = '- ' + asset_dir_name + '/' + sub + '/'
            f1 = open(self.pubspec_path, "r")
            content = f1.read()
            f1.close()
            if not content.__contains__(yamlAdd):
                t = content.replace('assets:', 'assets:\n    ' + yamlAdd)
                with open(self.pubspec_path, "w") as f2:
                    f2.write(t)
            # 引用文件
            subs = sub.split('/')
            while '' in subs:
                subs.remove('')
            if len(sub) == 0:
                return
            addClass = subs[0]
            f3 = open(self.asset_file_path, "r")
            asset_file_content = f3.read()
            f3.close()
            class_verify = 'class ' + addClass.title() + ' {'
            baseProfix = "static const String prefix = '${_assets}" + \
                addClass + "/';"
            if not asset_file_content.__contains__(class_verify):
                t = asset_file_content.__add__(class_verify + "\n  " +
                                               baseProfix + "}\n")
                with open(self.asset_file_path, "w") as f4:
                    f4.write(t)

            # 内部引用补充
            profix = 'prefix'
            if len(subs) > 1:
                profix = subs[1]
                if len(subs) > 2:
                    for item in subs[2:]:
                        profix += item.title()
                profix = profix.replace('_', '')
                profix = profix.replace('-', '')
                profix += (addClass.title() + 'Prefix')
                yamlAdd1 = "static const String " + profix + " = '${prefix}" + sub.replace(
                    addClass + '/', '') + "/';"
                f1 = open(self.asset_file_path, "r")
                content = f1.read()
                f1.close()
                if not content.__contains__(yamlAdd1):
                    t = content.replace(baseProfix,
                                        baseProfix + '\n  ' + yamlAdd1)
                    with open(self.asset_file_path, "w") as f2:
                        f2.write(t)
            else:
                yamlAdd1 = baseProfix

            file_name_dic = {}

            name_front1 = sub.replace(addClass, '')
            name_front1 = name_front1.replace('/', '')
            name_front1 = name_front1.replace('_', '')
            name_front1 = name_front1.replace('-', '')
            name_front_arr = name_front1.split('/')
            while '' in name_front_arr:
                name_front_arr.remove('')

            name = ''
            if len(name_front_arr) > 0:
                name_frint_end = name_front_arr[0]
                for item in name_front_arr[1:]:
                    name_frint_end += item.title()
                name = name_frint_end

            for item in files:
                name_front = item.split('.')[0]
                names = []
                file_names = name_front.split('-')
                for item1 in file_names:
                    temp_arr = item1.split('_')
                    for item2 in temp_arr:
                        names.append(item2)
                while '' in names:
                    names.remove('')

                frontName = name
                if frontName != '':
                    for item2 in names:
                        frontName += item2.title()
                else:
                    frontName = names[0]
                    for item2 in names[1:]:
                        frontName += item2.title()

                file_name_dic[frontName] = item

            for key, value in file_name_dic.items():
                file_profix = "static const String " + key + \
                    " = '${" + profix + "}" + value + "';"
                f1 = open(self.asset_file_path, "r")
                content = f1.read()
                f1.close()
                if not content.__contains__(file_profix):
                    t = content.replace(yamlAdd1,
                                        yamlAdd1 + '\n  ' + file_profix)
                    with open(self.asset_file_path, "w") as f2:
                        f2.write(t)


if __name__ == '__main__':
    project_path = input('请输入flutter项目跟路径:')
    assets_path = input('请输入项目资源文件夹地址(eg:assets文件夹):')
    asset_file_path = input('请输入项目引用资源文件地址:')
    FlutterAssetsTool(project_path=project_path,
                      asset_file_path=asset_file_path,
                      assets_path=assets_path).generated()
    # FlutterAssetsTool(
    #     project_path='/Users/caoshixin/Company/Project/starkid_game/',
    #     assets_path='/Users/caoshixin/Company/Project/starkid_game/assets/',
    #     asset_file_path='/Users/caoshixin/Company/Project/starkid_game/lib/common/assets.dart'
    # ).generated()
