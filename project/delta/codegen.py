from arpeggio import PTNodeVisitor


class CodeGenerationVisitor(PTNodeVisitor):

    WAT_TEMPLATE = ''';; Code generated by the Delta compiler
(module
  (func
    (export "_start")
    (result i32)
{}  )
)
'''

    def __init__(self, symbol_table, **kwargs):
        super().__init__(**kwargs)
        self.__symbol_table = symbol_table

    def visit_program(self, node, children):
        #print('program', children)
        #Agrega todas las declaraciones de variables hasta arriba del código.
        def declare_variables():
            return ''.join([f'    (local ${var_name} i32)\n'
                            for var_name in self.__symbol_table])
        return CodeGenerationVisitor.WAT_TEMPLATE.format(
            declare_variables()
            + ''.join(children))
    
    def visit_statement(self, node, children):
        return children[0]
    
    def visit_declaration(self, node, children):
        return ''
    
    def visit_assignment(self, node, children):
        return children[1] + children[0]
    
    def visit_lhs_variable(self, node, children):
        name = node.value
        return f'    local.set ${name}\n'
    
    def visit_if(self, node, children):
        result = (children[0]
                  +'    if\n'
                  + children[1])
        if len (children) == 3:
            result += ('    else\n'
                       + children[2])
        result += '    end\n'
        return result

    
    def visit_block(self, node, children):
        return ''.join(children)
    
    def visit_while(self, node, children):
        return (
            '    block\n'
            +'    loop\n'
            + children[0]
            +'    i32.eqz\n'
            +'    br_if 1\n'
            + children[1]
            + '    br 0\n'
            +'    end\n'
            +'    end\n'
        )

    def visit_expression(self, node, children):
        result = [children[0]]
        #El ciclo 'for 'se encarga de identificar los operadores a través de los índices impares (1, 3, 5, etc.)
        #Así se sabe qué operación realizar dependiendo del signo a través de 'case'.
        for i in range(1, len(children), 2):
            result.append(children[i + 1])
            match children[i]:
                case '+':
                    result.append('    i32.add\n')
                case '-':
                    result.append('    i32.sub\n')
        return ''.join(result)
    
    def visit_multiplicative(self, node, children):
        result = [children[0]]
        #El ciclo 'for 'se encarga de identificar los operadores a través de los índices impares (1, 3, 5, etc.)
        #Así se sabe qué operación realizar dependiendo del signo a través de 'case'.
        for i in range(1, len(children), 2):
            result.append(children[i + 1])
            match children[i]:
                case '*':
                    result.append('    i32.mul\n')
                case '/':
                    result.append('    i32.div_s\n')
                case '%':
                    result.append('    i32.rem_s\n')
        return ''.join(result)
        
    def visit_decimal(self, node, children):
        return f'    i32.const {node.value}\n'

    def visit_boolean(self, node, children):
        #print('boolean', children)
        if children[0] == 'true':
            return '    i32.const 1\n'
        else:
            return '    i32.const 0\n'
        
    def visit_unary(self, node, children):
        result = children[-1]
        for op in children[-2::-1]:
            match op:
                case'+':
                    pass # Do nothing

                case'-':
                    result = (
                        '    i32.const 0\n'
                        + result
                        + '    i32.sub\n'
                    )  # Subtracts value with zero. We get the same number, but negative.

                case'!':
                    result += '    i32.eqz\n' # Equals zero.
        return result
        
    def visit_parenthesis(self, node, children):
        return children[0]
    
    def visit_rhs_variable(self, node, children):
        name = node.value
        return f'    local.get ${name}\n'
    
        