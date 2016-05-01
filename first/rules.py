#coding=utf-8
class Rule(object):
    def action(self, block, handler):
        handler.start(self.tp)
        handler.feed(block)
        handler.end(self.tp)
        return True

class HeadingRule(Rule):
    '''
    只有一行，最多七十个字符，不已冒号结尾
    '''
    tp = 'heading'
    def condition(self, block):
        return '\n' not in block and len(block) <= 70 and not block.endswith(':')

class TitleRule(HeadingRule):
    '''
    第一行，且必须是heading
    '''
    tp = 'title'
    isFirst = True
    def condition(self, block):
        if not self.isFirst: return False
        self.isFirst = False
        return super(TitleRule, self).condition(block)

class ListitemRule(Rule):
    '''
    以-开始的段落，-需要被删除
    '''
    tp = 'listitem'
    def condition(self, block):
        return block[0] == '-'
    def action(self, block, handler):
        handler.start(self.tp)
        handler.feed(block[1:].strip()) # -之后可能有空白
        handler.end(self.tp)
        return True

class ListRule(ListitemRule):
    '''
    开始于不是listitem的块和随后的listitem的块之间，结束于listitem的块和随后的不是listitem的块之间
    '''
    tp = 'list'
    isListitem = False
    def condition(self, block):
        return True
    def action(self, block, handler):
        if not self.isListitem and super(ListRule, self).condition(block):
            handler.start(self.tp)
            self.isListitem = True
        elif self.isListitem and not super(ListRule, self).condition(block):
            handler.end(self.tp)
            self.isListitem = False
        return False

class ParagraphRule(Rule):
    '''
    所有不符合其它规则的block都是paragraph
    '''
    tp = 'paragraph'
    def condition(self, blcok):
        return True
