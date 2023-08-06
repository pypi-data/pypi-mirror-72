# python3.7
# encoding: utf-8
"""
@author: Chenjin.Qian
@email:  chenjin.qian@xquant.com
@file:   setup.py
@time:   2020-07-01 8:42
"""

from setuptools import setup, find_packages
import oracle_connection


def read(f):
    return open(f, encoding="utf-8").read()


setup(
    name="oracle-connection",
    version=oracle_connection.__version__,
    description='A new way to operate oracle',
    long_description=read('README.rst'),
    license='MIT License',
    author="Jingxuan",
    author_email="qian_chen_jin@163.com",
    url="https://github.com/Thchoonlophon/oracle-connection",
    packages=find_packages(),
    include_package_data=True,
    install_requires=["pandas", "cx_Oracle"],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
)
