from .lexer import Token

# Ключевой момент для определения, что в данный момент проверяется
current_construction = Token('None', 'None', 0)

constructions = {
    'assign': ['identifier_variable', 'operator_assignment', 'numeric_constant', 'operator_sum',
               'operator_substruction', 'semi', 'string_literal', 'operator_multiplication',
               'operator_mod', 'operator_division'],

    'keyword_echo': ['identifier_variable', 'numeric_constant', 'string_literal', 'comma'],

    # 'keyword_function': ['identifier', 'identifier_variable', 'comma', 'l_paren', 'r_paren'],

    'call_func': ['l_paren', 'r_paren', 'identifier_variable', 'numeric_constant', 'string_literal'],

    'keyword_if': ['r_paren', 'l_paren', 'operator_grater', 'operator_less', 'identifier_variable',
                   'numeric_constant', 'operator_identical'],

    'keyword_while': ['r_paren', 'l_paren', 'operator_grater', 'operator_less', 'identifier_variable',
                      'numeric_constant', 'operator_identical'],

    'keyword_break': [],

    # 'keyword_for': [['identifier_variable', 'operator_assignment', 'numeric_constant'],
    #                 ['r_paren', 'l_paren', 'operator_grater', 'operator_less', 'identifier_variable',
    #                  'numeric_constant'],
    #                 ['identifier_variable', 'operator_assignment', 'operator_sum', 'numeric_constant']],

    # other constructions
}

nesting_stack = []


def check_instruction(current_tok, next_tok):
    # подобное начальное условие формируется похожим образом для всех конструкций языка
    if current_construction.token_type == 'None' and \
            (current_tok.token_type == 'identifier_variable' and next_tok.token_type == 'operator_assignment') \
            or current_construction.token_type == 'assign':
        current_construction.token_type = 'assign'

        if next_tok.token_type == 'operator_assignment': current_construction.lexeme = current_tok.lexeme  # для main VAR

        if check_construction(current_tok, next_tok) == 'Incorrect_construction':
            raise KeyError

        # left and right part instruction
        if current_tok.lexeme == '=' or current_tok.lexeme == '<' or current_tok.lexeme == '>':
            current_construction.position += 1

        if current_tok.token_type == 'semi':
            current_construction.token_type = 'None'
            current_construction.position = 0
            current_construction.lexeme = 'None'


def check_echo(current_tok, next_tok):
    if current_tok.token_type == 'keyword_echo' or current_construction.token_type == 'keyword_echo':
        current_construction.token_type = 'keyword_echo'

        if check_construction(current_tok, next_tok) == 'Incorrect_construction' and \
                current_tok.token_type != 'keyword_echo':
            raise KeyError

        if check_construction(current_tok, next_tok) == 'End_construction':
            current_construction.token_type = 'None'


def check_function(current_tok, next_tok):
    if current_tok.token_type == 'keyword_function' or current_construction.token_type == 'keyword_function':
        current_construction.token_type = 'keyword_function'

        if check_construction(current_tok, next_tok) == 'End_construction':
            current_construction.token_type = 'None'


def check_call_func(current_tok, next_tok):
    if (current_tok.token_type == 'identifier' or current_construction.token_type == 'call_func') \
            and current_construction.token_type != 'keyword_function':
        current_construction.token_type = 'call_func'

        if current_tok.token_type != 'r_paren' and next_tok.token_type == 'semi':
            raise KeyError

        if check_construction(current_tok, next_tok) == 'End_construction':
            current_construction.token_type = 'None'


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

        # Проверка конструкций for`а
        if current_tok.token_type not in constructions[current_construction.token_type][current_construction.position] \
                and current_tok.token_type != 'semi' and current_tok.lexeme != '(' and current_tok.lexeme != ')' \
                and current_tok.token_type != 'keyword_for' and current_tok.lexeme != '{':
            raise KeyError

        if check_construction(current_tok, next_tok) == 'End_construction':
            current_construction.token_type = 'None'
            current_construction.position = 0


def check_if(current_tok, next_tok):
    if current_tok.token_type == 'keyword_if' or current_construction.token_type == 'keyword_if':
        current_construction.token_type = 'keyword_if'

        if check_construction(current_tok, next_tok) == 'End_construction':
            current_construction.token_type = 'None'
            current_construction.position = 0


def check_keyword_break(current_tok, next_tok):
    if current_tok.token_type == 'keyword_break' or current_construction.token_type == 'keyword_break':
        current_construction.token_type = 'keyword_break'

        if check_construction(current_tok, next_tok) == 'End_construction':
            current_construction.token_type = 'None'
            current_construction.position = 0


def check_while(current_tok, next_tok):
    if current_tok.token_type == 'keyword_while' or current_construction.token_type == 'keyword_while':
        current_construction.token_type = 'keyword_while'

        if check_construction(current_tok, next_tok) == 'End_construction':
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
    else:
        return 'Incorrect_construction'


def check_nesting():
    count_brace = 0
    for namespace in nesting_stack:
        if namespace.lexeme == '{':
            count_brace += 1
        if namespace.lexeme == '}':
            count_brace -= 1
    return count_brace
