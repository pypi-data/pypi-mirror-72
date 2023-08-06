# python3.7
# encoding: utf-8
"""
@author: Chenjin.Qian
@email:  chenjin.qian@xquant.com
@file:   setup.py
@time:   2020-06-30 11:05
"""

from setuptools import setup, find_packages

import holiday_calendar

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="holiday-calendar",
    version=holiday_calendar.__version__,
    description="The holidays in China",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license = 'MIT License',
    author="Jingxuan",
    author_email="qian_chen_jin@163.com",
    url="https://github.com/Thchoonlophon/holiday_calendar",
    packages=find_packages(),
    include_package_data = True,
    install_requires=["pandas", "requests"],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
)
