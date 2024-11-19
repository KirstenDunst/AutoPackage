<!--
 * @Author: Cao Shixin
 * @Date: 2023-02-17 10:10:56
 * @LastEditors: Cao Shixin
 * @LastEditTime: 2023-02-17 10:37:08
 * @Description: 
-->
# asset_tool.py

功能介绍：主要是为了方便导入1倍、2倍、3倍资源图使用。功能包括将原来文件重命名为自定义的名称，并存放在对应assets/images下的对应倍图文件夹下；<br><br>

使用介绍：（安装python环境）<br>
```
//运行命令
python3 scripts/asset_tool.py 
//回车之后提示需要你处理的源文件,拖入1倍图地址即可
拖入项目中打算加入项目的1倍png文件地址:'/Users/mac322865/Downloads/组12453.png'
//想要放入项目的名称（不用加后缀，后缀是直接用原来的后缀格式）
放入项目之后的名称:ic_prosthesis_height_detail
```
<br><br>

# locales_tool.py

功能介绍: 便于执行将assets/locales/下的国际化字段转化为项目里面使用的静态字符常量文件：lib/generated/locales.g.dart(这个文件每次运行脚本会覆盖，所以不要在里面手动编辑，避免丢失)<br><br>

使用介绍：
```python
python3 scripts/locales_tool.py
```


# excel_json_tool.py

功能介绍：便于开发将翻译人员提供的excel文件，按照现有的中文国际化json模版翻译或者补充成对应的国际化文件<br><br>

使用介绍：
```python
python3 scripts/excel_json_tool.py
# 会提示先拖入翻译对比好的excel的文件路径（这里脚本目前按照第一列是中文来处理的，后面如果有改动再调整）然后回车
# 提示拖入已存在国际化的中文国际化json文件地址（用于按照这个json为模版替换对应语言的value值），然后回车
# 提示excel里面的列和语言Local的对应关系，多个之间用逗号隔开，然后回车开始执行
```
<br>会在assets/locales文件夹下生成对应的local命名的json文件，结构同中文国际化json结构一致。另外会将excel里面没有遇到的中文国际化里面的翻译摘出来按照原有结构保存在notrans.json里面，以供下次翻译使用。<br><br>

Alert:执行期间如果遇到本地已存在对应国际化的json文件，会提示：忽略(使用本地，不做修改，跳过执行下一个)，覆盖(将本地擦除，写入excel独到的文件，相当于第一次执行脚本新生成的json)，合并（本地独有的key不做修改，没有的key添加到本地，value有调整的以excel为准，推荐使用）<br><br>

# locales_add.py
核心翻译使用DeepLX：https://github.com/OwO-Network/DeepLX (DeepL api：https://www.deepl.com/需要注册绑定信用卡，暂时不支持中国信用卡，且有50万字符每月的限制),使用的时候由于api防止恶意访问有限制，如果批量请求会被限制ip的访问。所采用使用安装软件的方式，请求走本地软件的请求绕开直接的访问的问题。可解决。所以前置条件需要参照链接安装一下软件，然后脚本才有效。
```pip install requests pandas```

功能介绍：开发的时候新增国际化的工具，执行的时候会在assets/locales/下生成一个todo.json将需要新增的中文对应的json结构放置在里面，在终端输入c回车，开始执行。<br>
执行完之后可直接在项目里面使用LocaleKeys.对应的key.tr使用（这个脚本附带了locales_tool.py的执行）<br><br>

Alert:
support language: https://developers.deepl.com/docs/v/zh/resources/supported-languages

执行过程中有中文提示：
Result:*-->*:*表示打印出当前翻译的内容翻译成(-->)什么语言：接口响应的内容(gpt接口响应可能会有一些特殊字符之类的，可以主观鉴别一下)<br>
Error:****表示那句中文翻译成什么语言出错。需要手动在对应语言json文件中将对应value用其他语言翻译好之后替换，全部替换完成之后再手动执行locales_tool.py脚本，生成对应的字符常量key，让后再项目里面LocaleKeys.对应的key.tr使用<br><br>

# locales_delete.py
功能介绍：删除国际化key,多个key之间用英文逗号隔开（key为复合key，比如多级json即使用大驼峰拼接后的key）

# json_2_locales.py
功能介绍：用于发布前将线上平台运维国际化覆盖本地国际化文件

# json_key_compare.py
功能介绍: 用于比对两个json文件的key是否有特殊key的存在<br><br>

使用介绍：（安装python环境）<br>
```
//运行命令
python3 /Users/mac322865/Project/inverter/hyx_inverter/scripts/json_key_compare.py
//回车之后提示输入对应的第一个json文件路径，回车再输入第二个json文件地址
输入第一个json文件地址:'/Users/mac322865/Project/inverter/hyx_inverter/lib/l10n/intl_en.arb'
输入第二个json文件地址:'/Users/mac322865/Project/inverter/hyx_inverter/lib/l10n/intl_zh.arb'
//回车执行操作比对结果
```

# json_check_value.py
功能介绍: 用于比对某一个json中是否存在重复value的内容，并将重复的value输出


<br><br>

## 其他
如果图片过大，或者转格式，可以先用 https://squoosh.app 来处理
<br><br><br><br><br><br><br><br><br>

