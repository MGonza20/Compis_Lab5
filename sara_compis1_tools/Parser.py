
import networkx as nx
from graphviz import Digraph


class ruleLine:
    def __init__(self, line_no, line):
        self.line_no = line_no
        self.line = line

class prod_obj:
    def __init__(self, name):
        self.name = name
        self.production = []

class group_i:
    def __init__(self):
        self.heart = []
        self.productions = []
        self.transitions = {}


class Parser:
    def __init__(self, filename):
        self.filename = filename
        self.tokens = []
        self.ignored_tokens = []
        self.productions = []
    
    def clean_comments(self, joined):
        for index, line in enumerate(joined):
            line_wo_comment = ''
            i = 0
            while i < len(line):
                if i < len(line) - 1 and line[i] == '/' and line[i + 1] == '*':
                    while i < len(line) - 1 and (line[i] != '*' or line[i + 1] != '/'):
                        i += 1
                    i += 2
                else:
                    line_wo_comment += line[i]
                    i += 1
            joined[index] = line_wo_comment
        return joined


    def getLines(self):
        f = open(self.filename, "r", encoding="utf-8")
        lines = f.readlines()
        f.close()
        
        lines_with_n = [n[:-1] if n[-1] == '\n' else n for n in lines]
        check_comments = [lll.split(' ') for lll in lines_with_n]  
        joined = [' '.join(line) for line in check_comments]
            
        return self.clean_comments(joined)
    

    def remove_spaces_list(self, lines):
        for line in lines:
            if not all(element == '' for element in line):
                while '' in line:
                    for element in line:
                        if element == '':
                            line.pop(line.index(element))
        return lines
    

    def process_elements(self, line, prod, multiple_r=False):
        list_ = []
        for element in line:
            if element == '|':
                if list_:
                    prod.productions.append(list_)
                list_ = []
            elif element[-1] == ';':
                if len(element) > 1:
                    list_.append(element[:-1])
                else:
                    if element and element != ';':
                        list_.append(element)
                if list_:
                    prod.productions.append(list_)
                break
            else:
                list_.append(element)

        if multiple_r:
            return prod, element, list_
        else:
            return prod
    
    
    def set_values(self):
        splits = [line.split(' ') for line in self.getLines()]
        splits = self.remove_spaces_list(splits)
        
        for indx, line in enumerate(splits, start=1):
            if line[0] == '%token':
                for token in line[1:]:
                    self.tokens.append(token)
            elif line[0] == 'IGNORE':
                for token in line[1:]:
                    if token in self.tokens:
                        ignored_token = self.tokens.pop(self.tokens.index(token))
                        self.ignored_tokens.append(ignored_token)

            elif line[0] and line[0][-1] == ':':
                prod = prod_obj(line[0][:-1])

                if len(line) > 1:
                    prod = self.process_elements(line[1:], prod)
                    self.productions.append(prod)
                else:
                    while True:
                        prod, element, list_ = self.process_elements(splits[indx], prod, multiple_r=True)
                        if element[-1] == ';':
                            break
                        else:
                            prod.production.append(list_)
                            indx += 1

                    self.productions.append(prod)
                    indx += 1


    def process_element_productions(self, element, checked, to_do, new_group):
        
        all_productions = self.productions.copy()
        element_productions = [prod for prod in all_productions if prod.name == element]
        if not element_productions:
            return

        element_production = element_productions[0]
        for production in element_production.production:

            first_element = production[0]
            if first_element not in checked:
                checked.append(first_element)
                to_do.append(first_element)

            new_production = ['•'] + production
            if new_production not in new_group.productions:
                new_prod_obj = prod_obj(element_production.name)
                new_prod_obj.production = new_production
                new_group.productions.append(new_prod_obj)


    def closure(self, heart_prductions):
        non_terminal_names = list(set(prod.name for prod in self.productions))

        new_group = group_i()
        for heart_production in heart_prductions:
            new_group.heart.append(heart_production)

        checked = []
        to_do = []

        for item in new_group.heart:
            dot_index = item.production.index('•')
            if dot_index +1 < len(item.production):
                element_after_dot = item.production[dot_index + 1]
                checked.append(element_after_dot)
                self.process_element_productions(element_after_dot, checked, to_do, new_group)

        while to_do:
            element = to_do.pop()
            if element in non_terminal_names:
                self.process_element_productions(element, checked, to_do, new_group)
        
        return new_group
    

    def go_to(self, group, element):
        new_group = group_i()
        all_productions = [prod for prod in group.productions] + [prod for prod in group.heart]

        for p in all_productions:
            dot_index = p.production.index('•')
            if dot_index + 1 < len(p.production) and p.production[dot_index + 1] == element:
                new_p = p.production.copy()
                new_p.pop(dot_index)
                new_p.insert(dot_index + 1, '•')
                new_prod_obj = prod_obj(p.name)
                new_prod_obj.production = new_p
                new_group.heart.append(new_prod_obj)
        
        res = self.closure(new_group.heart).productions
        new_group.productions =  res if res else []

        return new_group



    def get_group_transitions(self, group):
        transitions = set()
        all_productions = [prod for prod in group.productions] + [prod for prod in group.heart]
        
        for p in all_productions:
            dot_index = p.production.index('•')
            if dot_index + 1 < len(p.production):
                element_after_dot = p.production[dot_index + 1]
                transitions.add(element_after_dot)

        return list(transitions)


    def same_heart(self, lista1, lista2):
        return len(lista1) == len(lista2) and all(item in lista2 for item in lista1)


    def repeated(self, obj, dict_repeated):
        c_list = []
        for els in obj:
            list_ = [els.name] + els.production
            c_list.append(list_)

        for key, value in dict_repeated.items():
            reps_values = [[v.name] + v.production for v in value]
            if self.same_heart(reps_values, c_list):
                return key
        return None
    

    def construct_automata(self):
        first_prod = self.productions[0]
        augmented_p = prod_obj(f"{first_prod.name}'")
        augmented_p.production = ['•', first_prod.name]

        groups = {}
        group_count = 0
        augmented_prod = self.closure([augmented_p])
        groups[group_count] = augmented_prod
        toDo = [group_count]

        dict_repeated = {}
        dict_repeated[group_count] = augmented_prod.heart
        
        while toDo:
            no = toDo.pop()
            transitions = self.get_group_transitions(groups[no])
            for t in transitions:
                new_group = self.go_to(groups[no], t)
        
                if new_group.heart:
                    existing_group_no = self.repeated(new_group.heart, dict_repeated)
                    
                    if not existing_group_no:
                        group_count += 1
                        groups[group_count] = new_group
                        dict_repeated[group_count] = new_group.heart
                        toDo.append(group_count)
                        groups[no].transitions[t] = group_count

                    else:
                        groups[no].transitions[t] = existing_group_no
                
        for no, new_group in groups.items():
            for h in new_group.heart:
                if h.name[-1] == "'" and h.production[-1] == '•':
                    groups[no].transitions['$'] = 'aceptar'

        return groups

                                     
    def draw_automata_p(self, automata):
        G = nx.MultiDiGraph()
        for no, state in automata.items():
            h_list = [(p.name, '→', ' '.join(p.production)) for p in state.heart]
            h_list = [' '.join(h) for h in h_list]
            h_list = '<BR/>'.join(h_list)
            p_list = [(p.name, '→', ' '.join(p.production)) for p in state.productions]
            p_list = [' '.join(p) for p in p_list]
            p_list = '<BR/>'.join(p_list)
            G.add_node(str(no), h_list=h_list, p_list=p_list)

            for transition, final_dest in state.transitions.items():
                G.add_node(str(final_dest))
                G.add_edge(str(no), str(final_dest), label=transition, dir='forward')

        dot = Digraph()
        dot.attr(rankdir='LR') 
        dot.attr(splines='polyline') 
        for u, v, data in G.edges(data=True):
            dot.edge(u, v, label=data['label'], dir=data['dir'])
        for node in G.nodes:
            if node == 'aceptar':
                dot.node(node, shape='none')
            else:
                attrs = G.nodes[node]
                dot.node(node, '''<
                <TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0">
                    <TR><TD>{0}</TD></TR>
                    <TR><TD BGCOLOR="lightgrey">{1}</TD></TR>  
                </TABLE>>'''.format(attrs['h_list'], attrs['p_list']), shape='none')
        dot.render('x/automata_x', format='png')


    def first(self):
        non_terminal = list(set(prod.name for prod in self.productions))
        all_prods = [[prod.name] + p for prod in self.productions for p in prod.production]

        first = {}
        for nt in non_terminal:
            first[nt] = set()
            to_analize = []
            for p in all_prods:
                if len(p) > 1 and p[0] == nt:
                    for el in p[1:]:
                        to_analize.append(p[1])

            while to_analize:
                a = to_analize.pop()
                if a not in non_terminal:
                    first[nt].add(a)
                else:
                    for p in all_prods:
                        if len(p) > 1 and p[0] == a:
                            to_analize.append(p[1])

        a = []
                
        



if __name__ == "__main__":
    parser = Parser("sara_compis1_tools/slr-1.yalp")
    parser.set_values()
    # wut = parser.construct_automata()
    # parser.draw_automata_p(wut)
    parser.first()



