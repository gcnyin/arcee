import unittest
from unittest import TestCase
from arcee.generator.token_generator import TokenGenerator
from test.fixture.ast import ast


class TestTokenGenerator(TestCase):
    def setUp(self):
        self.gen = TokenGenerator(ast)

    def test_gen_token_classes(self):
        expect = '''
from collections import namedtuple

Token = namedtuple('Token', ['type', 'value', 'line', 'column'])
Program = namedtuple('Program', ['expression'])
Expression = namedtuple('Expression', ['nonterminal'])
Constexp = namedtuple('Constexp', ['NUMBER'])
Diffexp = namedtuple('Diffexp', ['expression1', 'expression2'])
Zeroexp = namedtuple('Zeroexp', ['expression'])
Ifexp = namedtuple('Ifexp', ['expression1', 'expression2', 'expression3'])
Varexp = namedtuple('Varexp', ['ID'])
Letexp = namedtuple('Letexp', ['ID', 'expression1', 'expression2'])'''.strip()
        result = self.gen.generate_tokens()
        self.assertEqual(expect, result)


if __name__ == '__main__':
    unittest.main()
