from Format import Format
from directAFD import AFD
from StateAFD import StateAFD
from Error import Error
import sys


class Token:
        def __init__(self, name):
            self.name = name
            self.regex = None
            self.line_no = None
            self.value = None
    
        def __str__(self):
            return f"Token({self.name}, {self.regex})"


class ruleLine:
    def __init__(self, line_no, line):
        self.line_no = line_no
        self.line = line


class Lexer:
    def __init__(self, filename):
        self.filename = filename
        self.tokens = []
        self.tokenizer = None

    
    def remove_spaces(self, lines):
        wo_spaces = []
        for line in lines:
            new_line = []
            between_q = False
            for char in line:
                if char == "'":
                    between_q = not between_q
                if char != " " or between_q:
                    new_line.append(char)
            wo_spaces.append("".join(new_line))
        return wo_spaces
    

    def clean_comments(self, joined):
        for index, line in enumerate(joined):
            line_wo_comment = ''
            i = 0
            while i < len(line):
                if i < len(line) - 1 and line[i] == '(' and line[i + 1] == '*':
                    while i < len(line) - 1 and (line[i] != '*' or line[i + 1] != ')'):
                        i += 1
                    i += 2
                else:
                    line_wo_comment += line[i]
                    i += 1
            joined[index] = line_wo_comment
        return joined


    def getLines(self, tokens_mode):
        f = open(self.filename, "r", encoding="utf-8")
        lines = f.readlines()
        f.close()
        
        if tokens_mode:
            lines = [line.encode('utf-8').decode('unicode_escape') for line in lines]

        lines_with_n = [n[:-1] for n in lines]
        check_comments = [lll.split(' ') for lll in lines_with_n]  

        joined = [' '.join(line) for line in check_comments]
        # Revision de errores en comentarios
        for line_no, lj in enumerate(joined, start=1):
            comments_stack = []
            for i in range(len(lj) - 1):

                current_next = lj[i:i+2]
                if current_next == '(*':
                    comments_stack.append(current_next)
                elif current_next == '*)':
                    if comments_stack and comments_stack[-1] == '(*':
                        comments_stack.pop()
                    else:
                        raise Exception(f"Error en comentario, linea {line_no}")
            if comments_stack:
                raise Exception(f"Error en comentario, linea {line_no}")

        joined = self.clean_comments(joined)
            
        return joined
    

    def special_split(self, text, delimiter):
        result = []
        start = 0
        open_curly_b = 0

        for index, char in enumerate(text):
            if char == '{':
                open_curly_b += 1
            elif char == '}':
                open_curly_b -= 1

            elif char == delimiter and not open_curly_b:
                result.append(text[start:index])
                start = index + 1

        result.append(text[start:])
        return result
    

    def remove_spaces_list(self, lines):
        for line in lines:
            if not all(element == '' for element in line):
                while '' in line:
                    for element in line:
                        if element == '':
                            line.pop(line.index(element))
        return lines
    

    def assign_values(self):
        splits = [self.special_split(line, ' ') for line in self.getLines(tokens_mode=False)]
        splits = self.remove_spaces_list(splits)
        
        start = 0
        rules_lines = []
        for indx, line in enumerate(splits, start=1):
            if line[0] == 'rule':
                start = indx + 1
            if start:
                rules_lines.append(ruleLine(indx, line))

        
        if len(rules_lines) > 1:

            rules_lines = rules_lines[1:]
            for rule in rules_lines:
                if rule.line[0] == '|':
                    rule.line.pop(0)
                if len(rule.line) == 1:
                    rule.line = rule.line[0]

            rules_dict = {}
            for rule in rules_lines:
                name = ''
                value = ''
                inside = False

                for i in range(len(rule.line)):
                    if rule.line[i] == '{':
                        inside = True
                        continue

                    if rule.line[i] == '}':
                        inside = False
                        continue

                    if not inside:
                        if rule.line[i] not in ['\t', ' ']:
                            name += rule.line[i]
                    else:
                        value += rule.line[i]

                if name:
                    rules_dict[name] = (ruleLine(rule.line_no, value.strip()))
        return rules_dict


    def getTokens(self):
        lines = self.remove_spaces(self.getLines(tokens_mode=True))
        for line_no, line in enumerate(lines, start=1):
            # generando tokens
            if line[:3] == 'let':
                name, regex = line[3:].split('=')
                token = Token(name)
                token.regex = regex
                token.line_no = line_no
                self.tokens.append(token)


    def range_maker(self, start, end, no):
        if len(start) == 3 and len(end) == 3:
            start, end = start[1], end[1]

        if start.isalpha() and end.isalpha():
            if ord(start) > ord(end):
                raise Exception("Error: Rango incorrecto, linea " + str(no))
            elements = [chr(i) for i in range(ord(start), ord(end) + 1)]
            aaa = 123

        elif start.isdigit() and end.isdigit():
            start, end = int(start), int(end)
            if start > end:
                raise Exception("Error: Rango incorrecto, linea " + str(no))
            elements = [str(i) for i in range(start, end + 1)]
        else:
            raise Exception("Formato de regex incorrecto")

        return elements

    
    def change_range_format(self):
        tokens = self.tokens
        for token in tokens:
            new_regex = ''
            i = 0

            if token.regex[0] == "'" and token.regex[-1] == "'" and token.regex.count("'") == 2:
                unquoted_token = token.regex[1:-1]
                token.regex = f'({unquoted_token})'
                continue
            

            while i < len(token.regex):

                p_left = token.regex.count("(")
                p_right = token.regex.count(")")
                if (p_left + p_right) % 2 != 0:
                    raise Exception("Error: Los parentesis no estan balanceados, "+ "linea " + str(token.line_no))
                
                c_left = token.regex.count("[") 
                c_right = token.regex.count("]") 
                if (c_left + c_right )% 2 != 0:
                    raise Exception("Error: Los corchetesno estan balanceados, "+ "linea " + str(token.line_no))

                
                if token.regex[i] == '[':
                    if token.regex.count("'") % 2 != 0:
                        raise Exception("Error en comillas, " + "linea " + str(token.line_no))
                    
                    content = ""
                    j = i + 1
                    while token.regex[j] != ']':
                        content += token.regex[j]
                        j += 1

                    if content.count("''") > 0:
                        content = content.replace("''", "'|'")
                        tokens_list = content.split("|")

                        elements = []
                        for k in range(len(tokens_list)):
                            if tokens_list[k] == "'-'":
                                continue
                            elif '-' in tokens_list[k]:
                                start, end = tokens_list[k].split('-')
                                elements += self.range_maker(start, end, token.line_no)

                        if elements:
                            content = '|'.join(elements)

                    else:
                        if '-' in content:
                            if content.count('-') > 1:
                                raise Exception("Formato de regex incorrecto,"+ "linea " + str(token.line_no))
                            start, end = content.split('-')
                            elements = self.range_maker(start, end, token.line_no)
                            content = '|'.join(elements)
                        elif '-' not in content:
                            content = content[1:-1]
                            elements = [content[i] for i in range(len(content))]
                            content = '|'.join(elements)
                    new_regex += '(' + content + ')'
                    i = j
                else:
                    check = ""
                    j = i
                    while token.regex[j] not in ['+', '*', '?', '(', ')', '[', ']']:
                        check += token.regex[j]
                        j += 1
                    keys = [tk.name for tk in tokens]
                    if check in keys:
                        i = j - 1
                        new_regex += check
                    else:
                        new_regex += token.regex[i]
                i += 1

            count_all = int((new_regex.count('(') + new_regex.count(')')) /2)
            if not count_all or new_regex[-1] in ['+', '*', '?']:
                if  new_regex[0] == "'" and new_regex[-1] == "'":
                    new_regex = new_regex[1:-1]
                new_regex = f'({new_regex})'

            token.regex = new_regex


    def replace_tokens(self):
        for tk in self.tokens:
            for token in self.tokens:
                index = tk.regex.find(token.name)
                while index != -1:
                    right_side = (index + len(token.name) == len(tk.regex) or not ((tk.regex[index + len(token.name)])).isalnum()) 

                    if right_side:
                        tk.regex = tk.regex[:index] + token.regex + tk.regex[index + len(token.name):]
                    index = tk.regex.find(token.name, index + 1)

    
    def surround_dot(self):
        for token in self.tokens:
            if token.regex.count('.') > 0:
                token.regex = token.regex.replace('.', "'.'" )
    

    def remove_double_parentheses(self, token):
        i = 0
        output = ""
        while i < len(token):
            if token[i] == '(':
                content = "("
                count_open = 1
                count_control = 1
                i += 1
                while count_open != 0:
                    if token[i] == '(':
                        count_open += 1
                        count_control += 1
                    elif token[i] == ')':
                        count_open -= 1
                    content += token[i]
                    i += 1
                
                start = content[:count_control]
                end = content[-count_control:]
                opp = '('*count_control
                clp = ')'*count_control
                if start == opp and end == clp and count_control > 1: 
                    output += content[count_control-1:-count_control+1]
                else:
                    output += content
                
            else:
                output += token[i]
                i += 1
        return output

    
    def generate_automatas(self):
        mega_content = []
        count = 0
        return_values = self.assign_values()
        done = []
        errors = set()
        for token in self.tokens:
            if token.name in return_values:
                ff = Format(token.regex)
                token.regex = ff.positiveId(token.regex + '#')
                token.regex = ff.zeroOrOneId(token.regex)
                token.regex = self.remove_double_parentheses(token.regex)
                token.regex = ff.concat(token.regex)
                token.value = return_values[token.name]
                done.append(token.name)
                
                afdd = AFD(token)
                new_afd = afdd.generateAFD(count)
                for elem in new_afd:
                    if elem.accepting:
                        elem.value = token.value

                mega_content.append(new_afd)
                count += len(new_afd)

        for rt, rt_val in return_values.items():
            if rt not in [tk.name for tk in self.tokens]:
                if rt[0] != "'" and rt[-1] != "'":
                    errors.add(Error(line=rt_val.line_no, error="Error: Token no definido: " + rt + " en archivo .yal"))

        for value in return_values:
            if value[0] == "'" and value[-1] == "'" and value not in done:
                lenn = len(value)
                token = Token(name=value[1:-1])
                token.regex = value + '#'
                token.value = return_values[value]
                ff = Format(token.regex)
                token.regex = ff.concat(token.regex)
                done.append(token.name)
                
                afdd = AFD(token)
                new_afd = afdd.generateAFD(count)
                for elem in new_afd:
                    if elem.accepting:
                        elem.value = token.value

                mega_content.append(new_afd)
                count += len(new_afd)
        return mega_content, errors, done
    

    def unify(self, mega_content):
        stack = []    
        for element in mega_content:
            for state in element:
                if state.start:
                    state.start = False
                    init_state = StateAFD(name='init', start=True, transitions={})
                    init_state.transitions['949'] = state.name
                    stack.append(init_state)
                stack.append(state)
        return stack
    

    def read(self):
        self.assign_values()
        self.getTokens()
        self.change_range_format()
        self.surround_dot()
        self.replace_tokens()
    

    def change_values(self, mega_automata):
        for state in mega_automata:
            updates = {str(chr(int(key))): state.transitions.pop(key) for key in list(state.transitions.keys())}
            state.transitions.update(updates)


    
