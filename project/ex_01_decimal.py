from delta import Compiler, Phase

source = '123'

c = Compiler('program')
c.realize(source, Phase.EVALUATION)

#  Parse tree: Da el árbol de parseo de los elementos
# SYNTACTIC_ANALYSIS

# print(c.parse_tree_str)

# SEMANTIC_ANALYSIS. Para atrapar la excepcion de que el número no sea mayor a 2 ** 31
# print(c.parse_tree_str)

# CODE GENERATION
# print(c.wat_code)

# EVALUATION
print(c.result)




