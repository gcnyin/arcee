from collections import Counter
from string import Template
from arcee.lexer.lexer import Lexer
from arcee.utils.fn import Filter, Map, ToTuple

__all__ = ['TokenGenerator']


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


class TokenGenerator:
    tab = ' ' * 4
    template = Template("$name = namedtuple($name_in_namedtuple, [$components_str])")

    def __init__(self, ast):
        self.ast = ast

    def generate_tokens(self):
        return TokenGenerator.__gen_token_classes(self.ast)

    @staticmethod
    def __gen_token_class(nonterminal):
        name = nonterminal.head.text.capitalize()
        content = nonterminal.content
        if len(content) > 1:
            '''such as :
            expression : zeroexp
            | diffexp
            | ifexp
            | varexp
            | letexp
            ;'''
            components = ('nonterminal',)
        else:
            components = (content[0] |
                          Filter(lambda token: token.type != Lexer.STRING) |
                          Map(lambda token: token.text) |
                          Map(lambda text: text[1:] if text.startswith('$') else text) |
                          ToTuple)
        components = get_order_elements_list(components)
        components_str = ', '.join(
            tuple(map(lambda component_str: "'" + component_str + "'", components)))
        name_in_namedtuple = "'" + name + "'"
        return TokenGenerator.template.substitute(name=name,
                                                  name_in_namedtuple=name_in_namedtuple,
                                                  components_str=components_str)

    @staticmethod
    def __gen_token_classes(ast):
        first_token = '''from collections import namedtuple

Token = namedtuple('Token', ['type', 'value', 'line', 'column'])
'''
        return first_token + '\n'.join(map(TokenGenerator.__gen_token_class, ast))
