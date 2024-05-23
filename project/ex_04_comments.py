from delta import Compiler, Phase

source = '''
// A line comment.

0

/* 
   A block
   comment.
*/
'''

c = Compiler('program')
c.realize(source, Phase.EVALUATION)
#print(c.parse_tree_str)
#print(c.wat_code)
print(c.result)




