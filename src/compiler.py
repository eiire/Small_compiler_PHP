import sys
from src.lexer import *
from src.parser import *


def start_compiler():
    file = open("input.txt", 'r')
    file_res = open("result.txt", 'w')

    if len(sys.argv) == 2:
        if sys.argv[1] == "--dump-tokens":
            line_number = 0
            for line in file:
                line_number += 1
                if line.find('"') < line.find('#') < line.rfind('"'):
                    # Generator_tokens --> lexer.tokens_in_line
                    # slize for thist # beginning left
                    for tok in tokens_in_line(line[0:check_thist_heshteg_after_cov(line) - 1], line_number):
                        print(tok.position, " \t", tok.name, "#", tok.token)
                else:
                    # slize for thist # beginning left
                    for tok in tokens_in_line(line.partition('#')[0], line_number):
                        print(tok.position, "\t", tok.name, "#", tok.token)

        elif sys.argv[1] == "--dump-ast":
            line_number = 0
            for line in file:
                line_number += 1
                if line.find('"') < line.find('#') < line.rfind('"'):
                    try:
                        iterator = iter(tokens_in_line(line[0:check_thist_heshteg_after_cov(line) - 1], line_number))
                        next(iterator)
                        for tok in tokens_in_line(line[0:check_thist_heshteg_after_cov(line) - 1], line_number):
                            next_tok = next(iterator)
                            table(tok, next_tok)
                    except StopIteration:
                        table(tok, tok)
                else:
                    try:
                        iterator = iter(tokens_in_line(line.partition('#')[0], line_number))
                        next(iterator)
                        for tok in tokens_in_line(line.partition('#')[0], line_number):
                            next_tok = next(iterator)
                            table(tok, next_tok)
                    except StopIteration:
                        table(tok, tok)


        elif sys.argv[1] == "--dump-asm":
            return 0

        file.close()
        file_res.close()
    else:
        return -1


start_compiler()
