#!/Users/insightshiga/.pyenv/shims/python
"""
単一責任の法則
* すべてのモジュールとクラスは1つの役割だけ持つ
"""

class UserInfo:
    # 自身を表す機能とファイルの出力を行う機能がごっちゃになっている
    def __init__(self, name, age, phone_number):
        self.name         = name
        self.age          = age
        self.phone_number = phone_number

    def __str__(self):
        return "{}, {}, {}".format(
            self.name, self.age, self.phone_number
        )

    # これが各クラスにあったら変更が合った時大変だよね
    """
    def write_str_to_file(self, filename):
        with open(filename, mode='w') as fh:
            fh.write(str(self))
    """

class Company:

    def __init__(self, name, age, phone_number):
        self.name         = name
        self.age          = age
        self.phone_number = phone_number

    def __str__(self):
        return "{}, {}, {}".format(
            self.name, self.age, self.phone_number
        )
# ファイルの出力を行う機能を切り出した
class FileManager:

    @staticmethod
    def write_str_to_file(obj, filename):
        with open(filename, mode='w') as fh:
            fh.write(str(obj))

user_info = UserInfo('Taro', 21, '000-0000-0000')

print(user_info)
#user_info.write_str_to_file('tmp.txt')
FileManager.write_str_to_file(user_info,'tmp.txt')
# オブジェクトが増えた時に流量できる
company = Company('mufj', 21, '111-1111-1111')
FileManager.write_str_to_file(company,'tmp2.txt')
