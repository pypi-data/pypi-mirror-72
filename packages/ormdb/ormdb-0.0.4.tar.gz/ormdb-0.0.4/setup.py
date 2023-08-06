#!/usr/bin/env python
# coding: utf-8
# author: Frank YCJ
# email: 1320259466@qq.com

import setuptools

with open("ormdb/README.MD", "r") as fh:
    long_description = fh.read()

# name:描述的是你打包的文件文件名。
# packages是所有要打包的包（package），这里需要打包的是test_package包以及test_package包下的test_package2。
# 所以packages=[‘test_package’,‘test_package.test_package2’]。包与包之间用逗号“ ，”隔开。

setuptools.setup(
    name="ormdb",
    version="0.0.4",
    author="Frank YCJ",
    author_email="1320259466@qq.com",
    description="Make database operation easier!",
    keywords='orm database mysql sqlserver web log',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/YouAreOnlyOne",
    # packages=setuptools.find_packages(),
    packages=["ormdb"],
    install_requires=['mysql>0.0.1'],
    python_requires=">=2.6, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*",
    license="Apache 2.0 license",
    Platform="OS All, Python 2.x",
    project_urls={
        "Bug Tracker": "https://github.com/YouAreOnlyOne/FastFrameJar/issues",
        "Documentation": "https://github.com/YouAreOnlyOne/FastFrameJar",
        "Source Code": "https://github.com/YouAreOnlyOne/FastFrameJar",
    },
    package_data={
        # If any package contains *.txt or *.rst files, include them:
        "ormdb": ["README.MD",],
        "ormdb": ["LICENSE",],
    },
    classifiers=[
        "Programming Language :: Python :: 2",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)


# 执行打包命令
# python setup.py sdist
# python setup.py sdist bdist_wheel
# python setup.py sdist
# python setup.py bdist_egg

# 安装包，cmd 进入dist目录 ， 运行 pip install ormdb-0.0.1.tar.gz

# 卸载安装的包，删除指定的模块或者包, 用如下命令:pip uninstall xxx


# 创建用户账号配置文件，进入 cmd 输入： echo.> .pypirc

# 打包并发布，终端中输入： python setup.py sdist upload -r pypi
# python -m twine upload dist/*
# python -m twine upload --repository-url https://upload.pypi.org/legacy/ dist/*
# python -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*