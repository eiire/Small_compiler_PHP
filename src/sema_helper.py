def warnings(current_token, symbol_table, lvl_and_ns, variable):
    # пробежаться относительно конструкции по текущим значениям типов переменной (слева) из инструкции
    print(current_token.lexeme, lvl_and_ns, variable)


def cut_type_var(list_vars):
    new_list_vars = []
    for var in list_vars:
        new_list_vars.append(var[:var.find(':')])
    return new_list_vars


def find_var_above(symbol_table, current_token, current_lvl):
    found = False
    for lvl, variables in symbol_table.items():
        if lvl[:lvl.find(':')] != current_lvl:
            if current_token.lexeme in cut_type_var(list(variables)):
                found = True
    return found