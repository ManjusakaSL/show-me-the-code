#coding=utf-8
import re, sys
from util import *
from handlers import *
from rules import *

class Parser(object):
    '''
    读取文本文件，应用规则并且控制处理程序
    '''
    def __init__(self, handler):
        self.handler = handler
        self.rules = []
        self.filters = []

    def addRule(self, rule):
        self.rules.append(rule)

    def addFilter(self, pattern, name):
        def Filter(block, handler):
            return re.sub(pattern,  self.handler.sub(name), block)
        self.filters.append(Filter)

    def parse(self, File):
        self.handler.start('document')
        for block in blocks(File):
            for Filter in self.filters:
                block = Filter(block, self.handler)
            for rule in self.rules:
                if rule.condition(block):
                    if rule.action(block, self.handler): break;
        self.handler.end('document')

class BasicParser(Parser):
    '''
    在构造函数中添加规则和过滤器
    '''
    def __init__(self, handler):
        super(BasicParser, self).__init__(handler)
        self.addRule(ListRule())
        self.addRule(ListitemRule())
        self.addRule(TitleRule())
        self.addRule(HeadingRule())
        self.addRule(ParagraphRule())
        self.addFilter(r'\*(.+?)\*', 'emphasis')
        self.addFilter(r'(http://[\.a-zA-Z/]+)', 'url')
        self.addFilter(r'([\.a-zA-Z]+@[\.a-zA-Z]+)', 'mail')

handler = HandlerHTML()
parser = BasicParser(handler)
parser.parse(sys.stdin)
