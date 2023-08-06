#!/usr/bin/env python
# coding: utf-8
# author: Frank YCJ
# email: 1320259466@qq.com
from enum import unique, Enum


@unique
class DbStyle(Enum):
    Oracle="Oracle"
    MySQL="MySQL"
    MariaDB="MariaDB"
    SQLServer="SQLServer"
    Access="Access"
    Memcached="Memcached"
    Redis="Redis"
    BerkeleyDB="BerkeleyDB"
    MongoDB="MongoDB"
    Cassandra="Cassandra"
    HBase="HBase"
