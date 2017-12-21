# -*- coding: utf-8 -*-

import sys
import datetime
import logging
from dbhelper import DBHelper

sys.path.append('../utils/')
from fileutil import FileUtil

class RESHelper():
    logger = logging.getLogger('RESHelper')

    def __init__(self):
        self.dbHelper=DBHelper()
        self.resFileName = '../../data/res.txt'  #疾病文件位置

    #保存数据 到DB的resitem表中
    def save_data(self):
        _resAll = FileUtil.readlines(self.resFileName)
        self._clear_data()
        print('Res data storing...')
        for _value in _resAll:
            try:
                if _value:
                    _sql = "insert into resitem(name) value('%s')"
                    _params = (_value,)
                    self.dbHelper.insert(_sql, *_params)
            except Exception as error:
                self.logger.log(logging.ERROR,  error)

    def _clear_data(self):
        params=('resitem',)
        self.dbHelper.clear(*params)

if __name__=='__main__':
    _begin = datetime.datetime.now()
    _zresHelper = RESHelper()
    _zresHelper.save_data()
    _end = datetime.datetime.now()
    _time = _end - _begin
    # self.logger.log(logging.INFO, "Res data stored in db: %s" % _time)\
    print("Res data stored in db: %s" % _time)
