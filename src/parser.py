from .ast_helper import *
from .symbol_table import *
from .assembly import displace
import copy

# общая таблица(общий случай), она дополняется вспомогательной для конструкций из помощника
parser_table = {
    'keyword_for': ['l_paren'],
    'keyword_while': ['l_paren'],
    'identifier_variable': ['operator_assignment', 'operator_sum', 'operator_substruction', 'operator_multiplication',
                            'operator_grater', 'operator_less', 'r_paren', 'semi', 'comma', 'operator_identical'],

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
    'operator_identical': ['numeric_constant', 'identifier_variable', 'string_literal'],
    'keyword_break': ['semi'],
    'identifier': ['l_paren'],
    'r_brace': ['None'],
    'operator_sum': ['numeric_constant', 'identifier_variable', 'string_literal'],
    'operator_substruction': ['numeric_constant', 'identifier_variable'],
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

            # This is`t implemented in assembler
            check_for(current_tok, next_tok)

            check_while(current_tok, next_tok)

            check_if(current_tok, next_tok)

            check_function(current_tok, next_tok)

            # This is`t implemented in assembler
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
    current_node = ast
    current_lvl = 0  # for symbol table
    test = None
    # проход по namespace
    for construction in stack_nodes_hierarchy:
        for el_on_lvl in reversed(current_node["children"]):
            if el_on_lvl["kind"] == construction:
                test = copy.deepcopy(current_node["children"])  #[e.copy() for e in current_node["children"]]
                current_lvl += 1
                current_node = el_on_lvl  # (dict)
                break

    # print(test, "HERE")
    # Describe all constructions
    create_node_function(current_token, next_token, current_node)
    create_node_call_func(current_token, next_token, current_node)
    create_node_for(current_token, next_token, current_node)
    create_node_assign(current_token, next_token, current_node, test)
    create_node_echo(current_token, next_token, current_node)
    create_node_if(current_token, next_token, current_node, test)
    create_node_while(current_token, next_token, current_node)

    # The function will see if the variable has been defined in the correct scope based on the symbol table..
    arrange_variables_in_memory(current_node, current_lvl, current_token, next_token)

    # ..so the update comes after
    craft_symbol_table(str(current_lvl), current_token, next_token)


def arrange_variables_in_memory(current_node, current_lvl, current_token, next_token):
    global displace

    if current_token.token_type == 'identifier_variable' and next_token.token_type == 'operator_assignment':
        if not find_var_above(symbol_table, current_token, current_lvl):
            # special case of variable search function, vars in global scope
            if current_token.lexeme not in cut_type_var(list(symbol_table["0:0"])):
                displace += 4
                print(displace, current_token.lexeme)

        current_node['children'][-1]["displace"] = find_displace_for_var(current_token)


def find_displace_for_var(current_token):
    global displace
    finder_displace = None  # displace variable
    flag = False
    children = ast["children"]
    print(children)
    for temp in children:
        if temp.get("left") == current_token.lexeme:
            if temp.get("displace") is None:
                temp["displace"] = displace
            finder_displace = temp["displace"]
            flag = True
            break
    parent = children[-1]["parent"]
    # print(parent)
    while parent is not None and flag is False:
        for temp in parent:
            # print(temp, current_token.lexeme)
            if temp.get("left") == current_token.lexeme:
                finder_displace = temp["displace"]
                flag = True
                break
        parent = parent[-1]["parent"]

    return finder_displace