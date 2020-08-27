import sys
from src.lexer import *
from src.parser import *
from src.assembly import *
import json


def start_compiler():
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

            print(json.dumps(ast, indent=4))

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
            asm_container, displace = generate_assebler(ast['childs'])

            global intro
            intro += f"{displace}\n" + asm_container
            intro += "nop\npop     rbp \nret\n"
            print(intro)

        file.close()
        file_res.close()
    else:
        return -1


start_compiler()

with open("build/symbol_table.json", "w", encoding="utf-8") as file:
    json.dump(symbol_table, file, indent=4)

with open("build/AST.json", "w", encoding="utf-8") as file:
    json.dump(ast, file, indent=4)
