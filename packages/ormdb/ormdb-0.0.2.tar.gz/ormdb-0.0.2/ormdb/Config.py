#!/usr/bin/env python
# coding: utf-8
# author: Frank YCJ
# email: 1320259466@qq.com
import os

_log_level="all"

def _init():
    global _log_level
    _log_level="all"
    os.environ.setdefault("LOG_LEVEL", _log_level)


def set_log_level(level):
    _log_level = level
    os.environ.setdefault("LOG_LEVEL",_log_level)

def get_log_level():

    try:
        _log_level=os.environ["LOG_LEVEL"]
    except BaseException:
        _log_level="all"

    return _log_level
