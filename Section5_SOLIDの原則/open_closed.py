#!/Users/insightshiga/.pyenv/shims/python
"""
開放閉鎖の法則
拡張に対しては開いており、修正に対しては閉じていなければならない
  * 振る舞いを変更する時に元のソースをいじらないようにする
  * 機能追加に強くなる
  * 機能追加した時は、その部分だけテストすれば良くなる（デグレの試験など不要）
"""

class UserInfo:

    def __init__(self, user_name: str, job_name: str, nationality: str):
        self.user_name   = user_name
        self.job_name    = job_name
        self.nationality = nationality

    def __str__(self):
        return '{}, {}, {}'.format(
                    self.user_name, self.job_name, self.nationality
                )


# ダメな例
"""
* ダメな点
* 新しいメソッドを加える時にUserInfoFilterをいじらなければいけない
* UserInfoFilterに条件を判断する機能が組み込まれている
"""
class UserInfoFilter:

    @staticmethod
    def filter_users_job(users: list[UserInfo], job_name: str) -> UserInfo:
        for user in users:
            if user.job_name == job_name:
                yield user

    @staticmethod
    def filter_users_nationality(users: list[UserInfo], nationality: str) -> UserInfo:
        for user in users:
            if user.nationality == nationality:
                yield user


# client
taro = UserInfo('taro', 'salary man', 'Japan')
jiro = UserInfo('jiro', 'police man', 'Japan')
john = UserInfo('john', 'salary man', 'USA')
user_list = [taro, jiro, john]

for man in UserInfoFilter.filter_users_job(user_list, 'police man'):
    print(man)

for man in UserInfoFilter.filter_users_nationality(user_list, 'Japan'):
    print(man)


# 良い例
# 抽象クラスを使える用にする
from abc import ABCMeta, abstractmethod

# UserInfoFilterの機能を分割する
# UserInfoFilterをの条件を判断する機能を抽象クラスとして定義する
class Comparation(metaclass=ABCMeta):

    @abstractmethod
    def is_equal(self, other: UserInfo) -> bool:
        pass

    def __and__(self, other):
        return AndComparation(self, other)

    def __or__(self, other):
        return OrComparation(self, other)

class JobNameComparation(Comparation):

    def __init__(self, job_name: str):
        self.job_name = job_name

    def is_equal(self, other: UserInfo) -> bool:
        return  self.job_name == other.job_name


class NationalityComparation(Comparation):

    def __init__(self, nationality: str):
        self.nationality = nationality

    def is_equal(self, other: UserInfo) -> bool:
        return self.nationality == other.nationality


class AndComparation(Comparation):

    def __init__(self, *args: Comparation):
        self.comparations = args

    def is_equal(self, other: list[UserInfo]) -> UserInfo:
        return all(
            map(
                lambda comparation: comparation.is_equal(other),
                self.comparations
            )
        )

class OrComparation(Comparation):

    def __init__(self, *args: Comparation):
        self.comparations = args

    def is_equal(self, other: list[UserInfo]) -> UserInfo:
        return any(
            map(
                # フィールドのis_equalが実行される
                lambda comparation: comparation.is_equal(other),
                self.comparations
            )
        )
# UserInfoFilterをの条件にあったuserを返す機能を抽象クラスとして定義する
class Filter(metaclass=ABCMeta):

    # ここしれっと多態性になってる
    @abstractmethod
    def filter(self, comparation: Comparation, items: list[UserInfo]) -> UserInfo:
        pass


class UserInfoFilter2(Filter):

    def filter(self, comparation: Comparation, items: list[UserInfo]) -> UserInfo:
        for item in items:
            if comparation.is_equal(item): #ここの処理を移譲することで汎用的になる
                yield item


# client
taro = UserInfo('taro', 'salary man', 'Japan')
jiro = UserInfo('jiro', 'police man', 'Japan')
john = UserInfo('john', 'salary man', 'USA')
user_list = [taro, jiro, john]

salary_man_comparation = JobNameComparation('salary man')
user_info_filter = UserInfoFilter2()
for user in user_info_filter.filter(salary_man_comparation, user_list):
    print(user)

japan_comparation = NationalityComparation('Japan')
for user in user_info_filter.filter(japan_comparation, user_list):
    print(user)

# Comparationを&で挟むとオーバーライドされたandが実行される
# つまり、ここで宣言された変数はAndComparationオブジェクトが返される
salary_man_and_japan = salary_man_comparation & japan_comparation
for user in user_info_filter.filter(salary_man_and_japan, user_list):
    print(user)
salary_man_or_japan = salary_man_comparation | japan_comparation
for user in user_info_filter.filter(salary_man_or_japan, user_list):
    print(user)
