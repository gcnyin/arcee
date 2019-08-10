from arcee.lexer.lexer import Token
from arcee.parser.arcee_parser import Nonterminal

parser_syntax = '''program : expression ;
expression : constexp
    | diffexp
    | zeroexp
    | ifexp
    | varexp
    | letexp
    ;
constexp : $NUMBER ;
diffexp : '-' '(' expression ',' expression ')' ;
zeroexp : 'zero?' '(' expression ')' ;
ifexp : 'if' expression 'then' expression 'else' expression ;
varexp : $ID ;
letexp : 'let' $ID '=' expression 'in' expression ;'''

ast = [
    Nonterminal(head=Token(type=3, text='program'), content=[[Token(type=3, text='expression')]]),
    Nonterminal(head=Token(type=3, text='expression'),
                content=[[Token(type=3, text='constexp')], [Token(type=3, text='diffexp')],
                         [Token(type=3, text='zeroexp')], [Token(type=3, text='ifexp')],
                         [Token(type=3, text='varexp')], [Token(type=3, text='letexp')]]),
    Nonterminal(head=Token(type=3, text='constexp'),
                content=[[Token(type=5, text='$NUMBER')]]),
    Nonterminal(head=Token(type=3, text='diffexp'),
                content=[[Token(type=4, text='-'), Token(type=4, text='('), Token(type=3, text='expression'),
                          Token(type=4, text=','), Token(type=3, text='expression'), Token(type=4, text=')')]]),
    Nonterminal(head=Token(type=3, text='zeroexp'),
                content=[[Token(type=4, text='zero?'), Token(type=4, text='('), Token(type=3, text='expression'),
                          Token(type=4, text=')')]]),
    Nonterminal(head=Token(type=3, text='ifexp'),
                content=[[Token(type=4, text='if'), Token(type=3, text='expression'), Token(type=4, text='then'),
                          Token(type=3, text='expression'), Token(type=4, text='else'),
                          Token(type=3, text='expression')]]),
    Nonterminal(head=Token(type=3, text='varexp'),
                content=[[Token(type=5, text='$ID')]]),
    Nonterminal(head=Token(type=3, text='letexp'),
                content=[[Token(type=4, text='let'), Token(type=5, text='$ID'), Token(type=4, text='='),
                          Token(type=3, text='expression'), Token(type=4, text='in'),
                          Token(type=3, text='expression')]])
]

keywords = ['$ID', '$NUMBER']
tokens_name = ['program', 'expression', 'constexp', 'diffexp', 'zeroexp', 'ifexp', 'varexp', 'letexp']
lexer_re = {'$ID': r'[a-zA-Z]+', '$NUMBER': r'\d+(\.\d*)'}
nonterminals_where_content_has_many_tokens = (
    Nonterminal(head=Token(type=3, text='expression'),
                content=[[Token(type=3, text='constexp')], [Token(type=3, text='diffexp')],
                         [Token(type=3, text='zeroexp')], [Token(type=3, text='ifexp')],
                         [Token(type=3, text='varexp')], [Token(type=3, text='letexp')]]),
)


a = (
    [[Token(type=3, text='expression')]],
    [[Token(type=5, text='$NUMBER')]],
    [[Token(type=4, text='-'), Token(type=4, text='('), Token(type=3, text='expression'), Token(type=4, text=','), Token(type=3, text='expression'), Token(type=4, text=')')]],
    [[Token(type=4, text='zero?'), Token(type=4, text='('), Token(type=3, text='expression'), Token(type=4, text=')')]],
    [[Token(type=4, text='if'), Token(type=3, text='expression'), Token(type=4, text='then'), Token(type=3, text='expression'), Token(type=4, text='else'), Token(type=3, text='expression')]],
    [[Token(type=5, text='$ID')]],
    [[Token(type=4, text='let'), Token(type=5, text='$ID'), Token(type=4, text='='), Token(type=3, text='expression'), Token(type=4, text='in'), Token(type=3, text='expression')]]
)
