# -*- coding:utf-8 -*-
import os
from setuptools import setup

# 第三方依赖
requires = [
    # "pandas>=0.23.4"
    "pycurl",
    "redis",
    "kafka",
    "logging"
]

setup(
    name="hs_package",  # 包名称
    version="0.0.6",  # 包版本
    description="",  # 包详细描述
    long_description="",   # 长描述，通常是readme，打包到PiPy需要
    author="hongs",  # 作者名称
    author_email="li_shengyou@163.com",  # 作者邮箱
    url="",   # 项目官网
    packages=["hs_httpController","hs_logController"],    # 项目需要的包
    install_requires=requires,  # 第三方库依赖
    zip_safe=False  # 此项需要，否则卸载时报windows error
)