### Lottie动画文件压缩优化命令行程序：tiny-lottie


<br>

>博客地址:https://www.jianshu.com/p/a640716ad221

<br>
在需要批处理的文件夹下运行如下命令,将批量处理文件夹下所有*.json文件。

###### Windows环境
```
tiny-lottie.exe -q 75 -p
```
###### Mac/Linux环境
```
python tiny-lottie.py -q 75
```

### 命令行参数
```
usage: TinyLottie [-h] [-d directory] [-q quality] [-o] [-p]

Lottie文件批处理工具, 支持使用webp图片压缩Lottie文件

optional arguments:
  -h, --help            show this help message and exit
  -d directory, --dir directory 运行文件夹，默认当前文件夹
  -q quality, --quality quality 质量百分比[0-100]，Webp图片压缩率，数字越大质量越高
  -o, --overwrite       是否覆盖源文件
  -p, --pause           执行完是否暂停窗口以便查看输出
```

使用效果<br>
![Lottie文件压缩.png](src/image/13651212-3fcca4fa78fbc6f0.webp.jpg)
