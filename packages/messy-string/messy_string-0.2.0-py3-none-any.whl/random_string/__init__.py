from .random_string import random_string
from . import RSParam
from . import RSError
import argparse


def main():
    parser = argparse.ArgumentParser(description='ランダムな文字列を生成するプログラム')
    parser.add_argument('--hex', help='16進数(default)', action='store_true')

    parser.add_argument('-d', '--decimal', help='数値を使用する', action='store_true')
    parser.add_argument('-c', '--character', help='文字列を使用する', action='store_true')
    parser.add_argument('-s', '--symbol', help='記号を使用する', action='store_true')
    parser.add_argument('-o', '--options', help='任意の文字列')

    parser.add_argument('-lo', '--lowercase', help='小文字にする(default)', action='store_true')
    parser.add_argument('-up', '--uppercase', help='大文字にする', action='store_true')
    parser.add_argument('-lu', '--loweruppercase', help='大文字と小文字を両方使う', action='store_true')

    parser.add_argument('-l', '--length', help='長さ', type=int, default=16)
    parser.add_argument('-n', '--number', help='出力する個数', type=int, default=1)

    parser.add_argument('-P', '--parameter', help='パラメータを指定', type=str)
    parser.add_argument('-Pl', '--parameter_list', help='利用できるパラメータの種類', action='store_true')
    args = parser.parse_args()

    parameter = {
        'string_type': {
            'hex': False,
            'decimal': False,
            'character': False,
            'symbol': False,
            'options': ''
        },
        'option': 'lowercase',
        'length': 16,
        'number': 1
    }

    if args.parameter is not None:
        parameter = RSParam.get_param(args.parameter)
    if args.parameter_list is True:
        for param in RSParam.get_param_list():
            print("パラメータ名: {}".format(param))
            print("\t{}".format(RSParam.get_param(param)))
        return

    if args.hex is True:
        parameter['string_type']['hex'] = True
    if args.decimal is True:
        parameter['string_type']['decimal'] = True
    if args.character is True:
        parameter['string_type']['character'] = True
    if args.symbol is True:
        parameter['string_type']['symbol'] = True
    if args.hex is False and args.decimal is False and args.character is False and args.symbol is False and args.parameter is None:
        parameter['string_type']['hex'] = True
    if args.options is not None:
        parameter['string_type']['options'] = args.options

    if args.lowercase is True:
        parameter['option'] = 'lowercase'
    elif args.uppercase is True:
        parameter['option'] = 'uppercase'
    elif args.loweruppercase is True:
        parameter['option'] = 'loweruppercase'

    if 1 <= args.length and isinstance(args.length, int):
        parameter['length'] = args.length
    if 1 <= args.number and isinstance(args.number, int):
        parameter['number'] = args.number

    strs = random_string(parameter)
    for s in strs:
        print(s)


if __name__ == '__main__':
    main()
