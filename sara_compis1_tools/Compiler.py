

from generated import Generated
from Parser import Parser

g = Generated()
print(g.return_tokens())

p = Parser('slr-1.yalp')
print(p.return_tokens())
