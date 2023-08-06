#!/usr/bin/env python
# coding: utf-8
# author: Frank YCJ
# email: 1320259466@qq.com
from enum import unique, Enum


@unique
class LogLevel(Enum):
    Debugger="d"
    Error="e"
    Fatal="f"
    Info="i"
    Warn="w"
    All="all"
    No="no"
