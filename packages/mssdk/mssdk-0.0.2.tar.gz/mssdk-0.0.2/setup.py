# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Date: 2020/4/23 13:58
Desc: mssdk 的 pypi 基本信息文件
"""
import re
import ast

import setuptools

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()


def get_version_string():
    """
    get the mssdk version number
    :return: str version number
    """
    with open("mssdk/__init__.py", "rb") as file:
        version_line = re.search(
            r"__version__\s+=\s+(.*)", file.read().decode("utf-8")
        ).group(1)
        return str(ast.literal_eval(version_line))


setuptools.setup(
    name="mssdk",
    version=get_version_string(),
    author="maxsmart",
    author_email="298038875@qq.com",
    license="MIT",
    description="Python SDK for MaxSmart!",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/cdmaxsmart/mssdk",
    packages=setuptools.find_packages(),
    install_requires=[
        "pandas>=0.25.3",
        "requests>=2.22.0",
    ],
    package_data={'': ['*.py', '*.json', "*.pk"]},
    keywords=['finance'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    python_requires='>=3.7',
)
