from string import Template
from arcee.utils.fn import Map

__all__ = ["LexerGenerator"]

tokenize = Template('''
import re

def tokenize(code):
    keywords = {$keywords}
    token_specification = [
        ('NEWLINE', r'\\n'),
        $tokens
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
            yield Token(kind, value, line_num, column)
''')


class LexerGenerator:

    def __init__(self, source_text):
        self.text = source_text

    def set_source_text(self, source_text):
        self.text = source_text
        a = r'\\'

    def generate_lexer(self):
        return LexerGenerator.generate_lexer_from_text(self.text)

    @staticmethod
    def generate_tokens(tokens_str):
        tokens = (tokens_str.strip().split("\n") |
                  Map(lambda token: token.split(":")) |
                  Map(lambda token: (token[0].strip(), token[1].strip())) |
                  Map(lambda token: ', '.join(("'" + token[0] + "'", LexerGenerator.escape_re(token[1])))) |
                  Map(lambda token: '(' + token + ')'))
        return ',\n        '.join(tokens)

    @staticmethod
    def escape_re(input):
        if input in ('(', ')', '[', ']'):
            return "r'\\" + input + "'"
        return "r'" + input + "'"

    @staticmethod
    def generate_keywords(keywords_str):
        words = (keywords_str.split(":")[1].split(",") |
                 Map(lambda word: word.strip()) |
                 Map(lambda word: '"' + word + '"'))
        return ', '.join(words)

    @staticmethod
    def split_tokens_and_keywords(text):
        text_list = text.strip().split("\n")
        return text_list[0], text.replace(text_list[0], '').strip()

    @staticmethod
    def generate_lexer_from_text(text):
        keywords_str, tokens_str = LexerGenerator.split_tokens_and_keywords(text)
        tokens = LexerGenerator.generate_tokens(tokens_str=tokens_str)
        keywords = LexerGenerator.generate_keywords(keywords_str=keywords_str)
        return tokenize.safe_substitute(keywords=keywords, tokens=tokens)
