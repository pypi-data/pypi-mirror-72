#!/usr/bin/env python
# coding: utf-8
# author: Frank YCJ
# email: 1320259466@qq.com

from ormdb.LogLevel import LogLevel
from ormdb import Config
# 设置日志级别
Config.set_log_level(LogLevel.All.value)
from ormdb.User import User


def saveData():
    # 创建一个实例：
    u = User(id=12345, name='Michael', email='test_unit@ormdb.org', password='my-pwd')
    # 保存到数据库：
    # u.save()
    u.search(id=222).ands(name="123",emial="2323@qq.com")

saveData()