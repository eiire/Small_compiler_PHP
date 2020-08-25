import sys
from src.lexer import *
from src.parser import *
import json


asm_container = '.intel_syntax noprefix\n.global main\n.LC0:\n.string \"%d\\n\"\nmain:\npush rbp\n' \
                'mov rbp, rsp\n'  # sub rsp, 100

marker = 0
marker_break = -1


def jopafunction(children, parent):
    global asm_container
    for i in children:
        if i["kind"] == "assign":
            if i["right"][:-1].isdigit():  # a = 10
                asm_container += f"mov DWORD PTR [rbp-{i['displace']}], {i['right']}" + "\n"
            else:  # a = b
                temp = None
                right = i["right"][:-1]  # variable
                displace_right = None  # displace variable
                for temp in children:
                    if temp["left"] == right:
                        displace_right = temp["displace"]
                        break
                asm_container += f"mov eax, DWORD PTR [rbp-{displace_right}]\nmov DWORD PTR [rbp-{i['displace']}], eax\n"
        elif i["kind"] == "assign_expression":
            op = {
                "operator_sum": "add ",
                "operator_substruction": "sub ",
                "operator_multiplication": "imul ",
                "operator_division": "idiv "
            }
            if not i["right"]["left"].isdigit() and not i["right"]["right"].isdigit():  # a + b
                temp = None
                right_1 = i["right"]["left"]
                right_2 = i["right"]["right"]
                displace_right_1 = None  # variable
                displace_right_2 = None
                for temp in children:
                    if temp["left"] == right_1:
                        displace_right_1 = temp["displace"]
                        break

                for temp in children:
                    if temp["left"] == right_2:
                        displace_right_2 = temp["displace"]
                        break
                asm_container += f"mov edx, DWORD PTR [rbp-{displace_right_1}]\nmov eax, DWORD PTR [rbp-{displace_right_2}]\n" + op[i["right"]["kind"]] + f"eax, edx\nmov DWORD PTR [rbp-{i['displace']}], eax\n"

            elif not i["right"]["left"].isdigit() and i["right"]["right"].isdigit():  # a + 10
                temp = None
                right_1 = i["right"]["left"]
                displace_right_1 = None  # variable
                for temp in children:
                    if temp["left"] == right_1:
                        displace_right_1 = temp["displace"]
                        break
                asm_container += f"mov eax, DWORD PTR [rbp-{displace_right_1}]\n" + op[i["right"]["kind"]] + f"eax, {i['right']['right']}\nmov DWORD PTR [rbp-{i['displace']}], eax\n"

            elif i["right"]["left"].isdigit() and not i["right"]["right"].isdigit():  # 10 + a
                temp = None
                right_1 = i["right"]["right"]
                displace_right_1 = None  # variable
                for temp in children:
                    print(temp)
                    if temp["left"] == right_1:
                        displace_right_1 = temp["displace"]
                        break
                asm_container += f"mov eax, {i['right']['left']}\nmov edx, DWORD PTR [rbp-{displace_right_1}]\n" + op[i["right"]["kind"]] + f"eax, edx\nmov DWORD PTR [rbp-{i['displace']}], eax\n"

            elif i["right"]["left"].isdigit() and i["right"]["right"].isdigit():  # a = 10 + 10
                asm_container += f"mov eax, {i['right']['right']}\n" + op[i["right"]["kind"]] + f"eax, {i['right']['left']}\nmov DWORD PTR [rbp-{i['displace']}], eax\n"            	

        elif i['kind'] == 'keyword_echo':
            if not i['elements'][:-1].isdigit():
                temp = None
                right = i["elements"][:-1]  # variable
                displace_right = None  # displace variable
                for temp in children:
                    # print(temp)
                    if temp.setdefault("left") == right:#if temp["left"] == right:
                        displace_right = temp["displace"]
                        break

                asm_container += f"mov eax, DWORD PTR [rbp-{displace_right}]\nmov esi, eax\nmov edi, OFFSET FLAT:.LC0\nmov eax, 0\ncall printf\n"
            else:
                asm_container += f"mov eax,{i['elements']}\nmov esi, eax\nmov edi, OFFSET FLAT:.LC0\nmov eax, 0\ncall printf\n"
        elif i['kind'] == 'keyword_if':
            global marker
            marker += 1
            marker_end = marker
            marker_else = marker_end
            jump = {
                "==": "jne",
                "!=": "je",
                "<": "jge",
                ">": "jle"
            }
            if i["condition"]["left"].isdigit() and i["condition"]["right"].isdigit():
                asm_container += f"mov edx, {i['condition']['left']}\nmov eax, {i['condition']['right']}\n"
            elif not i["condition"]["left"].isdigit() and i["condition"]["right"].isdigit(): # if (a == 10)
                temp = None
                left = i["condition"]["left"]
                displace = None  # variable
                for temp in children:
                    if temp["left"] == left:
                        displace = temp["displace"]
                        break
                asm_container += f"mov edx, DWORD PTR[rbp-{displace}]\nmov eax, {i['condition']['right']}\n"
            elif i["condition"]["left"].isdigit() and not i["condition"]["right"].isdigit(): # if (10 == a)
                temp = None
                right = i["condition"]["right"]
                displace = None  # variable
                for temp in children:
                    if temp["left"] == right:
                        displace = temp["displace"]
                        break
                asm_container += f"mov edx, {i['condition']['left']}\nmov eax, DWORD PTR[rbp-{displace}]\n"
            elif not i["condition"]["left"].isdigit() and not i["condition"]["right"].isdigit(): # if (b == a)
                temp = None
                left = i["condition"]["left"]
                right = i["condition"]["right"]
                displace_1 = None  # variable
                displace_2 = None
                for temp in children:
                    if temp["left"] == left:
                        displace_1 = temp["displace"]
                        break

                for temp in children:
                    if temp["left"] == right:
                        displace_2 = temp["displace"]
                        break
                asm_container += f"mov edx, DWORD PTR[rbp-{displace_1}]\nmov eax, DWORD PTR[rbp-{displace_2}]\n"
            asm_container += "cmp edx, eax\n"
            asm_container += f"{jump[i['condition']['op']]} .L{marker}\n"
            jopafunction(i['children'], children)
            asm_container += f".L{marker_end}:\n"

