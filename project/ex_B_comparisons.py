# Author: A01752791 Maximiliano Benítez Ahumada

from delta import Compiler, Phase

source = '1 <= 2 == 1 != 0 > 0 < 0 <= 1'

c = Compiler('program')
c.realize(source, Phase.EVALUATION)
#print(c.parse_tree_str)
#print(c.symbol_table)
#print(c.wat_code)
print(c.result)