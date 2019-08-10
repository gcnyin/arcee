from collections import namedtuple


Token = namedtuple('Token', ['type', 'text'])


class Lexer:
    EOF = 1
    TERMINAL = 2 # actually not used
    NONTERMINAL = 3
    STRING = 4
    KEYWORD = 5 # such as $id
    VERTICALBAR = 6  # |
    COLON = 7  # :
    SEMICOLON = 8  # ;
    token_names = ('n/a', '<EOF>', 'TERMINAL', 'NONTERMINAL',
                   'STRING', 'KEYWORD', 'VERTICALBAR', 'COLON', 'SEMICOLON')

    def __init__(self, source):
        self.input = source
        self.pointer = 0
        self.current = self.input[self.pointer]

    @staticmethod
    def get_token_name(types):
        return ', '.join(tuple(map(lambda x: Lexer.token_names[x], types)))

    def consume(self):
        self.pointer += 1
        if self.pointer >= len(self.input):
            self.current = None
        else:
            self.current = self.input[self.pointer]

    def match(self, x):
        if self.input == x:
            self.consume()
        else:
            raise Exception('excepting ' + str(x) +
                            '; found ' + str(self.current))

    def ws(self):
        while self.current in tuple(' \t\n\r'):
            self.consume()

    def current_is_letter(self):
        return self.current.isalpha()

    def next_token(self):
        while self.current:
            if self.current in tuple(' \t\n\r'):
                self.ws()
            elif self.current == '|':
                self.consume()
                return Token(Lexer.VERTICALBAR, '|')
            elif self.current == ':':
                self.consume()
                return Token(Lexer.COLON, ':')
            elif self.current == ';':
                self.consume()
                return Token(Lexer.SEMICOLON, ';')
            elif self.current == "'":
                return self.string()
            elif self.current_is_letter():
                return self.terminal_or_nonterminal()
            elif self.current == '$':
                return self.keyword()
        return Token(Lexer.EOF, "<EOF>")

    def string(self):
        buffer = ''
        self.consume()
        while True:
            buffer += self.current
            self.consume()
            if self.current == "'":
                self.consume()
                break
        return Token(Lexer.STRING, buffer)

    def terminal_or_nonterminal(self):
        buffer = ''
        while True:
            buffer += self.current
            self.consume()
            if not self.current_is_letter():
                break
        if buffer.isupper():
            return Token(Lexer.TERMINAL, buffer)
        elif buffer.islower():
            return Token(Lexer.NONTERMINAL, buffer)
        raise Exception("invalid name: " + buffer +
                        'is not a terminal or nonterminal')

    def keyword(self):
        buffer = ''
        while True:
            buffer += self.current
            self.consume()
            if self.current == ' ':
                self.consume()
                break
        return Token(Lexer.KEYWORD, buffer)
