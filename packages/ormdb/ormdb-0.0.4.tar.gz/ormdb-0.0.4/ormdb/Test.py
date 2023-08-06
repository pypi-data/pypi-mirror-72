#!/usr/bin/env python
# coding: utf-8
# author: Frank YCJ
# email: 1320259466@qq.com
from ormdb.DbStyle import DbStyle
from ormdb.LogLevel import LogLevel
from ormdb import Config
# 设置日志级别
Config.set_log_level(LogLevel.All.value)
# 设置连接数据库种类
Config.set_db_style(DbStyle.MySQL.value)
# 设置数据库连接信息
Config.set_db_config(password="ycj5201",database="test_python")
from ormdb.User import User


def saveData():
    # 创建一个实例：
    u = User(id=12,name="Json", email='test_unit@ormdb.org', password='123456')
    # dd=User.add(u)
    # print dd
    # 保存到数据库：
    # u.save()
    # u.search(id=222,name="yyy").ands(name="123",emial="2323@qq.com").ors(password="my").orderby("name").limit().execute()
    # dd=u.search(name="Frank").execute()
    # dd=User().native("select * from user").execute()
    # dd=User().search().like("id","1").execute()
    # print dd
    # User().update(name="Jieke").where(id=12).execute()
    print u.search_all()
saveData()


