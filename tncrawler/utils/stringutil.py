# -*- coding: utf-8 -*-

import difflib

class StringUtil(object):
    @staticmethod
    def str_is_empty(str=None):
        """string is empty return True else return False"""
        return True if str is None or str == '' else False

    @staticmethod
    def str_to_int(str=''):
        """change str to int"""
        return int(str) if not StringUtil.str_is_empty(str) and str.isdigit() else None

    @staticmethod
    def fund_size_format(fund_size=None, index=0):
        """change fund size units(billions to ten thousand)"""
        fund_size = fund_size.split('_') if fund_size is not None else []
        if len(fund_size) == 2 and StringUtil.str_to_int(fund_size[index]) is not None:
            return StringUtil.str_to_int(fund_size[index]) * 10000

    @staticmethod
    def escapes_special_characters(str=None):
        """Escapes special characters"""
        if not StringUtil.str_is_empty(str):
            return str.replace('(', '\\(')\
                .replace(')', '\\)')\
                .replace('.', '\\.')\
                .replace('$', '\\$')\
                .replace('^', '\\^')\
                .replace('[', '\\[')

    @staticmethod
    def sequenceMatcher(text1,text2):
        return difflib.SequenceMatcher(None,text1,text2).ratio()

if __name__ == '__main__':
    text1 = '感冒'
    text2 = '感冒'
    print StringUtil.sequenceMatcher(text1,text2)
