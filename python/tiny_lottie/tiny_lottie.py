#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author: Cao Shixin
Date: 2023-03-27 16:24:59
LastEditors: Cao Shixin
LastEditTime: 2023-03-27 16:29:20
Description: 
'''
import base64
import file as File
from PIL import Image
import demjson
import argparse
import traceback



if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="TinyLottie", description="Lottie文件批处理工具, 支持使用webp图片压缩Lottie文件")
    parser.add_argument("-d", "--dir", type=str, metavar="directory", required=False, dest="directory", default=".",
                        help="运行文件夹")
    parser.add_argument("-q", "--quality", type=int, metavar="quality", required=False, dest="quality", default=75,
                        help="质量百分比[0-100]")
    # parser.add_argument("-r", "--reformat", action="store_true", dest="reformat", default=False,
    #                     help="webp文件是否需要重新压缩")
    parser.add_argument("-o", "--overwrite", action="store_true", dest="overwrite", default=False,
                        help="是否覆盖源文件")
    parser.add_argument("-p", "--pause", action="store_true", dest="pause", default=False,
                        help="执行完是否暂停窗口以便查看输出")
    args = parser.parse_args()
    quality = args.quality
    # reformat = args.reformat
    overwrite = args.overwrite
    pause = args.pause
    # print("reformat: %s" % reformat)
    # print("overwrite: %s" % overwrite)
    print("Working on: [%s]" % (args.directory + File.separator))
    if args.directory:
        directory = File.File(args.directory)
        if directory.exists() and directory.isDirectory():
            tempDir = File.File(args.directory + File.separator + "lottie_temp" + File.separator)
            outputDir = File.File(args.directory + File.separator + "output" + File.separator)
            if outputDir.exists():
                outputDir.delete()
            if not tempDir.exists():
                tempDir.makedirs()
            else:
                # 删除临时文件夹内文件
                for t in tempDir.listFile():
                    t.delete()
            d_list = []
            s_list = []
            for json_file in directory.listFile():
                if json_file.isFile():
                    json_file_name = json_file.getName()
                    if json_file_name.endswith(".json"):
                        try:
                            print("Processing...[%s]" % json_file_name)
                            json_fd = open(json_file.getPath(), "rt", encoding="utf-8")
                            json_str = json_fd.read()
                            json_fd.close()
                            json_obj = demjson.decode(json_str, encoding="utf-8")
                            if "assets" in json_obj:
                                assets = json_obj["assets"]
                                total_len = len(assets)
                                count = 0
                                process_flag = False
                                for png_item in assets:
                                    count = count + 1
                                    if "p" in png_item and "id" in png_item:
                                        p = png_item["p"]
                                        name_id = png_item["id"]
                                        # data:image/png;base64,
                                        if p.startswith("data:image/"):
                                            p1 = p[p.index(","):]
                                            source_file_path = tempDir.getPath() + name_id
                                            fd = open(source_file_path, "wb+")
                                            fd.write(base64.b64decode(p1))
                                            fd.close()
                                            tmp_file_path = tempDir.getPath() + name_id + ".webp"
                                            im = Image.open(source_file_path).convert("RGBA")
                                            im.save(tmp_file_path, "WEBP", quality=quality, method=6)
                                            source_file = File.File(source_file_path)
                                            tmp_file = File.File(tmp_file_path)
                                            s_size = source_file.length()
                                            t_size = tmp_file.length()
                                            pp = (s_size - t_size) / s_size * 100
                                            if pp < 0:
                                                x = (-pp, ((t_size - s_size) / 1024), source_file_path)
                                                print("膨胀:%.5G%%\t +%.5g Kbs\t [%s]\t不处理..." % x)
                                            else:
                                                x = (pp, ((s_size - t_size) / 1024), source_file_path)
                                                print("压缩:%.5G%%\t -%.5g Kbs\t [%s]" % x)
                                                rs = open(tmp_file_path, 'rb').read()
                                                bs = base64.b64encode(rs)
                                                pb = "data:image/webp;base64," + bs.decode("utf-8")
                                                # png_item["p"] = pb
                                                json_str = json_str.replace(p, pb)
                                                process_flag = True
                                            source_file.delete()
                                            tmp_file.delete()
                                if process_flag:
                                    # json_obj["assets"] = assets
                                    # xs = demjson.encode(json_obj, encoding="utf-8")
                                    tmp_json_file_path = tempDir.getPath() + json_file_name
                                    t_file = open(tmp_json_file_path, "w+", encoding="utf-8")
                                    # t_file.write(xs.decode("utf-8"))
                                    t_file.write(json_str)
                                    t_file.close()
                                    s_list.append(json_file)
                                    d_list.append(File.File(tmp_json_file_path))
                        except Exception as e:
                            print("文件处理异常[%s]" % json_file_name, e)
                            traceback.print_exc()
                    else:
                        # print("ignore:[%s]" % filename)
                        pass
            print("\n")
            if len(s_list) > 0:
                for i in range(0, len(s_list)):
                    s_size = s_list[i].length()
                    t_size = d_list[i].length()
                    pp = (s_size - t_size) / s_size * 100
                    x = (pp, ((s_size - t_size) / 1024), s_list[i].getName())
                    print("压缩:%.5G%%\t -%.5g Kbs\t [%s]" % x)

            if len(s_list) > 0 and overwrite:
                print("overwriting...")
                for i in range(0, len(s_list)):
                    files = s_list[i]
                    if files.isFile():
                        files.delete()
                    filed = d_list[i]
                    filed.moveTo(args.directory + File.separator + filed.getName())
                print("Done")
                tempDir.delete()
            else:
                tempDir.rename(outputDir.getPath())
                if len(outputDir.listFile()) == 0:
                    outputDir.delete()
                print("Done")
        else:
            print("directory不存在或者不是一个文件夹")
    else:
        print("directory参数缺失")
    if pause:
        print("\n")
        print("-" * 30)
        input("程序执行完毕，按回车结束程序")
