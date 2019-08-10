from collections import namedtuple

from arcee.lexer.lexer import Lexer

__all__ = ['Parser', 'Nonterminal']

Nonterminal = namedtuple('Nonterminal', ['head', 'content'])


class Parser:
    """
    terms : nonterminal+
    nonterminal : NONTERMINAL ':' content ('|'  content)* ';'
    content : (NONTERMINAL | keyword)+
    keyword: $id
    """
    def __init__(self, text):
        self.input = Lexer(text)
        self.lookahead = None
        self.result = None
        self.consume()

    def consume(self):
        self.lookahead = self.input.next_token()

    def match(self, *match_types):
        if self.lookahead.type in match_types:
            current = self.lookahead
            self.consume()
            return current
        raise Exception("expect " +
                        self.input.get_token_name(match_types) +
                        ", but found <" +
                        self.input.get_token_name((self.lookahead.type,)) +
                        ': ' +
                        self.lookahead.text +
                        '>')

    def start(self):
        result = self.terms()
        if not self.result:
            self.result = result
        return result

    def terms(self):
        terms = [self.nonterminal()]
        while True:
            if self.lookahead.type == Lexer.EOF:
                break
            terms.append(self.nonterminal())
        return terms

    def nonterminal(self):
        head = self.match(Lexer.NONTERMINAL)
        self.match(Lexer.COLON)
        contents = [self.content()]
        while True:
            if self.lookahead.type == Lexer.VERTICALBAR:
                self.match(Lexer.VERTICALBAR)
                contents.append(self.content())
            elif self.lookahead.type == Lexer.SEMICOLON:
                break
        self.match(Lexer.SEMICOLON)
        return Nonterminal(head, contents)

    def content(self):
        content = [self.match(Lexer.NONTERMINAL, Lexer.KEYWORD, Lexer.STRING)]
        while True:
            if self.lookahead.type in (Lexer.NONTERMINAL, Lexer.KEYWORD, Lexer.STRING):
                content.append(self.lookahead)
                self.consume()
            else:
                break
        return content

    def __str__(self):
        return str(self.result)
