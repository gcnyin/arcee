from collections import Counter
from string import Template

from arcee.lexer.lexer import Lexer
from arcee.utils.fn import Map, Filter, FlatMap, ToSet, ToTuple

__all__ = ['ParserGenerator', 'get_order_elements_list']


def get_order_elements_list(names):
    name_dict = Counter(names)
    count_dict = dict()
    count_dict.setdefault(0)
    result = []
    for name in names:
        if names.count(name) == 1:
            result.append(name)
            continue
        count = count_dict.setdefault(name, 1)
        if count - name_dict[name] == 1:
            continue
        count_dict[name] += 1
        result.append(name + str(count))
    return result


parser_fixture = '''
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


class ParserGenerator:
    tab = ' ' * 4
    def_method_template = Template('''    def parse_$name(self):
        $content''')
    call_method_template = Template('$name')
    content_template = Template('''result = []
        $procedure
        return $class_name(*result)''')

    def __init__(self, ast):
        self.ast = ast
        self.keywords = self.get_keyworks()
        self.tokens_name = ParserGenerator.get_tokens_name(ast)
        self.multiple_nonterminals_tokens = tuple(filter(lambda nonterminal: len(nonterminal.content) > 1, self.ast))

    def get_keyworks(self):
        return (self.ast |
                Map(lambda nonterminal: nonterminal.content) |
                Filter(lambda content: len(content) == 1) |
                Map(lambda tokens: tokens[0]) |
                FlatMap(lambda x: x) |
                Filter(lambda token: token.type == Lexer.KEYWORD) |
                Map(lambda token: token.text) |
                ToSet)

    def generate_parser(self):
        return ParserGenerator.generate_fixture() + '\n\n' + self.gen_parse_methods()

    @staticmethod
    def generate_fixture():
        return parser_fixture

    def generate_method_name(self, name):
        if name in self.tokens_name:
            return "result.append(self.parse_" + name + '())'
        elif name in self.keywords:
            if name.startswith('$'):
                name = name[1:]
            return "result.append(self.match('" + name + "'))"
        return "self.match_str('" + name + "')"

    def generate_multiple_choices_term(self, name):
        target_nonterminal = (self.ast | Filter(lambda nonterminal: nonterminal.head.text == name) | ToTuple)[0]
        first = target_nonterminal.content[0][0].text
        if first.startswith('$'):
            first = first[1:]
        return "self.lookahead.type == '" + first.upper() + "':\n" + self.tab * 3 + \
               "result.append(self.parse_" + name + "())"

    def generate_parse_procudure(self, token_name):
        content = tuple(filter(lambda nonterminal: nonterminal.head.text == token_name, self.ast))[0].content
        choice = [[token.text for token in i] for i in content]
        if len(choice) == 1:
            result = [ParserGenerator.call_method_template.substitute(name=self.generate_method_name(i)) for i in
                      choice[0]]
            return '\n        '.join(result)
        result = [''.join([self.generate_multiple_choices_term(j) for j in i]) for i in choice]
        return 'if ' + '\n        elif '.join(result)

    @staticmethod
    def get_tokens_name(ast):
        result = [i.head.text for i in ast]
        return result

    def gen_parse_methods(self):
        methods = map(
            lambda token_name: ParserGenerator.def_method_template.substitute(
                name=token_name,
                content=ParserGenerator.content_template.substitute(
                    class_name=token_name.capitalize(),
                    procedure=self.generate_parse_procudure(token_name)
                )
            ),
            self.tokens_name
        )
        return '\n\n'.join(methods)
