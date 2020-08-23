from .parser_helper import *
from .ast_helper import *
from .symbol_table import *

# общая таблица(общий случай), она дополняется вспомогательной для конструкций из помощника
parser_table = {
    'keyword_for': ['l_paren'],
    'identifier_variable': ['operator_assignment', 'operator_sum', 'operator_substruction', 'operator_multiplication',
                            'operator_grater', 'operator_less', 'r_paren', 'semi', 'comma'],

    'l_paren': ['semi', 'identifier_variable', 'string_literal', 'numeric_constant', 'r_paren'],
    'operator_less': ['numeric_constant', 'identifier_variable'],
    'keyword_if': ['l_paren'],
    'semi': ['None', 'keyword_for', 'semi', 'r_paren', 'numeric_constant', 'identifier_variable'],
    'numeric_constant': ['semi', 'r_paren', 'operator_sum', 'operator_multiplication'],
    'keyword_<?php': ['None'],
    'operator_assignment': ['numeric_constant', 'identifier_variable', 'string_literal'],
    'r_paren': ['semi', 'l_brace', 'r_brace'],
    'l_brace': ['None', 'identifier', 'identifier_variable'],
    'operator_grater': ['numeric_constant'],
    'keyword_break': ['semi'],
    'identifier': ['l_paren'],
    'r_brace': ['None'],
    'operator_sum': ['numeric_constant', 'identifier_variable', 'string_literal'],
    'keyword_?>': ['None'],
    'operator_multiplication': ['identifier_variable', 'numeric_constant', 'string_literal'],
    'string_literal': ['operator_sum', 'semi', 'operator_multiplication', 'dot', 'comma', 'r_paren'],
    'keyword_echo': ['identifier_variable', 'string_literal', 'numeric_constant'],
    'dot': ['string_literal', 'numeric_constant', 'identifier_variable'],
    'comma': ['string_literal', 'numeric_constant', 'identifier_variable'],
    'keyword_function': ['identifier'],
}

ast = {
    "kind": "program",
    "children": [
        # array of nodes
    ]
}

# Парсер использует current_costruction из parser_helper для для поддержания вложенностей и определения, что проверяется
stack_nodes_hierarchy = ['program']  # контроль вложенностей


def parsing(current_tok, next_tok):
    try:
        if next_tok.token_type in parser_table[current_tok.token_type]:
            # print(current_tok.lexeme, next_tok.lexeme, current_construction.token_type) # DEBUGGER)

            # dangerous (в php все конструкции, имеющие вложенность, имеют и открывающую скобку => должно работать)
            if current_tok.lexeme == '(' and current_construction.token_type != 'keyword_echo':
                stack_nodes_hierarchy.append(current_construction.token_type)

            check_php(current_tok)

            check_echo(current_tok, next_tok)

            check_for(current_tok, next_tok)

            check_function(current_tok, next_tok)

            check_call_func(current_tok, next_tok)

            check_instruction(current_tok, next_tok)

            # создасться узел в зависимсти от того, какая конструкция была проверена
            node_creating(current_tok, next_tok)

            #  exit from namespace
            if current_tok.lexeme == '}':
                stack_nodes_hierarchy.pop()

            if current_tok.lexeme == '{' or current_tok.lexeme == '}':
                nesting_stack.append(current_tok)
                check_nesting()
            return 'Next'
        else:
            return current_tok.position
    except KeyError:
        print("Syntax error: ", current_tok.lexeme)


# MAIN FUNC for AST
def node_creating(current_token, next_token):
    need_lvl = ast
    current_lvl = 0  # for symbol table
    # проход по namespace
    for construction in stack_nodes_hierarchy:
        for el_on_lvl in reversed(need_lvl["children"]):
            if el_on_lvl["kind"] == construction:
                current_lvl += 1
                need_lvl = el_on_lvl  # (dict)
                break

    # Describe all constructions
    create_node_function(current_token, next_token, need_lvl)
    create_node_call_func(current_token, next_token, need_lvl)
    create_node_for(current_token, next_token, need_lvl)
    create_node_assign(current_token, next_token, need_lvl)
    create_node_echo(current_token, next_token, need_lvl)

    craft_symbol_table(str(current_lvl), current_token, next_token, need_lvl)