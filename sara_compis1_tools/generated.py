from sara_compis1_tools.StateAFD import StateAFD
from sara_compis1_tools.lexEval import LexEval
from sara_compis1_tools.Error import Error
import sys

mega = [StateAFD(name='init',transitions={'ε': 'A'},accepting=False,start=True, value=None),StateAFD(name='A',transitions={' ': 'B', '\t': 'B', '\n': 'B'},accepting=False,start=False, value=None),StateAFD(name='B',transitions={' ': 'B', '\t': 'B', '\n': 'B'},accepting=True,start=False, value=''),StateAFD(name='init',transitions={'ε': 'C'},accepting=False,start=True, value=None),StateAFD(name='C',transitions={'l': 'D'},accepting=False,start=False, value=None),StateAFD(name='D',transitions={'e': 'E'},accepting=False,start=False, value=None),StateAFD(name='E',transitions={'t': 'F'},accepting=False,start=False, value=None),StateAFD(name='F',transitions={'r': 'G'},accepting=False,start=False, value=None),StateAFD(name='G',transitions={'a': 'H'},accepting=False,start=False, value=None),StateAFD(name='H',transitions={'d': 'I', 'l': 'J'},accepting=True,start=False, value='print("id\\n")'),StateAFD(name='I',transitions={'i': 'K'},accepting=False,start=False, value=None),StateAFD(name='J',transitions={'e': 'L'},accepting=False,start=False, value=None),StateAFD(name='K',transitions={'g': 'M'},accepting=False,start=False, value=None),StateAFD(name='L',transitions={'t': 'N'},accepting=False,start=False, value=None),StateAFD(name='M',transitions={'i': 'O'},accepting=False,start=False, value=None),StateAFD(name='N',transitions={'r': 'P'},accepting=False,start=False, value=None),StateAFD(name='O',transitions={'t': 'Q'},accepting=False,start=False, value=None),StateAFD(name='P',transitions={'a': 'I'},accepting=False,start=False, value=None),StateAFD(name='Q',transitions={'o': 'H'},accepting=False,start=False, value=None),StateAFD(name='init',transitions={'ε': 'R'},accepting=False,start=True, value=None),StateAFD(name='R',transitions={'+': 'S'},accepting=False,start=False, value=None),StateAFD(name='S',transitions={},accepting=True,start=False, value='print("+\\n")'),StateAFD(name='init',transitions={'ε': 'T'},accepting=False,start=True, value=None),StateAFD(name='T',transitions={'(': 'U'},accepting=False,start=False, value=None),StateAFD(name='U',transitions={},accepting=True,start=False, value='print("(\\n")'),StateAFD(name='init',transitions={'ε': 'V'},accepting=False,start=True, value=None),StateAFD(name='V',transitions={')': 'W'},accepting=False,start=False, value=None),StateAFD(name='W',transitions={},accepting=True,start=False, value='print(")\\n")'),StateAFD(name='init',transitions={'ε': 'X'},accepting=False,start=True, value=None),StateAFD(name='X',transitions={'*': 'Y'},accepting=False,start=False, value=None),StateAFD(name='Y',transitions={},accepting=True,start=False, value='print("*\\n")')]
errors = set()

class Generated:
	def return_tokens(self):
		return ['espacioEnBlanco','id','+','(',')','*']

	def parse(self):
		if len(sys.argv) < 2:
			print('Por favor ingrese el archivo plano')
			sys.exit(1)
		txt_file = sys.argv[1]

		lex = LexEval(txt_file)
		results = lex.evaluate(mega, errors)
		lex.print_tokens(results)

