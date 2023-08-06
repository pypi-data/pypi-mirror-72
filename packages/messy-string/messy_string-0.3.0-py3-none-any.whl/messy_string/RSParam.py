RSP_PW_LOW = {
    'string_type': {
        'hex': False,
        'decimal': True,
        'character': True,
        'symbol': False,
        'options': ''
    },
    'option': 'lowercase',
    'length': 8,
    'number': 1
}

RSP_PW_MIDDLE = {
    'string_type': {
        'hex': False,
        'decimal': True,
        'character': True,
        'symbol': False,
        'options': ''
    },
    'option': 'loweruppercase',
    'length': 12,
    'number': 1
}

RSP_PW_HIGH = {
    'string_type': {
        'hex': False,
        'decimal': True,
        'character': True,
        'symbol': False,
        'options': '_'
    },
    'option': 'loweruppercase',
    'length': 16,
    'number': 1
}

RSP_PW_EXCELLENT = {
    'string_type': {
        'hex': False,
        'decimal': True,
        'character': True,
        'symbol': True,
        'options': ''
    },
    'option': 'loweruppercase',
    'length': 16,
    'number': 1
}

RSP_ID = {
    'string_type': {
        'hex': True,
        'decimal': False,
        'character': False,
        'symbol': False,
        'options': ''
    },
    'option': 'lowercase',
    'length': 8,
    'number': 1
}


def get_param(RSP_type: str):
    if RSP_type == 'RSP_PW_LOW':
        return RSP_PW_LOW
    elif RSP_type == 'RSP_PW_MIDDLE':
        return RSP_PW_MIDDLE
    elif RSP_type == 'RSP_PW_HIGH':
        return RSP_PW_HIGH
    elif RSP_type == 'RSP_PW_EXCELLENT':
        return RSP_PW_EXCELLENT
    elif RSP_type == 'RSP_ID':
        return RSP_ID
    else:
        from . import RSError
        raise RSError.ParamFormatError('パラメータ名が存在しません')


def get_param_list():
    return ['RSP_PW_LOW', 'RSP_PW_MIDDLE', 'RSP_PW_HIGH', 'RSP_PW_EXCELLENT', 'RSP_ID']
