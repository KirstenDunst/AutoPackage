# AutomicPack
自动打包并上传蒲公英，基于fastlane的一种处理方式


# 环境问题
1.安装
加上 -n /usr/local/bin是因为Mac OS X 10.11 已经禁止修改/usr/bin目录了

$ sudo gem install fastlane -n /usr/local/bin
$ sudo gem install firim -n /usr/local/bin


2.初始化
$ cd + (你的项目路径)
$ fastlane init

3.安装插件

$ fastlane add_plugin versioning
$ fastlane add_plugin firim

途中，你可能需要按y进行确认


4.项目打包配置
打开项目文件夹下fastlane里边的Fastlane文件
修改成上面的两个文件的内容


5.执行打包上传命令

$ fastlane archive

（其中上面的archive是指的你的Fastlane文件中配置的lane的名称）
