import logging
from pyleri import (
    Grammar,
    Token,
    Regex,
    Sequence,
    Ref,
    Choice,
    Repeat,
    )


logger = logging.getLogger()

class PSGrammar(Grammar):
    LIST = Ref()
    OBJ = Ref()
    STRING = Regex(r"'(?:.)*?'")
    INT = Regex("\d+")
    BOOL = Choice(Token("$False"), Token("$True"))
    ni_item = Choice(OBJ, LIST, STRING, BOOL, INT)
    variable = Sequence(Regex('\w+'), Token('='), ni_item)
    LIST = Sequence('@(', Repeat(ni_item), ')')
    OBJ = Sequence('@{', Repeat(variable), '}')
    START = Choice(OBJ, LIST)

class Parser:
    def __init__(self):
        self.parser = PSGrammar()

    def parse_node(self, node):
        logger.debug(node.element)
        if isinstance(node.element, Repeat):
            logger.debug('repeat x%s', len(node.children))
            return [self.parse_node(c) for c in node.children]
        elif isinstance(node.element, Choice) and getattr(node.element, 'name') != 'BOOL':
            assert len(node.children) == 1
            return self.parse_node(node.children[0])

        if not hasattr(node.element, 'name'):
            logger.debug('%s!!', node.element)
            return
        if node.element.name in 'OBJ':
            elements = self.parse_node(node.children[1])  # 0 and 2 are @{ }
            _dict = {}
            for k, v in elements:
                _dict[k] = v
            return _dict
        elif node.element.name == 'variable':
            name_node, equals, value_node = node.children
            var_value = self.parse_node(value_node)
            var_name = name_node.string
            logger.debug(f'Variable {var_name} == {var_value}')
            return var_name, var_value
        elif node.element.name == 'INT':
            return int(node.string)
        elif node.element.name == 'STRING':
            return node.string.strip("'")
        elif node.element.name == 'BOOL':
            return node.string == '$True'
        elif node.element.name == 'LIST':
            # 0 and 2 are [ ]
            return [self.parse_node(n) for n in node.children[1].children]
        else:
            logger.debug('unk %s', node.element)
        logger.debug('Elem: %s, Name: %s, Val: %s', node.element, node.element.name, node.string)
        assert False


    def parse_text(self, text):
        val = self.parser.parse(text)
        root = val.tree.children[0]
        res = self.parse_node(root)
        return res
