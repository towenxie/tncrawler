# -*- coding: utf-8 -*-

import sys
import datetime
import logging
import pymysql
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
        _totalSize = len(_resAll)
        print('Res data storing...')
        _stepSize = 1000
        _sql = "insert into resitem(name) values"
        _sqlTemp = ''
        for _index, _value in enumerate(_resAll):
            try:
                _value = pymysql.escape_string(_value);
                if _index % _stepSize == 0 or _index == _totalSize - 1:
                    if _sqlTemp:
                        _conn = self.dbHelper.connectDatabase()
                        print('storing: %d / %d' % (_index + 1, _totalSize))
                        _cur = _conn.cursor();
                        _sqlTemp = _sqlTemp + ",('%s')"  % _value if _index == _totalSize - 1 else _sqlTemp
                        _cur.execute(_sqlTemp)
                        _conn.commit()
                        _cur.close()
                        _conn.close()

                    _sqlTemp = _sql + "('%s')" % _value
                else:
                    _sqlTemp += ",('%s')"  % _value
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
