#!/usr/bin/env python
# coding: utf-8
# author: Frank YCJ
# email: 1320259466@qq.com

class Field(object):

    def __init__(self, name, column_type):
        self.name = name
        self.column_type = column_type

    def __str__(self):
        return '<%s:%s>' % (self.__class__.__name__, self.name)


class IntegerField(Field):

    def __init__(self, name):
        super(IntegerField, self).__init__(name, 'bigint')


class StringField(Field):

    def __init__(self, name):
        super(StringField, self).__init__(name, 'varchar(1000)')


class BoolField(Field):

    def __init__(self, name):
        super(BoolField, self).__init__(name, 'bool')


class DateField(Field):

    def __init__(self, name):
        super(DateField, self).__init__(name, 'date')


class TimeField(Field):

    def __init__(self, name):
        super(TimeField, self).__init__(name, 'time')


class DateTimeField(Field):

    def __init__(self, name):
        super(DateTimeField, self).__init__(name, 'datetime')


class DoubleField(Field):

    def __init__(self, name):
        super(DoubleField, self).__init__(name, 'double')


class FloatField(Field):

    def __init__(self, name):
        super(FloatField, self).__init__(name, 'float')


class DecimalField(Field):

    def __init__(self, name):
        super(DecimalField, self).__init__(name, 'decimal')
