#!/usr/bin/env python
# coding: utf-8
# author: Frank YCJ
# email: 1320259466@qq.com
import os
import json

_log_level="all"
_db_style="MySQL"
_db_config=""

def _init():
    global _log_level
    _log_level="all"
    os.environ.setdefault("LOG_LEVEL", _log_level)
    _db_style = "MySQL"
    os.environ.setdefault("DB_STYLE", _db_style)
    _db_config = ""
    os.environ.setdefault("DB_CONFIG", _db_style)


def set_log_level(level):
    _log_level = level
    os.environ.setdefault("LOG_LEVEL",_log_level)

def get_log_level():
    try:
        _log_level=os.environ["LOG_LEVEL"]
    except BaseException:
        _log_level="all"
    return _log_level



def set_db_style(dbstyle):
    _db_style = dbstyle
    os.environ.setdefault("DB_STYLE",_db_style)

def get_db_style():
    try:
        _db_style=os.environ["DB_STYLE"]
    except BaseException:
        _db_style="MySQL"
    return _db_style


def set_db_config(host="localhost",port=3306,username="root",password="ycj5201",database="test_python"):
    db_config=[host,port,username,password,database]
    _db_config = json.dumps(db_config)
    os.environ.setdefault("DB_CONFIG",_db_config)

def get_db_config():
    try:
        _db_config=os.environ["DB_CONFIG"]
    except BaseException,e:
        raise e
    return _db_config