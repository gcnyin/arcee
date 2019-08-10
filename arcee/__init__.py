import sys
from arcee.generator.lexer_generator import LexerGenerator
from arcee.generator.parser_generator import ParserGenerator
from arcee.generator.token_generator import TokenGenerator
from arcee.parser.arcee_parser import Parser


def generate(input):
    lexer_syntax, parser_syntax = input.split('\n\n')
    parser = Parser(parser_syntax)
    ast = parser.start()
    token_gen = TokenGenerator(ast)
    lexer_gen = LexerGenerator(lexer_syntax)
    parser_gen = ParserGenerator(ast)
    return token_gen.generate_tokens() + lexer_gen.generate_lexer() + parser_gen.generate_parser()


def arcee():
    file_name = sys.argv[1]
    with open(file_name) as file:
        print(generate(file.read()))
