from src.parser_helper import nesting_stack, current_construction

symbol_table = {
    '0': [],
}


# В зависимости от появления конструкций должно расширяться
def check_for_identifier(current_token):
    if current_token.token_type == 'identifier_variable' \
            and current_construction.token_type != 'keyword_for' \
            and current_construction.token_type != 'None':
        return True
    else:
        return False


def craft_symbol_table(current_lvl, current_token, stack_node_hierarchy):
    lvls = [lvl for lvl in list(symbol_table.keys())]

    if current_lvl in lvls:
        if check_for_identifier(current_token) and current_token.lexeme not in symbol_table[current_lvl]:
            symbol_table[current_lvl].append(current_token.lexeme)

    elif current_lvl not in lvls:
        if check_for_identifier(current_token):
            symbol_table.update({current_lvl: [current_token.lexeme]})



# symbol_table = {
#     '0:0': [],
# }
# _dict = {
#     "0": []
# }
# def craft_symbol_table(current_lvl, current_token, stack_node_hierarchy):
#     global _dict
#     lvls = [lvl for lvl in list(symbol_table.keys())]
#
#
#     if current_lvl in lvls:
#         if current_token.lexeme == '{':
#             _dict[current_lvl].append('{')
#
#         symbol_table[current_lvl +':'+ str(len(_dict[current_lvl]))].append(current_token.lexeme)
#
#     elif current_lvl not in lvls:
#         if current_token.lexeme == '{':
#             _dict.update({current_lvl: ['{']})
#
#         if check_for_identifier(current_token):
#             symbol_table.update({current_lvl +':' + str(len(_dict[current_lvl])): [current_token.lexeme]})
#     print(_dict)