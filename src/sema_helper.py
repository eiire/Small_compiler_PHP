current_operations = []

def warnings(current_token, next_token, symbol_table, lvl_and_ns, variable):
    # пробежаться относительно конструкции по текущим значениям типов переменной (слева) из инструкции

    print(get_type_var(symbol_table, current_token, lvl_and_ns))
    # print(current_operations)
    pass


def cut_type_var(list_vars):
    new_list_vars = []
    for var in list_vars:
        if var.find(':') != -1:
            new_list_vars.append(var[:var.find(':')])
        else:
            new_list_vars.append(var)
    return new_list_vars


def find_var_above(symbol_table, current_token, current_lvl):
    found = False
    if current_lvl == 0 and current_token.lexeme in cut_type_var(list(symbol_table["0:0"])): return False

    for lvl, variables in symbol_table.items():
        if lvl[:lvl.find(':')] != current_lvl:
            if current_token.lexeme in cut_type_var(list(variables)):
                found = True
    return found


def get_type_var(symbol_table, current_token, current_lvl):
    # получить нужный уровень и последний namespace переменной
    data_var = ""
    for lvl, variables in symbol_table.items():
        if lvl[:lvl.find(':')] != current_lvl:
            if current_token.lexeme in cut_type_var(list(variables)):
                data_var = lvl
    return symbol_table[data_var][-1].split(':')[0]


def change_type_main_var(symbol_table, main_var_const, next_token, current_lvl):
    for lvl, variables in symbol_table.items():
        if lvl[:lvl.find(':')] == current_lvl and main_var_const.lexeme in cut_type_var(list(variables)):
            variables[-1] = variables[-1][:variables[-1].find(':')] + ':' + next_token.token_type