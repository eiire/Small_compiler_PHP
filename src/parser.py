from .parser_helper import *
from .ast_helper import *
from src.symbol_table import *

# общая таблица(общий случай), она дополняется вспомогательной для конструкций из помощника
parser_table = {
    'keyword_for': ['l_paren'],
    'identifier_variable': ['operator_assignment', 'operator_sum', 'operator_substruction' 'operator_grater', 'operator_less', 'r_paren', 'semi'],
    'l_paren': ['semi', 'identifier_variable', 'string_literal', 'identifier_variable'],
    'operator_less': ['numeric_constant', 'identifier_variable'],
    'keyword_if': ['l_paren'],
    'identifier': ['operator_assignment', 'semi', 'operator_sum', 'identifier_variable'],
    'semi': ['None', 'keyword_for', 'semi', 'r_paren', 'numeric_constant', 'identifier_variable'],
    'numeric_constant': ['semi', 'r_paren'],
    'keyword_<?php': ['None'],
    'operator_assignment': ['numeric_constant', 'identifier_variable'],
    'r_paren': ['semi', 'l_brace', 'r_brace'],
    'l_brace': ['None', 'identifier', 'identifier_variable'],
    'operator_grater': ['numeric_constant'],
    'keyword_break': ['semi'],
    'r_brace': ['None'],
    'operator_sum': ['numeric_constant', 'identifier_variables'],
    'keyword_?>': ['None'],
    'operator_multiplication': ['identifier_variables', 'constant_numeric'],
    'keyword_function': ['identifier'],
}

ast = {
    "kind": "program",
    "children": [
        # array of nodes
    ]
}

# Парсер использует current_costruction из parser_helper для для поддержания вложенностей и определения, что проверяется
stack_nodes_hierarchy = ['program'] # контроль вложенностей


def parsing(current_tok, next_tok):
    # print(current_tok.lexeme, next_tok.lexeme, current_construction.token_type) # DEBUGGER)
    try:
        if next_tok.token_type in parser_table[current_tok.token_type]:
            # print(current_tok.lexeme, next_tok.lexeme, current_construction.token_type) # DEBUGGER)

            # dangerous (в php все конструкции, имеющие вложенность, имеют и открывающую скобку => должно работать)
            if current_tok.lexeme == '(':
                stack_nodes_hierarchy.append(current_construction.token_type)

            check_php(current_tok)

            check_for(current_tok, next_tok)

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


# ----->MAIN FUNC for AST<------ next_token понадобится для дальнейшего расширения языка
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

    craft_symbol_table(str(current_lvl), current_token)
    # Describe all constructions
    create_node_for(current_token, next_token, need_lvl)
    create_node_assign(current_token, next_token, need_lvl)