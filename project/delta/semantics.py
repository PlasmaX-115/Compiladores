from arpeggio import PTNodeVisitor


class SemanticMistake(Exception):

    def __init__(self, message):
        super().__init__(f'Semantic error: {message}')


class SemanticVisitor(PTNodeVisitor):

    def __init__(self, parser, **kwargs):
        super().__init__(**kwargs)
        self.__parser = parser
        self.__symbol_table = []

    def position(self, node):
        return self.__parser.pos_to_linecol(node.position)

    @property
    def symbol_table(self):
        return self.__symbol_table
    
    def visit_decimal(self, node, children):
        value = int(node.value)
        if value >= 2 ** 31:
            raise SemanticMistake(
                'Out of range decimal integer literal at position'
                f'{self.position(node)} => {value}' 
            )

