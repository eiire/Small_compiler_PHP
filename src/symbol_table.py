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

            if check_for_identifier(current_token, next_token) and \
                    current_token.token_type == 'identifier_variable' and next_token.token_type == 'operator_assignment':
                symbol_table[current_lvl + ':' + str(len(counter_ns[current_lvl]))] \
                    .append(current_token.lexeme + ':' + 'NULL')

            if check_for_identifier(current_token, next_token) \
                    and current_token.lexeme \
                    not in cut_type_var(list(symbol_table[current_lvl + ':' + str(len(counter_ns[current_lvl]))])):

                if not find_var_above(symbol_table, current_token, current_lvl):

                    if current_token.token_type == 'string_literal' or current_token.token_type == 'numeric_constant':
                        print(warnings(current_token,
                                 next_token,
                                 dict(symbol_table),
                                 current_lvl + ':' + str(len(counter_ns[current_lvl])),
                                 current_construction.lexeme,
                                 operation).rstrip(None))
                    else:
                        symbol_table[current_lvl + ':' + str(len(counter_ns[current_lvl]))]. \
                            append(current_token.lexeme + ':' + 'NULL')  # + ':' + str(displace))

                        print(warnings(current_token,
                                 next_token,
                                 dict(symbol_table),
                                 current_lvl + ':' + str(len(counter_ns[current_lvl])),
                                 current_construction.lexeme,
                                 operation).rstrip(None))
                else:
                    print(warnings(current_token,
                             next_token,
                             dict(symbol_table),
                             current_lvl + ':' + str(len(counter_ns[current_lvl])),
                             current_construction.lexeme,
                             operation).rstrip(None), find_var_above(symbol_table, current_token, current_lvl))
            elif current_token.token_type == 'operator_assignment' and \
                    (next_token.token_type == 'string_literal' or next_token.token_type == 'numeric_constant'):
                change_type_main_var(symbol_table, current_construction, next_token, current_lvl)

        # Появилась новая вложенность на том же самом у р о в н е (вложенности)
        elif current_lvl not in [int(_lvls[0:1]) for _lvls in lvls]:
            if current_token.lexeme == '{':
                counter_ns[current_lvl].append('{')

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
    if current_token.token_type in ['operator_sum', 'operator_multiplication', 'operator_substruction',
                                    'operator_division', 'operator_mod']:
        operation = current_token.token_type

    if (current_token.token_type == 'identifier_variable'
        or current_token.token_type == 'string_literal'
        or current_token.token_type == 'numeric_constant') \
            and current_construction.token_type != 'keyword_for' \
            and current_construction.token_type != 'keyword_if' \
            and current_construction.token_type != 'keyword_while'\
            and current_construction.token_type != 'None':
        return True
    else:
        return False
