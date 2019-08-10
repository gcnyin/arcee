import unittest
from unittest import TestCase
from arcee.generator.lexer_generator import LexerGenerator


class TestGenerateLexer(TestCase):
    syntax = '''
KEYWORDS: let, in
NUMBER  : \d+(\.\d*)?
ASSIGN  : =
ID      : [A-Za-z]+
SKIP    : [ \\t]+'''

    def setUp(self):
        self.gen = LexerGenerator(TestGenerateLexer.syntax)

    def test_generate_keywords(self):
        self.assertEqual(self.gen.generate_keywords("KEYWORDS: let, in"), '"let", "in"')

    def test_generate_tokens(self):
        self.assertEqual(self.gen.generate_tokens('''
        NUMBER  : \d+(\.\d*)?
        ASSIGN  : =
        RIGHT_BRACKET : (
        LETF_BRACKET : )
        ID      : [A-Za-z]+
        SKIP    : [ \\t]+''').strip(),
                         '''
        ('NUMBER', r'\d+(\.\d*)?'),
        ('ASSIGN', r'='),
        ('RIGHT_BRACKET', r'\('),
        ('LETF_BRACKET', r'\)'),
        ('ID', r'[A-Za-z]+'),
        ('SKIP', r'[ \\t]+')'''.strip())

    def test_split_tokens_and_keywords(self):
        keywords, tokens = self.gen.split_tokens_and_keywords(TestGenerateLexer.syntax)
        self.assertEqual(keywords, "KEYWORDS: let, in")
        self.assertEqual(tokens, '''NUMBER  : \d+(\.\d*)?
ASSIGN  : =
ID      : [A-Za-z]+
SKIP    : [ \\t]+''')

    def test_generate_lexer(self):
        result = '''
import re

def tokenize(code):
    keywords = {"let", "in"}
    token_specification = [
        ('NEWLINE', r'\\n'),
        ('NUMBER', r'\d+(\.\d*)?'),
        ('ASSIGN', r'='),
        ('ID', r'[A-Za-z]+'),
        ('SKIP', r'[ \\t]+')
    ]
    tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)
    line_num = 1
    line_start = 0
    for mo in re.finditer(tok_regex, code):
        kind = mo.lastgroup
        value = mo.group(kind)
        if kind == 'NEWLINE':
            line_start = mo.end()
            line_num += 1
        elif kind == 'SKIP':
            pass
        else:
            if value in keywords:
                kind = value.upper()
            column = mo.start() - line_start
            yield Token(kind, value, line_num, column)'''.strip()
        generated_lexer = self.gen.generate_lexer_from_text(TestGenerateLexer.syntax).strip()
        self.assertEqual(result, generated_lexer)


if __name__ == '__main__':
    unittest.main()
