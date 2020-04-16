type_entity = "NULL"  # отслеживание типа текущего токена в операции


def warnings(current_token, next_token, symbol_table, lvl_and_ns, variable, operation):
    global type_entity
    if current_token.token_type == 'semi': type_entity = "NULL"
    # print(operation)

    if current_token.token_type == 'identifier_variable' \
            or current_token.token_type == 'numeric_constant' \
            or current_token.token_type == 'string_literal':
        type_entity = get_type_var(symbol_table, current_token, lvl_and_ns, type_or_var='TYPE')

    # print(type_entity, current_token.lexeme, next_token.lexeme, operation) # DEBUG
    if get_type_var(symbol_table, current_token, lvl_and_ns) == 'NULL' \
            and next_token.token_type != 'operator_assignment':
        print(f"NOTICE Undefined variable: {current_token.lexeme} on {current_token.position}")

    if operation == 'operator_sum' and type_entity == 'string_literal' \
            and current_token.token_type == "string_literal" and current_token.lexeme[1:-1 - 1].isdigit() \
            and next_token.token_type != 'semi':
        print(f"Warning: A non-numeric value encountered in {current_token.position}")

    elif type_entity == 'numeric_constant' and current_token.token_type == "string_literal" \
            and current_token.lexeme[1:-1 - 1].isdigit() != True and next_token.token_type != 'semi':
        print(f"Warning: A non-numeric value encountered in {current_token.position}")

    elif type_entity == 'string_literal' and next_token.token_type == 'operator_multiplication':
        print(f"Warning: A non-numeric value encountered in {current_token.position}")

    elif operation == 'operator_multiplication' and type_entity == 'string_literal':
        # print(type_entity, current_token.lexeme, next_token.lexeme, operation) # DEBUG
        print(f"Warning: A non-numeric value encountered in {current_token.position}")

    elif operation == 'operator_sum' and type_entity != 'numeric_constant' \
            and current_token.token_type == 'string_literal':
        print(f"Warning: A non-numeric value encountered in {current_token.position}")

    # print(type_entity, current_token.lexeme, next_token.lexeme, operation) # DEBUG


def find_var_above(symbol_table, current_token, current_lvl):
    found = False
    # переменная не находится в namespace какой-либо конструкции(lvl)
    if current_lvl == 0 and current_token.lexeme in cut_type_var(list(symbol_table["0:0"])): return False

    for lvl, variables in symbol_table.items():
        if lvl[:lvl.find(':')] != current_lvl:
            if current_token.lexeme in cut_type_var(list(variables)):
                found = True
    return found


def change_type_main_var(symbol_table, main_var_const, next_token, current_lvl):
    for lvl, variables in symbol_table.items():
        if lvl[:lvl.find(':')] == current_lvl and main_var_const.lexeme in cut_type_var(list(variables)):
            if next_token.lexeme[1:-1 - 1].isdigit():
                variables[-1] = variables[-1][:variables[-1].find(':')] + ':' + 'numeric_constant'
            else:
                variables[-1] = variables[-1][:variables[-1].find(':')] + ':' + next_token.token_type


def get_type_var(symbol_table, current_token, current_lvl, type_or_var='TYPE'):
    data_var = ""
    for lvl, variables in symbol_table.items():
        if lvl[:lvl.find(':')] != current_lvl:
            if current_token.lexeme in cut_type_var(list(variables)):
                data_var = lvl

    if type_or_var == 'TYPE':
        if current_token.token_type == 'string_literal':
            if current_token.lexeme[1:-1 - 1].isdigit():
                return 'numeric_constant'
            else:
                return 'string_literal'
        if current_token.token_type == 'numeric_constant':
            return 'numeric_constant'
        if current_token.token_type == 'identifier_variable':
            return symbol_table[data_var][-1].split(':')[1]
    elif type_or_var == 'VAR':
        return symbol_table[data_var][-1].split(':')[0]


def cut_type_var(list_vars):
    new_list_vars = []
    for var in list_vars:
        if var.find(':') != -1:
            new_list_vars.append(var[:var.find(':')])
        else:
            new_list_vars.append(var)
    return new_list_vars