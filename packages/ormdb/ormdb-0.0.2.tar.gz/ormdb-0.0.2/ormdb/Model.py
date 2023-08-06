#!/usr/bin/env python
# coding: utf-8
# author: Frank YCJ
# email: 1320259466@qq.com
from ormdb.Log import Log
from ormdb.ModelMetaclass import ModelMetaclass

L=Log()
class Model(dict):
    __metaclass__ = ModelMetaclass

    def __init__(self, **kw):
        super(Model, self).__init__(**kw)

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(r"'Model' object has no attribute '%s'" % key)

    def __setattr__(self, key, value):
        self[key] = value

    def save(self):
        fields = []
        params = []
        args = []
        for k, v in self.__mappings__.iteritems():
            fields.append(v.name)
            params.append('?')
            args.append(getattr(self, k, None))
        sql = 'insert into %s (%s) values (%s)' % (self.__table__, ','.join(fields), ','.join(params))
        L.i('SQL: %s' % sql)
        L.i('ARGS: %s' % str(args))


    def delete(self):
        fields = []
        params = []
        args = []
        for k, v in self.__mappings__.iteritems():
            fields.append(v.name)
            params.append('?')
            args.append(getattr(self, k, None))
        sql = 'insert into %s (%s) values (%s)' % (self.__table__, ','.join(fields), ','.join(params))
        L.i('SQL: %s' % sql)
        L.i('ARGS: %s' % str(args))

    def update(self):
        fields = []
        params = []
        args = []
        for k, v in self.__mappings__.iteritems():
            fields.append(v.name)
            params.append('?')
            args.append(getattr(self, k, None))
        sql = 'insert into %s (%s) values (%s)' % (self.__table__, ','.join(fields), ','.join(params))
        L.i('SQL: %s' % sql)
        L.i('ARGS: %s' % str(args))

    def search(self,**kw):

        sql = 'select * from %s where ' % self.__table__
        tag=True
        for a in kw.keys():
            if tag:
                sql=sql+ " %s=%s "%(a,kw.get(a))
                tag=False
            else:
                sql=sql+ " and %s=%s "%(a,kw.get(a))

        L.i('SQL: %s' % sql)
        self["sql"]=sql
        return self

    def ands(self, **k):
        condition=""
        for a in k.keys():
            condition+= " or %s=%s "%(a,k.get(a))
        self["sql"] = self["sql"]+condition
        L.i('SQL: %s' % self["sql"])

    def ors(self):
        pass

    def orderby(self):
        pass

    def groupby(self):
        pass

    def limit(self):
        pass

    def having(self):
        pass

    def between(self):
        pass

    def like(self):
        pass
