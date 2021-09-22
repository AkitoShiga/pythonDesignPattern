#!/Users/insightshiga/.pyenv/shims/python
"""
開放閉鎖の法則
拡張に対しては開いており、修正に対しては閉じていなければならない
  * 振る舞いを変更する時に元のソースをいじらないようにする
  * 機能追加に強くなる
  * 機能追加した時は、その部分だけテストすれば良くなる（デグレの試験など不要）
"""

from abc import ABCMeta, abstractmethod

class UserInfo:

    def __init__(self, user_name, job_name, nationality):
        self.user_name   = user_name
        self.job_name    = job_name
        self.nationality = nationality

    def __str__(self):
        return '{}, {}, {}'.format(
            self.user_name, self.job_name, self.nationality
        )

class Comparation(metaclass=ABCMeta):

    @abstractmethod
    def is_equal(self, other):
        pass

    def __and__(self, other):
        return AndComparation(self, other)

    def __or__(self, other):
        return OrComparation(self, other)


class AndComparation(Comparation):

    def __init__(self, *args):
        self.comparations = args

    def is_equal(self, other):
        return all(
            map(
                lambda comparation: comparation.is_equal(other),
                self.comparations
            )
        )


class OrComparation(Comparation):

    def __init__(self, *args):
        self.comparations = args

    def is_equal(self, other):
        return any(
            map(
                lambda comparation: comparation.is_equal(other),
                self.comparations
            )
        )


class JobNameComparation(Comparation):

    def __init__(self, job_name):
        self.job_name = job_name

    def is_equal(self, other):
        return self.job_name == other.job_name


class NationalityComparation(Comparation):

    def __init__(self, nationality):
        self.nationality = nationality

    def is_equal(self, other):
        return self.nationality == other.nationality



class Filter(metaclass=ABCMeta):

    @abstractmethod
    def filter(self, comparation, item):
        pass

class UserInfoFilter(Filter):

    def filter(self, comparation, items):
        for item in items:
            if comparation.is_equal(item):
                yield item

"""
class UserInfoFilter:
    現在の実装では機能を追加する時に元のメソッドをいじらなければならず
    良くない

    @staticmethod
    def filter_users_job(users, job_name):
        for user in users:
            if user.job_name == job_name:
                yield user

    @staticmethod
    def filter_users_nationality(users, nationality):
        for user in users:
            if user.nationality == nationality:
                yield user
"""
    # 機能の変更がひつようとなった場合、新しいメソッドを作らなければならない

taro = UserInfo('taro', 'salary man', 'Japan');
jiro = UserInfo('jiro', 'police man', 'Japan');
john = UserInfo('john', 'salary man', 'USA');

user_list = [taro, jiro, john]

salary_man_comparation = JobNameComparation('salary man')
japan_comparation = NationalityComparation('Japan')
user_info_filter = UserInfoFilter()


for user in user_info_filter.filter(salary_man_comparation, user_list):
    print(user)
for user in user_info_filter.filter(japan_comparation, user_list):
    print(user)


print('-'*100)
salary_man_and_japan = salary_man_comparation & japan_comparation
for user in user_info_filter.filter(salary_man_and_japan, user_list):
    print(user)

print('-'*100)
salary_man_or_japan = salary_man_comparation | japan_comparation
for user in user_info_filter.filter(salary_man_or_japan, user_list):
    print(user)
"""
for man in UserInfoFilter.filter_users_nationality(user_list, 'Japan'):
    print(man)
"""

