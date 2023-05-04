
from sara_compis1_tools.AFD_tools import AFD_tools
from sara_compis1_tools.StateAFD import StateAFD
from sara_compis1_tools.Error import Error


class LexEval:
    def __init__(self, filename):
        self.filename = filename
        self.file = open(self.filename, 'r', encoding='utf-8')
        self.lines = self.file.readlines()
        self.file.close()

 
    def evaluate(self, mega, prev_errors=None):
        lines =  [line[:-1] if line[-1] == '\n' else line for line in self.lines]
        afd_tools = AFD_tools()
        tokens = []
        errors = prev_errors if prev_errors else set() 
        afd_tools = AFD_tools()
        symbols = afd_tools.get_symbols(mega)

        for line_no, line in enumerate(lines, start=1):
            i = 0
            lenn = len(line)
            while i < lenn:
                if line[i] not in [' ', '\t', '\n']:
                    start = i
                    if line[i] == '"': 
                        i += 1
                        while i < lenn and line[i] != '"':  
                            current = line[i]
                            if current not in symbols:
                                errors.add(Error(line_no, f'Caracter no reconocido: {current}', i))

                            i += 1
                        if i < lenn and line[i] == '"':  
                            i += 1
                    else:
                        while i < lenn and line[i] not in [' ', '\t', '\n']:
                            current = line[i]
                            if current not in symbols:
                                errors.add(Error(line_no, f'Caracter no reconocido: {current}', i))

                            i += 1
                    lexeme = line[start:i]
                else:
                    lexeme = line[i]
                    i += 1

                accepted = afd_tools.afn_simulation(mega, lexeme)
                if accepted:
                    if accepted != 'empty_value':
                        tokens.append(accepted)
                else:
                    if lexeme not in [' ', '\t', '\n']:
                        if len(lexeme) == 1:
                            errors.add(Error(line_no, f'Caracter no reconocido: {lexeme}', start))
                        elif len(lexeme) > 1:
                            errors.add(Error(line_no, f'Cadena no aceptada: {lexeme}', start))
        return tokens, errors
    

    def sort_errors(self, errors):
        errors = list(errors)
        errors.sort(key=lambda x: x.line)
        i = 0
        while i < len(errors) - 1:
            if errors[i].line == errors[i+1].line and errors[i].error == errors[i+1].error:
                errors.pop(i)
            else:
                i += 1
        return errors


    def print_tokens(self, result_sim):
        tokens, errors = result_sim
        if not errors:
            print('')
            for token in tokens:
                exec(token)
        else:
            print('\n')
            errors = self.sort_errors(errors)
            for error in errors:
                if error.position:
                    print(f'Error en línea {error.line}: \n{error.error}, posición {error.position}\n')
                else:   
                    print(f'Error en línea {error.line}: \n{error.error}\n')

