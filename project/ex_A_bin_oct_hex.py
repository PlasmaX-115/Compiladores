# Author: A01752791 Maximiliano Benítez Ahumada

from delta import Compiler, Phase

source = '#x0FF1ce'

c = Compiler('program')
c.realize(source, Phase.CODE_GENERATION)
#print(c.parse_tree_str)
#print(c.symbol_table)
print(c.wat_code)
#print(c.result)