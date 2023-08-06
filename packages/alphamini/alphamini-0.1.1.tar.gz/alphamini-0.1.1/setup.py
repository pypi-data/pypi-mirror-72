#!/usr/bin/env python
# coding=utf-8

import setuptools

with open("README.md", "r") as f:
    long_desc = f.read()

with open("LICENSE", "r") as f:
    license_txt = f.read()

setuptools.setup(
    name="alphamini",
    version="0.1.1",
    author='logic.peng',
    author_email='logic.peng@ubtrobot.com',
    description="python sdk for ubtech alpha mini robot",
    long_description=long_desc,
    long_description_content_type="text/markdown",
    license="GPLv3",
    python_requires='>=3.6',
    # url="",
    packages=setuptools.find_packages(exclude=["*.test", "*.test.*", "test.*", "test*", "test"]),  # 排除掉测试包
    # packages=['mini'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        'console_scripts': [
            'setup_py_pkg = mini.tool.pkg_tool:setup_py_pkg',
            'install_py_pkg = mini.tool.pkg_tool:install_py_pkg',
            'uninstall_py_pkg = mini.tool.pkg_tool:uninstall_py_pkg',
            'run_py_pkg = mini.tool.pkg_tool:run_py_pkg',

            'query_py_pkg = mini.tool.pkg_tool:show_py_pkg',
            'list_py_pkg = mini.tool.pkg_tool:list_py_pkg2',
        ],
    },
    install_requires=[
        'websockets',
        'ifaddr',
        'protobuf'
    ],
    zip_safe=False
)
