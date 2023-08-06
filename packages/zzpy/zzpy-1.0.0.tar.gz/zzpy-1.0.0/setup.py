#!/usr/bin/env python
# -*- coding:utf-8 -*-

#############################################
# File Name: setup.py
# Author: LiangjunFeng
# Mail: zhumavip@163.com
# Created Time:  2018-4-16 19:17:34
#############################################

from setuptools import setup, find_packages  # 这个包没有的可以pip一下

setup(
    name="zzpy",  # 这里是pip项目发布的名称
    version="1.0.0",  # 版本号，数值大的会优先被pip
    keywords=["pip", "zzpy", "util"],
    description="Python3 utilities",
    long_description="Python3 utilities",
    license="MIT Licence",

    url="https://github.com/zerocpp/zzpy",  # 项目相关文件地址，一般是github
    author="zerocpp",
    author_email="85642468@qq.com",

    packages=find_packages(),
    include_package_data=True,
    platforms="any",
    install_requires=["pymongo", "pymysql", "redis"]  # 这个项目需要的第三方库
)
