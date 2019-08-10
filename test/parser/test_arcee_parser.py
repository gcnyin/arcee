import os
from unittest import TestCase

from arcee.parser.arcee_parser import Parser
from test.fixture.ast import ast, parser_syntax


class TestParser(TestCase):
    def setUp(self):
        self.parser = Parser(parser_syntax)

    def test_result(self):
        self.assertEqual(ast, self.parser.start())
