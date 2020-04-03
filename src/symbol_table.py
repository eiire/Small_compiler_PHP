from src.parser_helper import nesting_stack, current_construction

symbol_table = {
    '0:0': [],
}

counter_ns = {
    "0": []
}


# В зависимости от появления конструкций должно расширяться
def check_for_identifier(current_token):
    if current_token.token_type == 'identifier_variable' \
            and current_construction.token_type != 'keyword_for' \
            and current_construction.token_type != 'None':
        return True
    else:
        return False


def craft_symbol_table(current_lvl, current_token):
    global counter_ns
    lvls = [lvl for lvl in list(symbol_table.keys())]

    try:
        if current_lvl + ':' + str(len(counter_ns[current_lvl])) in lvls:
            # подсчет областей
            if current_token.lexeme == '{':
                counter_ns[current_lvl].append('{')

            if check_for_identifier(current_token) \
                    and current_token.lexeme not in symbol_table[current_lvl + ':' + str(len(counter_ns[current_lvl]))]:
                symbol_table[current_lvl + ':' + str(len(counter_ns[current_lvl]))].append(current_token.lexeme)

        elif current_lvl not in lvls:
            if current_token.lexeme == '{':
                counter_ns.update({current_lvl: ['{']})

            if check_for_identifier(current_token):
                symbol_table.update({current_lvl + ':' + str(len(counter_ns[current_lvl])): [current_token.lexeme]})
    except:
        # Создание областей
        if current_token.lexeme == '{':
            counter_ns.update({current_lvl: ['{']})

# symbol_table = {
#     '0:0': [],
# }
# counter_ns = {
#     "0": []
# }
# def craft_symbol_table(current_lvl, current_token, stack_node_hierarchy):
#     global counter_ns
#     lvls = [lvl for lvl in list(symbol_table.keys())]
#
#
#     if current_lvl in lvls:
#         if current_token.lexeme == '{':
#             counter_ns[current_lvl].append('{')
#
#         symbol_table[current_lvl +':'+ str(len(counter_ns[current_lvl]))].append(current_token.lexeme)
#
#     elif current_lvl not in lvls:
#         if current_token.lexeme == '{':
#             counter_ns.update({current_lvl: ['{']})
#
#         if check_for_identifier(current_token):
#             symbol_table.update({current_lvl +':' + str(len(counter_ns[current_lvl])): [current_token.lexeme]})
#     print(counter_ns)

# lvls = [lvl for lvl in list(symbol_table.keys())]
#
# if current_lvl in lvls:
#     if check_for_identifier(current_token) and current_token.lexeme not in symbol_table[current_lvl]:
#         symbol_table[current_lvl].append(current_token.lexeme)
#
# elif current_lvl not in lvls:
#     if check_for_identifier(current_token):
#         symbol_table.update({current_lvl: [current_token.lexeme]})
