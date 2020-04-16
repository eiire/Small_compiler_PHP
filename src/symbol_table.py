from .parser_helper import nesting_stack, current_construction
from .sema_helper import cut_type_var, find_var_above, warnings, change_type_main_var

symbol_table = {
    '0:0': [],
}

counter_ns = {
    "0": []
}


operation = ""


def craft_symbol_table(current_lvl, current_token, next_token):
    global counter_ns
    lvls = [lvl for lvl in list(symbol_table.keys())]

    try:
        if current_lvl + ':' + str(len(counter_ns[current_lvl])) in lvls:
            # подсчет областей
            if current_token.lexeme == '{':
                counter_ns[current_lvl].append('{')

            if check_for_identifier(current_token, next_token) \
                    and current_token.lexeme \
                    not in cut_type_var(list(symbol_table[current_lvl + ':' + str(len(counter_ns[current_lvl]))])):

                if not find_var_above(symbol_table, current_token, current_lvl):
                    if current_token.token_type == 'string_literal' or current_token.token_type == 'numeric_constant':
                        warnings(current_token,
                                 next_token,
                                 dict(symbol_table),
                                 current_lvl + ':' + str(len(counter_ns[current_lvl])),
                                 current_construction.lexeme,
                                 operation)
                    else:
                        symbol_table[current_lvl + ':' + str(len(counter_ns[current_lvl]))]. \
                            append(current_token.lexeme + ':' + 'NULL')

                        warnings(current_token,
                                 next_token,
                                 dict(symbol_table),
                                 current_lvl + ':' + str(len(counter_ns[current_lvl])),
                                 current_construction.lexeme,
                                 operation)
                else:
                    warnings(current_token,
                             next_token,
                             dict(symbol_table),
                             current_lvl + ':' + str(len(counter_ns[current_lvl])),
                             current_construction.lexeme,
                             operation)
            elif current_token.token_type == 'operator_assignment' and \
                    (next_token.token_type == 'string_literal' or next_token.token_type == 'numeric_constant'):
                change_type_main_var(symbol_table, current_construction, next_token, current_lvl)

        elif current_lvl not in lvls:
            if current_token.lexeme == '{':
                counter_ns.update({current_lvl: ['{']})

            if check_for_identifier(current_token, next_token):
                symbol_table.update({current_lvl + ':' + str(len(counter_ns[current_lvl])):
                                         [current_token.lexeme + ':' + 'NULL']})
    except:
        # Создание областей
        if current_token.lexeme == '{':
            counter_ns.update({current_lvl: ['{']})


def check_for_identifier(current_token, next_token):
    global operation
    # Выяснить совершаемую операцию ДО определения типа переменной
    if current_token.token_type == 'operator_sum' or current_token.token_type == 'operator_multiplication':
        operation = current_token.token_type

    if (current_token.token_type == 'identifier_variable'
        or current_token.token_type == 'string_literal'
        or current_token.token_type == 'numeric_constant') \
            and current_construction.token_type != 'keyword_for' \
            and current_construction.token_type != 'None':
        return True
    else:
        return False
