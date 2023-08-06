# GOSS Python SDK

## 目录

- [介绍](#介绍)
- [安装指南](#安装指南)
- [使用方法](#使用方法)

## 介绍

* 机智云OSS Python SDK, 目前可以支持Python2.7以及Python3.x

## 安装指南

* 使用pip安装
```sh
$ pip install -U goss-sdk-python
```

* 手动安装
```sh
$ python setup.py install
```

## 使用方法

* 以下为使用腾讯云例子

```python
from goss import GossClient, GOSS_TENCENT_COS

# 初始化客户点
client = GossClient(
    ctype=GOSS_TENCENT_COS,
    secret_id='xxxxxxxxxxxx',
    secret_key='xxxxxxxxxxxx',
    region='xxxxxx',
    bucket='xxxxxx',
)

# 文件上传结果
uri, err = client.upload_file(local_path='/xxx/xxx/xxx.xx', cloud_path='xxx/xxx')
# uri 为文件下载链接
# err 为上传结果，如果成功则为None，否则为错误原因
```
