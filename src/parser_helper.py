from .lexer import Token

# Ключевой момент для определения, что в данный момент проверяется
current_construction = Token('None', 'None', 0)

constructions = {'keyword_for': [['identifier_variable', 'operator_assignment', 'numeric_constant'],
                                 ['r_paren', 'l_paren', 'operator_grater', 'operator_less', 'identifier_variable',
                                  'numeric_constant'],
                                 ['identifier_variable', 'operator_assignment', 'operator_sum', 'numeric_constant']],

                 'assign': ['identifier_variable', 'operator_assignment', 'numeric_constant', 'operator_sum',
                            'operator_substruction', 'semi', 'string_literal', 'operator_multiplication']

                 # other constructions
                 }

nesting_stack = []


def check_instruction(current_tok, next_tok):
    # подобное начальное условие формируется похожим образом для всех конструкций языка
    if current_construction.token_type == 'None' and \
            (current_tok.token_type == 'identifier_variable' and next_tok.token_type == 'operator_assignment') \
            or current_construction.token_type == 'assign':
        current_construction.token_type = 'assign'

        if next_tok.token_type == 'operator_assignment': current_construction.lexeme = current_tok.lexeme # для main VAR

        if check_construction(current_tok, next_tok) != 'Next':
            raise KeyError

        # left and right part instruction
        if current_tok.lexeme == '=' or current_tok.lexeme == '<' or current_tok.lexeme == '>':
            current_construction.position += 1

        if current_tok.token_type == 'semi':
            current_construction.token_type = 'None'
            current_construction.position = 0
            current_construction.lexeme = 'None'


def check_for(current_tok, next_tok):
    if current_tok.token_type == 'keyword_for' or current_construction.token_type == 'keyword_for':
        current_construction.token_type = 'keyword_for'

        if current_tok.lexeme == ';':
            current_construction.position += 1
            if (current_construction.position == 2 or 1 or 0) and next_tok.position == 'end_str':
                return current_tok.position

        if current_construction.position != 2 and check_construction(current_tok, next_tok) \
                == 'End_construction':
            return current_tok.position

        # check expression in for without skin
        if current_tok.token_type not in constructions[current_construction.token_type][current_construction.position] \
                and current_tok.token_type != 'semi' and current_tok.lexeme != '(' and current_tok.lexeme != ')' \
                and current_tok.token_type != 'keyword_for' and current_tok.lexeme != '{':
            raise KeyError

        if check_construction(current_tok, next_tok) == -1:
            return current_tok.position
        elif check_construction(current_tok, next_tok) == 'End_construction':
            current_construction.token_type = 'None'
            current_construction.position = 0


def check_php(current_tok):
    if current_tok.position == "1:0" and current_tok.token_type == 'keyword_<?php':
        return 'Next'
    elif current_tok.position != "1:0" and current_tok.token_type == 'keyword_<?php':
        return current_tok.position


def check_construction(curent_tok, next_tok):
    if curent_tok.token_type in constructions[current_construction.token_type]:
        return 'Next'
    elif (curent_tok.lexeme == ';' and next_tok.token_type == 'None') or curent_tok.lexeme == '{':
        return 'End_construction'


def check_nesting():
    count_brace = 0
    for namespace in nesting_stack:
        if namespace.lexeme == '{':
            count_brace += 1
        if namespace.lexeme == '}':
            count_brace -= 1
    return count_brace
