# -*- coding: utf-8 -*-

import codecs
import datetime

class FileUtil(object):

    @staticmethod
    def readlines(fileName):
        _file = codecs.open(fileName, 'r', 'utf-8')
        _results=list()
        for value in _file.readlines():
            try:
                val = value.strip().replace('"','').replace('[','').replace(']','')
                _results.append(val)
            except Exception as error:
                FileUtil.logger.log(logging.ERROR,  error)
        _file.close()
        return _results

    @staticmethod
    def save_file(item):
        _file = codecs.open('zz.txt', 'ab', 'utf-8')
        line = item + "\n"
        _file.write(line)
        _file.close()

    @staticmethod
    def save_new_file(item, _newfileName):
        _file = codecs.open(_newfileName, 'ab', 'utf-8')
        line = item + "\n"
        _file.write(line)
        _file.close()
