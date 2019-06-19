# AutomicPack
自动打包并上传蒲公英，基于shell的一种处理方式

# 使用方法
首先可以在你的项目中的info.plist文件中加入两个key，用来加入你所创建的蒲公英的apiKey和uerKey(不配置的话也没有问题，执行sh文件的时候会有提醒的)

 LEPgyerApiKey 在Info.plist中配置蒲公英apiKey
 LEPgyerUKey 在Info.plist中配置蒲公英ukey


1-下载pkgtopgy.sh至任意目录 
2-终端新建窗口 输入sh （sh+空格），然后拖入文件 pkgtopgy.sh 回车 （也可以右击-显示简介-打开方式设置为终端，然后双击打开）

(按照提示来，如果上面的蒲公英你已经配置好了，那么这里终端上只会有一个打包输出的路径需要你选择，自己找一个路径就好了)



# 使用问题
项目里面的环境是需要自己配的！
项目里面的环境是需要自己配的！
项目里面的环境是需要自己配的！
pkgtopgy.sh 中的109行、111行，需要根据项目中的环境调整一下！
pkgtopgy.sh 中的109行、111行，需要根据项目中的环境调整一下！
pkgtopgy.sh 中的109行、111行，需要根据项目中的环境调整一下！


# 环境问题
首先你需要安装python环境，
使用前：
安装pip
sudo easy_install pip
安装json-query
pip install json-query 
安装 gym
pip install gym

如果运行的时候会报错： line 39: gym: command not found问题，
那么终端执行：sudo gem install gym
                    （sudo gem install gym -n /usr/local/bin）
                    

fastlane环境安装：

如果用的是mac自带的ruby，需要 sudo权限
使用: sudo gem install fastlane

如果报错：ERROR: While executing gem ... (Errno::EPERM) Operation not permitted - /usr/bin/commander 
使用: sudo gem install -n /usr/local/bin fastlane

初始化：
在项目根目录下，初始化Fastlane：
fastlane init

新版本安装的时候出现了下面的分支选择，按要求选择就行

1. 📸  Automate screenshots
2. 👩‍✈️  Automate beta distribution to TestFlight (自动testfilght型配置)
3. 🚀  Automate App Store distribution (自动发布型配置)
4. 🛠  Manual setup - manually setup your project to automate your (需要手动配置内容)



