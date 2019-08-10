from unittest import TestCase

from arcee.generator.parser_generator import get_order_elements_list, ParserGenerator
from test.fixture.ast import ast, tokens_name, keywords, nonterminals_where_content_has_many_tokens


class TestParserGenerator(TestCase):
    def setUp(self):
        self.gen = ParserGenerator(ast)

    def test_get_order_elements_list(self):
        self.assertEqual(
            ['expression1', 'id1', 'var', 'expression2', 'id2'],
            get_order_elements_list(['expression', 'id', 'var', 'expression', 'id'])
        )

    def test_generate_fixture(self):
        expect = '''
class Parser:
    def __init__(self, token_list):
        self.tokens = token_list
        self.pointer = 0
        self.lookahead = None
        self.result = None
        self.consume()

    def consume(self):
        if self.pointer < len(self.tokens):
            self.lookahead = self.tokens[self.pointer]
            self.pointer += 1

    def match(self, x):
        if self.lookahead.type == x:
            current = self.lookahead
            self.consume()
            return current
        raise Exception("not match " + str(x))

    def match_str(self, expect_str):
        if self.lookahead.value == expect_str:
            result = self.lookahead
            self.consume()
            return result
        else:
            raise Exception('expect: ' + expect_str + ', actual:' + self.lookahead.value)

    def start(self):
        if not self.result:
            result = self.parse_program()
            self.result = result
        return self.result'''.strip()
        self.assertEqual(expect, self.gen.generate_fixture())

    def test_get_tokens_name(self):
        self.assertEqual(tokens_name, self.gen.get_tokens_name(ast))

    def test_gen_parse_methods(self):
        expect = '''    def parse_program(self):
        result = []
        result.append(self.parse_expression())
        return Program(*result)

    def parse_expression(self):
        result = []
        if self.lookahead.type == 'NUMBER':
            result.append(self.parse_constexp())
        elif self.lookahead.type == '-':
            result.append(self.parse_diffexp())
        elif self.lookahead.type == 'ZERO?':
            result.append(self.parse_zeroexp())
        elif self.lookahead.type == 'IF':
            result.append(self.parse_ifexp())
        elif self.lookahead.type == 'ID':
            result.append(self.parse_varexp())
        elif self.lookahead.type == 'LET':
            result.append(self.parse_letexp())
        return Expression(*result)

    def parse_constexp(self):
        result = []
        result.append(self.match('NUMBER'))
        return Constexp(*result)

    def parse_diffexp(self):
        result = []
        self.match_str('-')
        self.match_str('(')
        result.append(self.parse_expression())
        self.match_str(',')
        result.append(self.parse_expression())
        self.match_str(')')
        return Diffexp(*result)

    def parse_zeroexp(self):
        result = []
        self.match_str('zero?')
        self.match_str('(')
        result.append(self.parse_expression())
        self.match_str(')')
        return Zeroexp(*result)

    def parse_ifexp(self):
        result = []
        self.match_str('if')
        result.append(self.parse_expression())
        self.match_str('then')
        result.append(self.parse_expression())
        self.match_str('else')
        result.append(self.parse_expression())
        return Ifexp(*result)

    def parse_varexp(self):
        result = []
        result.append(self.match('ID'))
        return Varexp(*result)

    def parse_letexp(self):
        result = []
        self.match_str('let')
        result.append(self.match('ID'))
        self.match_str('=')
        result.append(self.parse_expression())
        self.match_str('in')
        result.append(self.parse_expression())
        return Letexp(*result)'''
        self.assertEqual(expect, self.gen.gen_parse_methods())

    def test_multiple_nonterminals_tokens(self):
        self.assertEqual(
            nonterminals_where_content_has_many_tokens,
            self.gen.multiple_nonterminals_tokens
        )
