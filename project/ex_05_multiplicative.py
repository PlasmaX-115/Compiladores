from delta import Compiler, Phase

source = '5 * 6 / 7 % 3'

c = Compiler('program')
c.realize(source, Phase.CODE_GENERATION)
#print(c.parse_tree_str)
print(c.wat_code)
#print(c.result)




