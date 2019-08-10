from arcee.generator.lexer_generator import LexerGenerator
from arcee.generator.parser_generator import ParserGenerator
from arcee.generator.token_generator import TokenGenerator
from arcee.parser.arcee_parser import Parser


def main():
    lexer_syntax = '''
KEYWORDS: let, in, if, then, else, zero, =, -, (, )
NUMBER  : \d+(\.\d*)?
ASSIGN  : =
SUBTRACTION : -
RIGHT_BRACKET : (
COLON: ,
LETF_BRACKET : )
ID      : [A-Za-z]+
SKIP    : [ \\t]+'''
    parser_syntax = '''
program : expression ;
expression : zeroexp
    | diffexp
    | ifexp
    | varexp
    | letexp
    | constexp
    ;
constexp : $NUMBER ;
diffexp : '-' '(' expression ',' expression ')' ;
zeroexp : 'zero' '(' expression ')' ;
ifexp : 'if' expression 'then' expression 'else' expression ;
varexp : $ID ;
letexp : 'let' $ID '=' expression 'in' expression ;'''
    parser = Parser(parser_syntax)
    ast = parser.start()
    token_gen = TokenGenerator(ast)
    lexer_gen = LexerGenerator(lexer_syntax)
    parser_gen = ParserGenerator(ast)
    print(token_gen.generate_tokens())
    print(lexer_gen.generate_lexer())
    print(parser_gen.generate_parser())


if __name__ == '__main__':
    main()
