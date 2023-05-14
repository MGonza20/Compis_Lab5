

from generated import Generated
from Parser import Parser

g = Generated()
tokens_scanner = set(g.return_tokens())

p = Parser('sara_compis1_tools/slr-2-ok.yalp')
tokens_parser = set(p.return_tokens())


errors = p.analyze_yapar()
errors = sorted(errors, key=lambda x: x[1])
all_errors = []
for error_message, indx in errors:
    all_errors.append(error_message)
if set(tokens_scanner) != set(tokens_parser):
    all_errors.append('Error: Los tokens no son iguales en el scanner y el parser')


if all_errors:
    print('\nErrores encontrados en archivo .yalp:\n')
    for error_message, indx in errors:
        print(f'{error_message}\n')
else:    
    auto = p.construct_automata()
    p.draw_automata_p(auto)

    firsts = p.all_first()
    follows = p.all_follows()

    print('\nResultados de funcion primero:')
    for k, v in firsts.items():
        print(f'Primero({k}) = {v}')

    print('\nResultados de funcion siguiente:')
    for k, v in follows.items():
        print(f'Siguiente({k}) = {v}')
    print()
