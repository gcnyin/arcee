import unittest
from unittest import TestCase

from arcee.lexer.lexer import Lexer, Token


class TestLexer(TestCase):
    def setUp(self):
        source = '''
        program : expression ;
        expression : zeroexp
            | diffexp
            | ifexp
            | varexp
            | letexp
            ;
        diffexp : '-' '(' expression ',' expression ')' ;
        zeroexp : 'zero?' '(' expression ')' ;
        ifexp : 'if' expression 'then' expression 'else' expression ;
        varexp : $id ;
        letexp : 'let' $id '=' expression 'in' expression ;
        '''
        self.lexer = Lexer(source)

    def testResult(self):
        result = []
        t = self.lexer.next_token()
        while t.type != Lexer.EOF:
            result.append(t)
            t = self.lexer.next_token()
        result.append(t)
        self.assertEqual(
            [
                Token(type=3, text='program'),
                Token(type=7, text=':'),
                Token(type=3, text='expression'),
                Token(type=8, text=';'),
                Token(type=3, text='expression'),
                Token(type=7, text=':'),
                Token(type=3, text='zeroexp'),
                Token(type=6, text='|'),
                Token(type=3, text='diffexp'),
                Token(type=6, text='|'),
                Token(type=3, text='ifexp'),
                Token(type=6, text='|'),
                Token(type=3, text='varexp'),
                Token(type=6, text='|'),
                Token(type=3, text='letexp'),
                Token(type=8, text=';'),
                Token(type=3, text='diffexp'),
                Token(type=7, text=':'),
                Token(type=4, text='-'),
                Token(type=4, text='('),
                Token(type=3, text='expression'),
                Token(type=4, text=','),
                Token(type=3, text='expression'),
                Token(type=4, text=')'),
                Token(type=8, text=';'),
                Token(type=3, text='zeroexp'),
                Token(type=7, text=':'),
                Token(type=4, text='zero?'),
                Token(type=4, text='('),
                Token(type=3, text='expression'),
                Token(type=4, text=')'),
                Token(type=8, text=';'),
                Token(type=3, text='ifexp'),
                Token(type=7, text=':'),
                Token(type=4, text='if'),
                Token(type=3, text='expression'),
                Token(type=4, text='then'),
                Token(type=3, text='expression'),
                Token(type=4, text='else'),
                Token(type=3, text='expression'),
                Token(type=8, text=';'),
                Token(type=3, text='varexp'),
                Token(type=7, text=':'),
                Token(type=5, text='$id'),
                Token(type=8, text=';'),
                Token(type=3, text='letexp'),
                Token(type=7, text=':'),
                Token(type=4, text='let'),
                Token(type=5, text='$id'),
                Token(type=4, text='='),
                Token(type=3, text='expression'),
                Token(type=4, text='in'),
                Token(type=3, text='expression'),
                Token(type=8, text=';'),
                Token(type=1, text='<EOF>')
            ],
            result
        )


if __name__ == '__main__':
    unittest.main()
