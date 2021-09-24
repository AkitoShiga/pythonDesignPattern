"""
依存性逆転の法則
クライアントはなるべく抽象によったクラスを使用する
サブクラスじゃなくてスーパークラスつかおうね
"""

# 悪い例
class Book:
    def __init__(self, content):
        self.content = content


class Formatter:

    def format(self, book:Book):
        return book.content# 実装クラスを使用している

class Printer:

    def print(self, book:Book):
        formatter = Formatter() # 実装クラスを使用している
        formatted_book = formatter.format(book)
        print(formatted_book)

book = Book('My Book')
printer = Printer()
printer.print(book)


# 良い例
from abc import ABCMeta, abstractmethod, abstractproperty

class IBook(metaclass=ABCMeta):

    @abstractproperty
    def content(self):
        pass

class BookN(IBook):

    def __init__(self, content):
        self.content = content

    @property
    def content(self):
        return self.content

class IFormatter(metaclass=ABCMeta):

    @abstractmethod
    def format(self, i_book: IBook):
        pass

class HtmlFormatter(IFormatter):

    def format(self, IBook):
        return '<h1>' + IBook.content + '</h1>'

class XmlFormatter(IFormatter):

    def format(self, IBook):
        return '<xml>' + IBook.content + '</xml>'

class Printer:
    def __init__(self, i_formatter: IFormatter):
        self.i_formatter = i_formatter

    def print(self, i_book:IBook):
        formatted_book = self.i_formatter.format(i_book)

book = Book('My Book')
html_formatter = HtmlFormatter()
html_printer = Printer(html_formatter)
html_printer.print(book)
xml_formatter = XmlFormatter()
xml_printer = Printer(xml_formatter)
xml_printer.print(book)
