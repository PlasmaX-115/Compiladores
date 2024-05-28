from arpeggio import PTNodeVisitor


class SemanticMistake(Exception):

    def __init__(self, message):
        super().__init__(f'Semantic error: {message}')


class SemanticVisitor(PTNodeVisitor):

    RESERVED_WORDS = ['true', 'false', 'var', 'if', 'else', 'while']

    def __init__(self, parser, **kwargs):
        super().__init__(**kwargs)
        self.__parser = parser
        self.__symbol_table = []

    def position(self, node):
        return self.__parser.pos_to_linecol(node.position)

    @property
    def symbol_table(self):
        return self.__symbol_table
    
    # Lanzar excepcion si se quiere usar una palabra reservada como nombre de variable.
    def visit_decl_variable(self, node, children):
        name = node.value
        if name in SemanticVisitor.RESERVED_WORDS:
            raise SemanticMistake(
                'Reserved word not allowed as variable name at position '
                f'{self.position(node)} => {name}'
            )
    # Lanzar una excepcion si se quiere declarar una variable dos veces.
        if name in self.__symbol_table:
            raise SemanticMistake(
                'Duplicate variable declaration at position '
                f'{self.position(node)} => {name}'
            )
        self.__symbol_table.append(name)

    # Lanzar excepcion si se hace una asignación a variable no declarada.
    def visit_lhs_variable  (self, node, children):
        name = node.value
        if name not in self.__symbol_table:
            raise SemanticMistake(
                'Assignment to undeclared variable at position '
                f'{self.position(node)} => {name}'
            )

    def visit_decimal(self, node, children):
        value = int(node.value)
        if value >= 2 ** 31:
            raise SemanticMistake(
                'Out of range decimal integer literal at position '
                f'{self.position(node)} => {value}' 
            )
        
    def visit_rhs_variable  (self, node, children):
        name = node.value
        if name not in self.__symbol_table:
            raise SemanticMistake(
                'Undeclared variable reference variable at position '
                f'{self.position(node)} => {name}'
            )

