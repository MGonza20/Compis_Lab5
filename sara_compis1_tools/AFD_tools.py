from sara_compis1_tools.StateAFD import StateAFD

class AFD_tools:
    def __init__(self):
        pass


    get_state = lambda self, name, states: next(filter(lambda state: state.name == name, states), None)

    def epsilon_clousure(self, state, states):
        
        clousure = {state}
        if 'ε' in state.transitions:
            for target in state.transitions['ε']:
                next_state = self.get_state(target, states)
                clousure |= self.epsilon_clousure(next_state, states)

        return clousure
 

    def move(self, states_set, sym, states):
        res = set()

        for state in states_set:
            if sym in state.transitions:
                for target in state.transitions[sym]:
                    next_state = self.get_state(target, states)
                    res.add(next_state)
        return res


    def afn_simulation(self, afn, str_eval):
        current_states = set(filter(lambda s: s.start, afn))
        epsilon_states = set()

        for state in current_states:
            epsilon_states |= self.epsilon_clousure(state, afn)

        for sym in str_eval:
            next_states = set()

            for state in epsilon_states:
                next_states |= self.move({state}, sym, afn)

            epsilon_states = set()
            for state in next_states:
                epsilon_states |= self.epsilon_clousure(state, afn)

        for state in epsilon_states:
            if state.accepting:
                return state.value if state.value else 'empty_value'


    def get_symbols(self, afn):
        symbols = set()
        for state in afn:
            for sym in state.transitions:
                if sym != 'ε':
                    symbols.add(sym)
        return list(symbols)
    

if __name__ == '__main__':
    afd_tools = AFD_tools()
    mega = [StateAFD(name='init',transitions={'ε': 'A'},accepting=False,start=True, value=None),StateAFD(name='A',transitions={'a': 'B', 'b': 'B', 'c': 'B', 'A': 'B', 'B': 'B', 'C': 'B'},accepting=False,start=False, value=None),StateAFD(name='B',transitions={'a': 'B', 'b': 'B', 'c': 'B', 'A': 'B', 'B': 'B', 'C': 'B', '0': 'B', '1': 'B', '2': 'B', '3': 'B', '4': 'B', '5': 'B', '6': 'B', '7': 'B', '8': 'B', '9': 'B'},accepting=True,start=False, value='print("Identificador\\n")'),StateAFD(name='init',transitions={'ε': 'C'},accepting=False,start=True, value=None),StateAFD(name='C',transitions={'i': 'D'},accepting=False,start=False, value=None),StateAFD(name='D',transitions={'f': 'E'},accepting=False,start=False, value=None),StateAFD(name='E',transitions={},accepting=True,start=False, value='print("If\\n")'),StateAFD(name='init',transitions={'ε': 'F'},accepting=False,start=True, value=None),StateAFD(name='F',transitions={'f': 'G'},accepting=False,start=False, value=None),StateAFD(name='G',transitions={'o': 'H'},accepting=False,start=False, value=None),StateAFD(name='H',transitions={'r': 'I'},accepting=False,start=False, value=None),StateAFD(name='I',transitions={},accepting=True,start=False, value='print("For\\n")'),StateAFD(name='init',transitions={'ε': 'J'},accepting=False,start=True, value=None),StateAFD(name='J',transitions={'w': 'K'},accepting=False,start=False, value=None),StateAFD(name='K',transitions={'h': 'L'},accepting=False,start=False, value=None),StateAFD(name='L',transitions={'i': 'M'},accepting=False,start=False, value=None),StateAFD(name='M',transitions={'l': 'N'},accepting=False,start=False, value=None),StateAFD(name='N',transitions={'e': 'O'},accepting=False,start=False, value=None),StateAFD(name='O',transitions={},accepting=True,start=False, value='print("While\\n")'),StateAFD(name='init',transitions={'ε': 'P'},accepting=False,start=True, value=None),StateAFD(name='P',transitions={'0': 'Q', '1': 'Q', '2': 'Q', '3': 'Q', '4': 'Q', '5': 'Q', '6': 'Q', '7': 'Q', '8': 'Q', '9': 'Q'},accepting=False,start=False, value=None),StateAFD(name='Q',transitions={'0': 'Q', '1': 'Q', '2': 'Q', '3': 'Q', '4': 'Q', '5': 'Q', '6': 'Q', '7': 'Q', '8': 'Q', '9': 'Q'},accepting=True,start=False, value='print("Entero\\n")'),StateAFD(name='init',transitions={'ε': 'R'},accepting=False,start=True, value=None),StateAFD(name='R',transitions={'+': 'S', '-': 'S', '*': 'S', '/': 'S'},accepting=False,start=False, value=None),StateAFD(name='S',transitions={},accepting=True,start=False, value='print("Operador aritmetico\\n")')]
    print(afd_tools.afn_simulation(mega, 'if'))