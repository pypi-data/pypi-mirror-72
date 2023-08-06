#!/usr/bin/env python
# coding: utf-8
# author: Frank YCJ
# email: 1320259466@qq.com
from ormdb.Field import Field
from ormdb.Log import Log
from ormdb.MySQL import MySQL

L = Log()

class ModelMetaclass(type):

    def __new__(cls, name, bases, attrs):
        if name == 'Model':
            return type.__new__(cls, name, bases, attrs)
        mappings = dict()
        sql = "CREATE TABLE %s (\n%s)"
        cloums=""
        for k, v in attrs.iteritems():
            if isinstance(v, Field):
                cloums=cloums+v.name+" "+v.column_type+",\n"
                L.i('Found mapping: %s==>%s' % (k, v))
                mappings[k] = v
        for k in mappings.iterkeys():
            attrs.pop(k)
        attrs['__table__'] = name  # 假设表名和类名一致
        attrs['__mappings__'] = mappings  # 保存属性和列的映射关系
        cloums=cloums[0:-2]
        sql=sql%(name,cloums)
        L.i("Create table: "+sql)
        try:
            MySQL.execute_db(sql)
        except Exception,e:
            if str(e).__contains__("Table 'user' already exists"):
                L.i("Table '%s' already exists"%name)
            else:
                raise e
        return type.__new__(cls, name, bases, attrs)
