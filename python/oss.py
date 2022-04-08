# -*- coding: utf-8 -*
'''
Author: Cao Shixin
Date: 2019-11-28 15:18:26
LastEditors: Cao Shixin
LastEditTime: 2022-04-07 20:02:52
Description: 
'''
import oss2
import os


class OSSOperate(object):
    def __init__(self, key_id: str, key_secret: str, end_point: str):
        # 对象初始化操作
        self.access_key_id = os.getenv('OSS_TEST_ACCESS_KEY_ID', key_id)
        self.access_key_secret = os.getenv('OSS_TEST_ACCESS_KEY_SECRET',
                                           key_secret)
        self.endpoint = os.getenv('OSS_TEST_ENDPOINT', end_point)

    def showBucket(self):
        print("**********   获取bucket信息  *******")
        service = oss2.Service(
            oss2.Auth(self.access_key_id, self.access_key_secret),
            self.endpoint)
        print("*****************************")
        print("     现有bucket有:      ")
        print('\n'.join(info.name for info in oss2.BucketIterator(service)))
        print("*****************************")

    def createBucket(self):
        print("**********   创建  *******")
        bucket_input = input("请输入想创建的bucket名:   ")
        # 创建Bucket对象，所有Object相关的接口都可以通过Bucket对象来进行
        bucket = oss2.Bucket(oss2.Auth(self.access_key_id,
                                       self.access_key_secret),
                             self.endpoint,
                             bucket_name=bucket_input)

        # 带权限与存储类型创建bucket
        bucket.create_bucket(permission=oss2.BUCKET_ACL_PRIVATE,
                             input=oss2.models.BucketCreateConfig(
                                 oss2.BUCKET_STORAGE_CLASS_STANDARD))
        if oss2.Bucket(oss2.Auth(self.access_key_id, self.access_key_secret),
                       self.endpoint,
                       bucket_name=bucket_input):
            print("     成功创建%s" % bucket_input)
            self.showBucket()
        print("***************************")

    def bucketInfo(self):
        print("**********   获取bucket_info  *******")
        bucket_input = input('请输入bucket名:   ')
        # 获取bucket相关信息
        bucket = oss2.Bucket(oss2.Auth(self.access_key_id,
                                       self.access_key_secret),
                             self.endpoint,
                             bucket_name=bucket_input)
        bucket_info = bucket.get_bucket_info()
        print("     bucket_info:")
        print(' name: ' + bucket_info.name)
        print(' storage class: ' + bucket_info.storage_class)
        print(' creation date: ' + bucket_info.creation_date)
        print("*******************************")
        print("     bucket_stat:")
        bucket_stat = bucket.get_bucket_stat()
        print(' storage: ' + str(bucket_stat.storage_size_in_bytes))
        print(' object count: ' + str(bucket_stat.object_count))
        print(' multi part upload count: ' +
              str(bucket_stat.multi_part_upload_count))
        print("********************************")

    def upload(self, path_direct):
        print("**********   上传  *******")
        bucket_input = input('请输入要传入的bucket名:   ')
        print("**************************")
        print("    上传目录下所有文件：")
        dirs = os.listdir(path_direct)
        for file in dirs:
            print(file)
        print("***************************")

        filename = input('请输入要上传的文件名： ')
        cloud_name = input('请输入云端文件名：   ')
        bucket = oss2.Bucket(oss2.Auth(self.access_key_id,
                                       self.access_key_secret),
                             self.endpoint,
                             bucket_name=bucket_input)
        with open(oss2.to_unicode(filename), 'rb') as f:
            bucket.put_object(cloud_name, f)
        meta = bucket.get_object_meta(cloud_name)
        if meta:
            print("     上传成功")
            print("     云端所有文件：")
            for i in oss2.ObjectIterator(bucket):
                print(i.key)
        else:
            print("     上传失败")

    def download(self, save_dir_path):
        print("**********   下载  *******")
        bucket_input = input('请输入bucket名:')
        bucket = oss2.Bucket(oss2.Auth(self.access_key_id,
                                       self.access_key_secret),
                             self.endpoint,
                             bucket_name=bucket_input)
        print("     %s下有如下文件:" % bucket_input)
        for i in oss2.ObjectIterator(bucket):
            print(i.key)
        print("***************************")
        cloud_name = input('请输入要下载的文件名：')
        file_name = input('请输入保存至本地文件名：')
        bucket.get_object_to_file(cloud_name, file_name)
        print(file_name[4:])
        if file_name[4:] in os.listdir(save_dir_path):
            print("     成功下载%s" % cloud_name)
        print("**************************")
        print("     当前目录下所有文件：")
        for file in os.listdir(save_dir_path):
            print(file)
        print("***************************")

    def remove(self):
        print("**********   删除  *******")
        bucket_input = input('请输入bucket名:')
        bucket = oss2.Bucket(oss2.Auth(self.access_key_id,
                                       self.access_key_secret),
                             self.endpoint,
                             bucket_name=bucket_input)
        print("     %s下有如下文件(删除前):" % bucket_input)
        for i in oss2.ObjectIterator(bucket):
            print(i.key)
        print("***************************")
        file_name = input('请输入要删除的文件名：')

        # 删除名为motto.txt的Object
        bucket.delete_object(file_name)
        print("     成功删除%s" % file_name)
        print("     %s下有如下文件(删除后):" % bucket_input)
        for i in oss2.ObjectIterator(bucket):
            print(i.key)


if __name__ == '__main__':
    print("************************")
    print("     「指令数字」：")
    print("0. 获取bucket信息")
    print("1. 查看具体bucket信息")
    print("2. 创建bucket")
    print("3. 上传文件")
    print("4. 下载文件")
    print("5. 删除文件")
    print("6. 退出")
    print("************************")
    ossOperate = OSSOperate()
    while 1:
        num = int(input('请输入指令数：'))
        if num == 0:
            ossOperate.showBucket()
        elif num == 1:
            ossOperate.bucketInfo()
        elif num == 2:
            ossOperate.createBucket()
        elif num == 3:
            ossOperate.upload()
        elif num == 4:
            ossOperate.download()
        elif num == 5:
            ossOperate.remove()
        else:
            break
