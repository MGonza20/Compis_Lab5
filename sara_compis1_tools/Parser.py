
class ruleLine:
    def __init__(self, line_no, line):
        self.line_no = line_no
        self.line = line

class prod_obj:
    def __init__(self, name):
        self.name = name
        self.productions = []
        self.augmented = False

class group_i:
    def __init__(self, i_num):
        self.i_num = i_num
        self.heart = []
        self.productions = []


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
                            prod.productions.append(list_)
                            indx += 1

                    self.productions.append(prod)
                    indx += 1


    def gen_aumented_grammar(self):
        first_prod = self.productions[0]
        augmented_grammar = prod_obj(f"{first_prod.name}'")
        augmented_grammar.productions.append(['•', first_prod.name])
        augmented_grammar.augmented = True
        self.productions.insert(0, augmented_grammar)


    def process_element_productions(self, element, checked_elements, elements_to_process, new_group, non_terminal_names):
        
        element_productions = [prod for prod in self.productions if prod.name == element]

        if not element_productions:
            return

        element_production = element_productions[0]
        for production in element_production.productions:
            first_element = production[0]

            if first_element not in checked_elements:
                checked_elements.append(first_element)
                elements_to_process.append(first_element)

            production.insert(0, '•')

            if production not in new_group.productions:
                new_prod_obj = prod_obj(element_production.name)
                new_prod_obj.productions.append(production)
                new_group.productions.append(new_prod_obj)



    def closure(self, no):
        augmented_production = [prod for prod in self.productions if prod.augmented]
        non_terminal_names = list(set(prod.name for prod in self.productions))

        if not augmented_production:
            return None

        augmented_production = augmented_production[0]

        ## Setup inicial de prueba
        # augmented_production = prod_obj('E')
        
        ## Prueba 1
        # augmented_production.productions.append(['E', '+', '•', 'T'])

        ## Prueba 2
        # augmented_production.productions.append(['E', '•'])
        new_group = group_i(no)
        new_group.heart.append(augmented_production)

        checked_elements = []
        elements_to_process = []

        for item in new_group.heart:
            dot_index = item.productions[0].index('•')
            if dot_index +1 < len(item.productions[0]):
                element_after_dot = item.productions[0][dot_index + 1]
                checked_elements.append(element_after_dot)
                self.process_element_productions(element_after_dot, checked_elements, elements_to_process, new_group, non_terminal_names)

        while elements_to_process:
            element = elements_to_process.pop()
            if element in non_terminal_names:
                self.process_element_productions(element, checked_elements, elements_to_process, new_group, non_terminal_names)

        return new_group

                
                    

if __name__ == "__main__":
    parser = Parser("sara_compis1_tools/slr-1.yalp")
    parser.set_values()
    parser.gen_aumented_grammar()
    wut = parser.closure(0)
    print(parser.tokens)



