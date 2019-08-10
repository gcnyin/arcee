# Arcee

It is a Python parser generator, use EBNF-like syntax.

## Install

```bash
$ pip install Arcee
```

## Example

It's really readable. 

grammar:

```
KEYWORDS        : let, if, zero, -
NUMBER          : \d+(\.\d*)?
ASSIGN          : =
SUBTRACTION     : -
RIGHT_BRACKET   : (
COLON           : ,
LETF_BRACKET    : )
ID              : [A-Za-z]+
SKIP            : [ \\t]+

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
letexp : 'let' $ID '=' expression 'in' expression ;
```

```
$ arcee grammar > result.py
```

`result.py` has three parts:

### Token

```python
from collections import namedtuple

Token = namedtuple('Token', ['type', 'value', 'line', 'column'])
Program = namedtuple('Program', ['expression'])
# ...
```

### Lexer

```python
import re

def tokenize(code):
    pass # ...
```

### Parser

```python
class Parser:
    def __init__(self, token_list):
        pass
    
    # ... 
        
    def parse_expression(self):
        if xxx:
            self.parse_constexp()
        elif yyy:
            self.parse_diffexp()
        #...

    def parse_constexp(self):
        pass
        
    def parse_diffexp(self):
        pass

    def parse_zeroexp(self):
        pass

    def parse_ifexp(self):
        pass

    def parse_varexp(self):
        pass

    def parse_letexp(self):
        pass
```

You can parse input such as:

```python
input = '''let a = 0 in if zero(a) then -(a, 1) else -(a, 2)'''

tokens = list(tokenize(input))

parser = Parser(tokens)

parser.parse_program()
```

result is:

```python
result = Program(
    expression=Expression(
        nonterminal=Letexp(
            ID=Token(type='ID', value='a', line=2, column=4),
            expression1=Expression(
                nonterminal=Constexp(
                    NUMBER=Token(type='NUMBER', value='0', line=2, column=8))),
            expression2=Expression(
                nonterminal=Ifexp(
                    expression1=Expression(
                        nonterminal=Zeroexp(
                            expression=Expression(
                                nonterminal=Varexp(
                                    ID=Token(type='ID', value='a', line=2, column=21))))),
                    expression2=Expression(
                        nonterminal=Diffexp(
                            expression1=Expression(
                                nonterminal=Varexp(
                                    ID=Token(type='ID', value='a', line=2, column=31))),
                            expression2=Expression(
                                nonterminal=Constexp(
                                    NUMBER=Token(type='NUMBER', value='1', line=2,
                                                 column=34))))),
                    expression3=Expression(
                        nonterminal=Diffexp(
                            expression1=Expression(
                                nonterminal=Varexp(
                                    ID=Token(type='ID', value='a', line=2, column=44))),
                            expression2=Expression(
                                nonterminal=Constexp(
                                    NUMBER=Token(type='NUMBER', value='2', line=2,
                                                 column=47))))))))))
```

Now, you can use this ast to do what you like.

You can also use api in your Python file.

```python
from arcee import generate

grammar = '''KEYWORDS        : let, if, zero, -
NUMBER          : \d+(\.\d*)?
ASSIGN          : =
SUBTRACTION     : -
RIGHT_BRACKET   : (
COLON           : ,
LETF_BRACKET    : )
ID              : [A-Za-z]+
SKIP            : [ \\t]+

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

print(generate(grammar))
```