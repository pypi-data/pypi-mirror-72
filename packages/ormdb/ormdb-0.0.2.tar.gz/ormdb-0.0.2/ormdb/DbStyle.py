#!/usr/bin/env python
# coding: utf-8
# author: Frank YCJ
# email: 1320259466@qq.com
from enum import unique, Enum


@unique
class DbStyle(Enum):
    Oracle=""
    MySQL=""
    MariaDB=""
    SQLServer=""
    Access=""
    Memcached=""
    Redis=""
    BerkeleyDB=""
    MongoDB=""
    Cassandra=""
    HBase=""
