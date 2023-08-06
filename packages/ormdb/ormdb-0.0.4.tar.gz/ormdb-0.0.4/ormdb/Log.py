#!/usr/bin/env python
# coding: utf-8
# author: Frank YCJ
# email: 1320259466@qq.com
from ormdb import Config


class Log:


    def d(self, msg):
        if Config.get_Config.get_log_level()() == "all" or Config.get_log_level() == "d":
            print msg

    def e(self, msg):
        if Config.get_log_level() == "all" or Config.get_log_level() == "e":
            print msg

    def f(self, msg):
        if Config.get_log_level() == "all" or Config.get_log_level() == "f":
            print msg

    def i(self, msg):
        if Config.get_log_level() == "all" or Config.get_log_level() == "i":
            print msg

    def w(self, msg):
        if Config.get_log_level() == "all" or Config.get_log_level() == "w":
            print msg
