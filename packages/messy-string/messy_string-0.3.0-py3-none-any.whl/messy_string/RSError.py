class ParamFormatError(Exception):
    """パラメーターのフォーマットが違うことを知らせる例外クラス"""

    def __init__(self, detail=''):
        self.detail = detail

    def __str__(self):
        return 'パラメーターのフォーマットが違います({})'.format(self.detail)


class ParamValError(Exception):
    """パラメーターの値が違うことを知らせる例外クラス"""

    def __init__(self, detail=''):
        self.detail = detail

    def __str__(self):
        return 'パラメーターの値が不正です({})'.format(self.detail)
