#!/usr/bin/env python
# coding: utf-8
# author: Frank YCJ
# email: 1320259466@qq.com
import MySQLdb
import json
from ormdb import Config


class MySQL:

    @staticmethod
    def get_conn():
        db_config = json.loads(Config.get_db_config())
        db = MySQLdb.connect(host=db_config[0], port=db_config[1], user=db_config[2], passwd=db_config[3],
                             db=db_config[4], charset='utf8')
        return db

    @staticmethod
    def query_db(sql):
        data = None
        try:
            db = MySQL.get_conn()
            cursor = db.cursor()
            cursor.execute(sql)
            data = cursor.fetchall()
        except Exception,e:
            raise e
        finally:
            db.close()
        return data

    @staticmethod
    def execute_db(sql):
        data = None
        try:
            db = MySQL.get_conn()
            cursor = db.cursor()
            data = cursor.execute(sql)
            db.commit()
        except Exception,e:
            db.rollback()
            raise e
        finally:
            db.close()
        return data
