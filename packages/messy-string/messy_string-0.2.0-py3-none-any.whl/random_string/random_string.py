# coding: utf-8
'''
-hex : 11234567890abcde

-decimal: 1234567890
-character: qwertyuiopasdfghjklzxcvbnm
-symbol: !"#$%&'()

-length: 10
'''

import random
from . import RSError

BASE_FORMAT = {
    'string_type': {
        'hex': bool,
        'decimal': bool,
        'character': bool,
        'symbol': bool,
        'options': str
    },
    'option': str,
    'length': int,
    'number': int
}


def base_string(param: dict):
    HEX_lowercase = "1234567890abcdef"
    DECIMAL = "1234567890"
    CHARACTER_lowercase = "abcdefghijklmnopqrstuvwxyz"
    SYMBOL = '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'
    strings = ''

    st_type = param['string_type']
    st_opt = param['option']

    if st_type['hex'] is True:
        strings += HEX_lowercase
    if st_type['character'] is True:
        strings += CHARACTER_lowercase

    if st_opt == 'lowercase':
        pass
    elif st_opt == 'uppercase':
        strings = strings.upper()
    elif st_opt == 'loweruppercase':
        strings = ''.join(list(set(list(strings + strings.upper()))))

    if st_type['symbol'] is True:
        strings += SYMBOL
    if st_type['decimal'] is True:
        strings += DECIMAL

    if st_type['options'] != '':
        strings += st_type['options']

    return strings


def param_format_check(param: dict, base_param):
    if set(param.keys()) != set(base_param.keys()):
        raise RSError.ParamFormatError

    for key, value in base_param.items():
        if type(value) is dict:
            param_format_check(param=param[key], base_param=base_param[key])
        elif isinstance(param[key], value) is False:
            raise RSError.ParamFormatError


def param_val_check(param: dict):
    st_type = param['string_type']
    st_opt = param['option']

    if st_type['hex'] is True and (st_type['decimal'] is True or st_type['character'] is True or
                                   st_type['symbol'] is True):
        raise RSError.ParamValError('hexとその他のオプションは共用できません')
    elif st_type['hex'] is True:
        pass
    elif st_type['decimal'] is True or st_type['character'] is True or st_type['symbol'] is True:
        pass
    else:
        raise RSError.ParamValError('hexもしくはその他のオプションの中から最低1つ選択してください')

    if st_opt in ['lowercase', 'uppercase', 'loweruppercase']:
        pass
    else:
        raise RSError.ParamValError("'lowercase', 'uppercase', 'loweruppercase'の中から1つ選択してください")

    if 1 <= param['length'] and isinstance(param['length'], int):
        pass
    else:
        raise RSError.ParamValError("文字列の長さが正しくありません")
    if 1 <= param['number'] and isinstance(param['number'], int):
        pass
    else:
        raise RSError.ParamValError("生成数の値が正しくありません")


def random_string(parameter: dict):
    param_format_check(param=parameter, base_param=BASE_FORMAT)
    param_val_check(param=parameter)
    strings = base_string(param=parameter)
    number = parameter['number']
    length = parameter['length']
    ret_str_list = []

    for i in range(0, number):
        temp_string = ""
        for i in range(0, length):
            temp_string += strings[random.randint(0, len(strings) - 1)]
        ret_str_list.append(temp_string)

    return ret_str_list
