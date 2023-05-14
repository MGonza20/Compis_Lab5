

from generated import Generated
from Parser import Parser

g = Generated()
tokens_scanner = g.return_tokens()

p = Parser('slr-1.yalp')
tokens_parser = p.return_tokens()

if set(tokens_scanner) == set(tokens_parser):
    print('Los tokens son iguales')
else:
    print('Los tokens no son iguales')
