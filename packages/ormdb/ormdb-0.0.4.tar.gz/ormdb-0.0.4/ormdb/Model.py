#!/usr/bin/env python
# coding: utf-8
# author: Frank YCJ
# email: 1320259466@qq.com
from ormdb import Config

from ormdb.Log import Log
from ormdb.ModelMetaclass import ModelMetaclass
from ormdb.MySQL import MySQL

L=Log()
class Model(dict):
    __metaclass__ = ModelMetaclass

    def __init__(self, **kw):
        self["sql"]=""
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

        for k, v in self.__mappings__.iteritems():
            if getattr(self, k, None):
                fields.append(v.name)
                params.append("'"+str(getattr(self, k, None))+"'")

        sql = 'insert into %s (%s) values (%s)' % (self.__table__, ','.join(fields), ','.join(params))
        self["sql"]=sql
        L.i('SQL: %s' % self["sql"])
        return self.execute()


    @staticmethod
    def add(obj):
        if isinstance(obj,Model):
            return obj.save()
        else:
            raise AttributeError(r"'%s' does not inherit 'Model'." %type(obj))

    def delete(self,**kw):
        sql = 'delete from %s where '%self.__table__
        tag = True
        for a in kw.keys():
            key = None
            try:
                key = self.__getattribute__(a)
            except:
                key = self.__get_key__(a)

            if tag:
                sql = sql + " %s='%s' " % (key, kw.get(a))
                tag = False
            else:
                sql = sql + " and %s='%s' " % (key, kw.get(a))
        self["sql"] = sql
        L.i('SQL: %s' % self["sql"])
        return self

    @staticmethod
    def delete_by_id(obj):
        if isinstance(obj, Model):
            key=obj.__get_key__('id')
            if key:
                return obj.delete(id=obj.id).execute()
            else:
                raise AttributeError(r"'%s' object has no attribute 'id'." % type(obj))

        else:
            raise AttributeError(r"'%s' does not inherit 'Model'." % type(obj))

    def update(self,**kw):
        sql = 'update %s set ' % self.__table__
        tag = True
        for a in kw.keys():
            key = a
            # try:
            #     key = self.__getattribute__(a)
            # except:
            #     key = self.__get_key__(a)

            if tag:
                sql = sql + " %s='%s', " % (key, kw.get(a))
                tag = False
            else:
                sql = sql + " %s='%s', " % (key, kw.get(a))
        sql=sql[0:-2]
        self["sql"] = sql
        L.i('SQL: %s' % self["sql"])
        return self

    @staticmethod
    def update_by_id(obj):
        if isinstance(obj, Model):
            key = obj.__get_key__('id')
            if key:
                update_cloums={}
                for k, v in obj.__mappings__.iteritems():
                    if getattr(obj, k, None):
                        update_cloums[v.name]=str(getattr(obj, k, None))
                return obj.update(**update_cloums).where(id=obj.id).execute()
            else:
                raise AttributeError(r"'%s' object has no attribute 'id'." % type(obj))

        else:
            raise AttributeError(r"'%s' does not inherit 'Model'." % type(obj))

    def search(self,**kw):
        sql = 'select * from %s where ' % self.__table__
        tag=True
        for a in kw.keys():
            key=None
            try:
                key = self.__getattribute__(a)
            except:
                key=self.__get_key__(a)

            if tag:
                sql=sql+ " %s='%s' "%(key,kw.get(a))
                tag=False
            else:
                sql=sql+ " and %s='%s' "%(key,kw.get(a))
        self["sql"]=sql
        L.i('SQL: %s' % self["sql"])
        return self

    @staticmethod
    def search_all(obj):
        if isinstance(obj, Model):
            sql = 'select * from %s ' % obj.__table__
            obj["sql"] = sql
            L.i('SQL: %s' % obj["sql"])
            return obj.execute()
        else:
            raise AttributeError(r"'%s' does not inherit 'Model'." % type(obj))

    def search_all(self):
        sql = 'select * from %s ' % self.__table__
        self["sql"] = sql
        L.i('SQL: %s' % self["sql"])
        return self.execute()


    def __get_key__(self,name):
        key=None
        for k, v in self.__mappings__.iteritems():
            if k==name:
                key=v.name
                break
        if not key:
            raise AttributeError(r"'Model' object has no attribute '%s'" % name)
        return key

    def ands(self, **k):
        condition=""
        for a in k.keys():
            key = None
            try:
                key = self.__getattribute__(a)
            except:
                key = self.__get_key__(a)
            condition+= " and %s=%s "%(key,k.get(a))
        self["sql"] = self["sql"]+condition
        L.i('SQL: %s' % self["sql"])
        return self

    def ors(self,**k):
        condition = ""
        for a in k.keys():
            key = None
            try:
                key = self.__getattribute__(a)
            except:
                key = self.__get_key__(a)
            condition += " or %s=%s " % (key, k.get(a))
        self["sql"] = self["sql"] + condition
        L.i('SQL: %s' % self["sql"])
        return self

    def orderby(self,k):
        key = None
        try:
            key = self.__getattribute__(k)
        except:
            key = self.__get_key__(k)
        self["sql"] = self["sql"] + (" order by %s"%key)
        L.i('SQL: %s' % self["sql"])
        return self

    def groupby(self,k):
        key = None
        try:
            key = self.__getattribute__(k)
        except:
            key = self.__get_key__(k)
        self["sql"] = self["sql"] + (" group by %s"%key)
        L.i('SQL: %s' % self["sql"])
        return self

    def limit(self,start=0,end=30):
        self["sql"] = self["sql"] + (" limit %s,%s"%(start,end))
        L.i('SQL: %s' % self["sql"])
        return self

    def having(self,condition):
        self["sql"] = self["sql"] + (" having %s"%condition)
        L.i('SQL: %s' % self["sql"])
        return self

    def between(self,name,value1,value2):
        key = None
        try:
            key = self.__getattribute__(name)
        except:
            key = self.__get_key__(name)
        self["sql"] = self["sql"] + (" %s between %s and %s"%(key,value1,value2))
        L.i('SQL: %s' % self["sql"])
        return self

    def notbetween(self,name,value1,value2):
        key = None
        try:
            key = self.__getattribute__(name)
        except:
            key = self.__get_key__(name)
        self["sql"] = self["sql"] + (" %s not between %s and %s"%(key,value1,value2))
        L.i('SQL: %s' % self["sql"])
        return self

    def like_reg(self,name,regexp):
        key = None
        try:
            key = self.__getattribute__(name)
        except:
            key = self.__get_key__(name)
        sql=" %s like '%s'" %(key,regexp)
        self["sql"] = self["sql"] + sql
        L.i('SQL: %s' % self["sql"])
        return self

    def like(self,name,word):
        key = None
        try:
            key = self.__getattribute__(name)
        except:
            key = self.__get_key__(name)
        sql=" %s like '%%%s%%'" %(key,word)
        self["sql"] = self["sql"] + sql
        L.i('SQL: %s' % self["sql"])
        return self

    def where_sql(self,nativesql):
        sql = 'select * from %s where ' % self.__table__
        sql=sql+nativesql
        self["sql"] = self["sql"] + sql
        L.i('SQL: %s' %self["sql"])
        return self

    def where(self,**kw):
        sql=""
        tag = True
        for a in kw.keys():
            key = None
            try:
                key = self.__getattribute__(a)
            except:
                key = self.__get_key__(a)

            if tag:
                sql = sql + " where %s='%s' " % (key, kw.get(a))
                tag = False
            else:
                sql = sql + " and %s='%s' " % (key, kw.get(a))
        self["sql"] =self["sql"] + sql
        L.i('SQL: %s' % self["sql"])
        return self

    def native(self,nativesql):
        self["sql"] = nativesql
        L.i('SQL: %s' % nativesql)
        return self

    def execute(self):
        L.i("Start performing database operations based on sql statements...")
        L.i("Database connection style: %s"%Config.get_db_style())
        L.i('SQL: %s' % self["sql"])
        data=None

        if  isinstance(self["sql"],str):
            if str(self["sql"]).__contains__("select"):
                data=MySQL.query_db(self["sql"])
            else:
                data=MySQL.execute_db(self["sql"])
        else:
            raise ValueError(r"There is a conflict in the function call in %s "%self["sql"])
        L.i("End of execution...")
        return data