def start_compiler():
    global asm_container
    file = open("src/input.txt", 'r')
    file_res = open("build/result.txt", 'w')

    if len(sys.argv) == 2:
        if sys.argv[1] == "--dump-tokens":
            line_number = 0
            for line in file:
                line_number += 1
                if line.find('"') < line.find('#') < line.rfind('"'):
                    # Generator_tokens --> lexer.tokens_in_line
                    # slize for thist # beginning left
                    for tok in tokens_in_line(line[0:check_thist_heshteg_after_cov(line) - 1], line_number):
                        file_res.write(tok.position + " \t" + tok.lexeme + ' ' + "#" + tok.token_type + '\n')
                else:
                    # slize for thist # beginning left
                    for tok in tokens_in_line(line.partition('#')[0], line_number):
                        file_res.write(tok.position + "\t" + tok.lexeme + ' ' + "#" + tok.token_type + '\n')

        elif sys.argv[1] == "--dump-ast":
            line_number = 0
            for line in file:
                line_number += 1
                line = re.sub('#.+', '', line)
                if line.find('"') < line.find('#') < line.rfind('"') and line != '\n':
                    try:
                        iterator = iter(tokens_in_line(line[0:check_thist_heshteg_after_cov(line) - 1], line_number))
                        next(iterator)
                        for tok in tokens_in_line(line[0:check_thist_heshteg_after_cov(line) - 1], line_number):
                            next_tok = next(iterator)
                            if parsing(tok, next_tok) != 'Next': return print('ERROR in: ', tok.position)
                    except StopIteration:
                        none_tok = Token('None', 'None', 'end_str')
                        if parsing(tok, none_tok) != 'Next': return print('ERROR in: ', tok.position)

                elif (line.find('"') < line.find('#') < line.rfind('"')) == False and line != '\n':
                    try:
                        iterator = iter(tokens_in_line(line.partition('#')[0], line_number))
                        next(iterator)
                        for tok in tokens_in_line(line.partition('#')[0], line_number):
                            next_tok = next(iterator)
                            if parsing(tok, next_tok) != 'Next':
                                # print(parsing(tok, next_tok))
                                return print('ERROR in: ', tok.position)


                    except StopIteration:
                        # пустая строка, вызов парсера с предыдущими значениями токена
                        none_tok = Token('None', 'None', 'end_str')
                        if parsing(tok, none_tok) != 'Next': return print('ERROR in: ', tok.position)
            if check_nesting() != 0:
                print('error: expected ‘}’ at end of input')

        elif sys.argv[1] == "--dump-asm":
            line_number = 0
            for line in file:
                line_number += 1
                line = re.sub('#.+', '', line)
                if line.find('"') < line.find('#') < line.rfind('"') and line != '\n':
                    try:
                        iterator = iter(tokens_in_line(line[0:check_thist_heshteg_after_cov(line) - 1], line_number))
                        next(iterator)
                        for tok in tokens_in_line(line[0:check_thist_heshteg_after_cov(line) - 1], line_number):
                            next_tok = next(iterator)
                            if parsing(tok, next_tok) != 'Next': return print('ERROR in: ', tok.position)
                    except StopIteration:
                        none_tok = Token('None', 'None', 'end_str')
                        if parsing(tok, none_tok) != 'Next': return print('ERROR in: ', tok.position)

                elif (line.find('"') < line.find('#') < line.rfind('"')) == False and line != '\n':
                    try:
                        iterator = iter(tokens_in_line(line.partition('#')[0], line_number))
                        next(iterator)
                        for tok in tokens_in_line(line.partition('#')[0], line_number):
                            next_tok = next(iterator)
                            if parsing(tok, next_tok) != 'Next':
                                # print(parsing(tok, next_tok))
                                return print('ERROR in: ', tok.position)


                    except StopIteration:
                        # пустая строка, вызов парсера с предыдущими значениями токена
                        none_tok = Token('None', 'None', 'end_str')
                        if parsing(tok, none_tok) != 'Next': return print('ERROR in: ', tok.position)
            if check_nesting() != 0:
                print('error: expected ‘}’ at end of input')

            current_node = None

            jopafunction(ast['children'], None)
            asm_container += "nop\npop     rbp \nret\n"
            print(asm_container)

        file.close()
        file_res.close()
    else:
        return -1


start_compiler()

with open("build/symbol_table.json", "w", encoding="utf-8") as file:
    json.dump(symbol_table, file, indent=4)

with open("build/AST.json", "w", encoding="utf-8") as file:
    # print(ast)
    json.dump(ast, file, indent=4)