if __name__ == '__main__':

    # if len(sys.argv) < 2:
    #     print("Por favor ingrese el archivo .yal")
    #     sys.exit(1)

    # yal_file = sys.argv[1]
    # yal_file = "sara_compis1_tools/con1_1.yal"
    yal_file = "con1_1.yal"
    lexer = Lexer(yal_file)
    
    lexer.read()
    mega_content, errors, done = lexer.generate_automatas()
    mega_automata = lexer.unify(mega_content)
    lexer.change_values(mega_automata)

    with open('generated.py', 'w', encoding="utf-8") as file:
        file.write("from sara_compis1_tools.StateAFD import StateAFD\n")
        file.write("from sara_compis1_tools.lexEval import LexEval\n")
        file.write("from sara_compis1_tools.Error import Error\n")
        file.write("import sys\n\n")
        file.write("mega = [")
        for i, obj in enumerate(mega_automata):
            if obj.value:
                value_str = repr(obj.value.line) if isinstance(obj.value.line, str) else str(obj.value.line)
            else:
                value_str = None
            file.write(f"StateAFD(name='{obj.name}',transitions={obj.transitions},accepting={obj.accepting},start={obj.start}, value={value_str})")
            if i != len(mega_automata) - 1:
                file.write(",")
        file.write("]\n")

        if errors:
            file.write("errors = set([")
            for i, error in enumerate(errors):
                file.write(f"Error(line={error.line}, error='{error.error}')")
                if i != len(errors) - 1:
                    file.write(",")
            file.write("])\n\n")
        else:
            file.write("errors = set()\n\n")

        file.write("class Generated:\n")
        file.write("\tdef return_tokens(self):\n")
        file.write("\t\treturn [")
        for indx, token in enumerate(done):
            if indx == len(done) - 1:
                file.write(f"'{token}'")
            else:
                file.write(f"'{token}',")
        file.write("]\n\n")

        file.write("\tdef parse(self):\n")
        file.write("\t\tif len(sys.argv) < 2:\n\t\t\tprint('Por favor ingrese el archivo plano')\n\t\t\tsys.exit(1)\n")
        file.write("\t\ttxt_file = sys.argv[1]\n\n")
        file.write("\t\tlex = LexEval(txt_file)\n")

        file.write("\t\tresults = lex.evaluate(mega, errors)\n")
        file.write("\t\tlex.print_tokens(results)\n\n")
