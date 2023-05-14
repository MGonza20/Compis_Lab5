from sara_compis1_tools.StateAFD import StateAFD
from sara_compis1_tools.lexEval import LexEval
from sara_compis1_tools.Error import Error
import sys

mega = [StateAFD(name='init',transitions={'ε': 'A'},accepting=False,start=True, value=None),StateAFD(name='A',transitions={'0': 'B', '1': 'B', '2': 'B', '3': 'B', '4': 'B', '5': 'B', '6': 'B', '7': 'B', '8': 'B', '9': 'B'},accepting=False,start=False, value=None),StateAFD(name='B',transitions={'0': 'B', '1': 'B', '2': 'B', '3': 'B', '4': 'B', '5': 'B', '6': 'B', '7': 'B', '8': 'B', '9': 'B'},accepting=True,start=False, value='print("Número entero\\n")'),StateAFD(name='init',transitions={'ε': 'C'},accepting=False,start=True, value=None),StateAFD(name='C',transitions={'0': 'D', '1': 'D', '2': 'D', '3': 'D', '4': 'D', '5': 'D', '6': 'D', '7': 'D', '8': 'D', '9': 'D'},accepting=False,start=False, value=None),StateAFD(name='D',transitions={'0': 'D', '1': 'D', '2': 'D', '3': 'D', '4': 'D', '5': 'D', '6': 'D', '7': 'D', '8': 'D', '9': 'D', '.': 'E'},accepting=False,start=False, value=None),StateAFD(name='E',transitions={'0': 'F', '1': 'F', '2': 'F', '3': 'F', '4': 'F', '5': 'F', '6': 'F', '7': 'F', '8': 'F', '9': 'F'},accepting=False,start=False, value=None),StateAFD(name='F',transitions={'0': 'F', '1': 'F', '2': 'F', '3': 'F', '4': 'F', '5': 'F', '6': 'F', '7': 'F', '8': 'F', '9': 'F'},accepting=True,start=False, value='print("Número decimal\\n")'),StateAFD(name='init',transitions={'ε': 'G'},accepting=False,start=True, value=None),StateAFD(name='G',transitions={'0': 'H'},accepting=False,start=False, value=None),StateAFD(name='H',transitions={'x': 'I'},accepting=False,start=False, value=None),StateAFD(name='I',transitions={'0': 'J', '1': 'J', '2': 'J', '3': 'J', '4': 'J', '5': 'J', '6': 'J', '7': 'J', '8': 'J', '9': 'J', 'a': 'J', 'b': 'J', 'c': 'J', 'd': 'J', 'e': 'J', 'f': 'J', 'A': 'J', 'B': 'J', 'C': 'J', 'D': 'J', 'E': 'J', 'F': 'J'},accepting=False,start=False, value=None),StateAFD(name='J',transitions={'0': 'J', '1': 'J', '2': 'J', '3': 'J', '4': 'J', '5': 'J', '6': 'J', '7': 'J', '8': 'J', '9': 'J', 'a': 'J', 'b': 'J', 'c': 'J', 'd': 'J', 'e': 'J', 'f': 'J', 'A': 'J', 'B': 'J', 'C': 'J', 'D': 'J', 'E': 'J', 'F': 'J'},accepting=True,start=False, value='print("Número hexadecimal\\n")'),StateAFD(name='init',transitions={'ε': 'K'},accepting=False,start=True, value=None),StateAFD(name='K',transitions={'+': 'L', '-': 'L', '*': 'L', '/': 'L'},accepting=False,start=False, value=None),StateAFD(name='L',transitions={},accepting=True,start=False, value='print("Operador aritmetico\\n")'),StateAFD(name='init',transitions={'ε': 'M'},accepting=False,start=True, value=None),StateAFD(name='M',transitions={'^': 'N'},accepting=False,start=False, value=None),StateAFD(name='N',transitions={},accepting=True,start=False, value='print("Operador de potenciacion\\n")')]
errors = set()
tokens = [digitoenterosdecimalesbeggininghexadecimalesaritmeticos]

if len(sys.argv) < 2:
	print('Por favor ingrese el archivo plano')
	sys.exit(1)
txt_file = sys.argv[1]

lex = LexEval(txt_file)
results = lex.evaluate(mega, errors)
lex.print_tokens(results)

from sara_compis1_tools.Visualizer import Visualizer
v = Visualizer()
v.draw_mega_afd(mega)
