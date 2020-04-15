prev_var = ""


def warnings(current_token, next_token, symbol_table, lvl_and_ns, variable):
    global prev_var
    if current_token.token_type == 'identifier_variable' \
            or current_token.token_type == 'numeric_constant' \
            or current_token.token_type == 'string_literal':
        prev_var = get_type_var(symbol_table, current_token, lvl_and_ns, type_or_var='TYPE')

    if get_type_var(symbol_table, current_token, lvl_and_ns) == 'NULL' \
            and next_token.token_type != 'operator_assignment':
        print(f"NOTICE Undefined variable: {current_token.lexeme} on {current_token.position}")

    if prev_var == 'string_literal' and current_token.lexeme[1:-1-1].isdigit() != True and next_token.token_type != 'semi':
        print(f"Warning: A non-numeric value encountered in {current_token.position}")


def cut_type_var(list_vars):
    new_list_vars = []
    for var in list_vars:
        if var.find(':') != -1:
            new_list_vars.append(var[:var.find(':')])
        else:
            new_list_vars.append(var)
    return new_list_vars


def change_type_main_var(symbol_table, main_var_const, next_token, current_lvl):
    for lvl, variables in symbol_table.items():
        if lvl[:lvl.find(':')] == current_lvl and main_var_const.lexeme in cut_type_var(list(variables)):
            if next_token.lexeme[1:-1-1].isdigit() == True:
                variables[-1] = variables[-1][:variables[-1].find(':')] + ':' + 'numeric_constant'
            else:
                variables[-1] = variables[-1][:variables[-1].find(':')] + ':' + next_token.token_type


def get_type_var(symbol_table, current_token, current_lvl, type_or_var='TYPE'):
    # получить нужный уровень и последний namespace переменной
    data_var = ""
    for lvl, variables in symbol_table.items():
        if lvl[:lvl.find(':')] != current_lvl:
            if current_token.lexeme in cut_type_var(list(variables)):
                data_var = lvl
    if type_or_var == 'TYPE':
        if current_token.token_type == 'string_literal':
            return 'string_literal'
        if current_token.token_type == 'numeric_constant':
            return 'numeric_constant'
        if current_token.token_type == 'identifier_variable':
            return symbol_table[data_var][-1].split(':')[1]
    elif type_or_var == 'VAR':
        return symbol_table[data_var][-1].split(':')[0]


def find_var_above(symbol_table, current_token, current_lvl):
    found = False
    if current_lvl == 0 and current_token.lexeme in cut_type_var(list(symbol_table["0:0"])): return False

    for lvl, variables in symbol_table.items():
        if lvl[:lvl.find(':')] != current_lvl:
            if current_token.lexeme in cut_type_var(list(variables)):
                found = True
    return found
