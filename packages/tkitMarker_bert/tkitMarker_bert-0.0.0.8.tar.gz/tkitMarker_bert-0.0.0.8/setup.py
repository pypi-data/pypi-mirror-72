# -*- coding: utf-8 -*-
from setuptools import find_packages, setup
from os import path as os_path
import time
this_directory = os_path.abspath(os_path.dirname(__file__))

# 读取文件内容
def read_file(filename):
    with open(os_path.join(this_directory, filename), encoding='utf-8') as f:
        long_description = f.read()
    return long_description

# 获取依赖
def read_requirements(filename):
    return [line.strip() for line in read_file(filename).splitlines()
            if not line.startswith('#')]
long_description="""

这里是说明

使用bert微调提取实体，描述这些信息。
==0.0.0.07
过滤掉中文标点
解决bert中出现 [UNK]问题
==v0.0.0.04
加入关键词清理 ## 问题

"""
setup(
    name='tkitMarker_bert',
    version='0.0.0.08',
    description='Terry toolkit',
    author='Terry Chan',
    author_email='napoler2008@gmail.com',
    url='https://github.com/napoler/tkitMarker_bert',
    # install_requires=read_requirements('requirements.txt'),  # 指定需要安装的依赖
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[
        'tkitFile==0.0.1.2',
        'tkitText==0.0.1.58',
        'tqdm==4.45.0',
        'transformers==2.8.0'
    ],
    packages=['tkitMarker_bert'])

"""
pip freeze > requirements.txt

python3 setup.py sdist
#python3 setup.py install
python3 setup.py sdist upload
"""