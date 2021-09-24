#! /Users/insightshiga/.pyenv/shims/python

"""
インターフェース分離の原則
インターフェースに抽象メソッドを定義しすぎて、実装が無駄な実装をしないようにする
沢山実装しそうだったらスーパークラスを一個つくってそのサブクラスにしちゃう
"""

from abc import ABCMeta, abstractmethod
# だめな例
class Athlete(metaclass=ABCMeta):

    @abstractmethod
    def swim(self):
        pass

    # 不要
    @abstractmethod
    def high_jump(self):
        pass

    # 不要
    @abstractmethod
    def long_jump(self):
        pass


class Athlete1(Athlete):

    def swim(self):
        print('swim')

# 無駄な継承をしなければいけない！
    def high_jump(self):
        pass

# 無駄な継承をしなければいけない！
    def long_jump(self):
        pass


a1 = Athlete1()
a1.swim()

# 良い例
class AthleteN(metaclass=ABCMeta):
    pass

class SwimAthlete(AthleteN):

    @abstractmethod
    def swim(self):
        pass

class JumpAthlete(AthleteN):

    @abstractmethod
    def high_jump(self):
        pass

    @abstractmethod
    def long_jump(self):
        pass

class Athlete2(SwimAthlete):

    def swim(self):
        print('swim')

class Athlete3(SwimAthlete, JumpAthlete):

    def swim(self):
        print('swim')

    def high_jump(self):
        print('jump')

    def long_jump(self):
        print('long jump')

a2 = Athlete2()
a2.swim()

a3 = Athlete3()
a3.high_jump()
a3.long_jump()
