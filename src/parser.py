from src.lexer import Token


parser_table = {
    'keyword_for': ['l_paren'],
    'identifier_variable': ['operator_assignment', 'operator_sum', 'operator_grater', 'operator_less', 'r_paren', 'semi'],
    'l_paren': ['semi', 'identifier_variable', 'string_literal', 'identifier_variable'],
    'operator_less': ['numeric_constant', 'identifier_variable'],
    'keyword_if': ['l_paren'],
    'identifier': ['operator_assignment', 'semi', 'operator_sum', 'identifier_variable'],
    'semi': ['None', 'keyword_for', 'semi', 'r_paren', 'numeric_constant', 'identifier_variable'],
    # if str end --> None, else --> next_tok may be same tok(example 'for')
    'numeric_constant': ['semi', 'r_paren', 'l_brace'],
    'keyword_<?php': ['None'],
    'operator_assignment': ['numeric_constant', 'identifier_variable'],
    'r_paren': ['semi', 'l_brace', 'r_brace'],
    'l_brace': ['None', 'identifier'],
    'operator_grater': ['numeric_constant'],
    'keyword_break': ['semi'],
    'r_brace': ['None'],
    'operator_sum': ['numeric_constant', 'identifier_variables'],
    'keyword_?>': ['None'],
    'operator_multiplication': ['identifier_variables', 'constant_numeric'],
}

nesting_stack = []

constructions = {'keyword_for': [['identifier_variable', 'operator_assignment', 'numeric_constant'],
                                 ['r_paren', 'l_paren', 'operator_grater', 'operator_less', 'identifier_variable',
                                  'numeric_constant'],
                                 ['identifier_variable', 'operator_assignment', 'operator_sum', 'numeric_constant']],
                 'keyword_if': ['r_paren', 'l_paren', 'operator_grater', 'operator_less', 'identifier_variable',
                                'numeric_constant']
                 }


stack_nodes_hierarchy = ['program']
keyword_construction = Token('None', 'None', 0)  # расширить стеком


ast = {
    "kind": "program",
    "children": [
        # array of nodes
    ]
}


def node_creating(token):
    need_lvl = ast
    stack = stack_nodes_hierarchy
    print(need_lvl)
    print(stack)
    for construction in stack_nodes_hierarchy: # ----->MAIN FUNC<------
        # print(construction)
        for el_on_lvl in reversed(need_lvl["children"]):
            if el_on_lvl["kind"] == construction: #  BODY
                need_lvl = el_on_lvl
                break

    # Describe all constructions
    if token.token_type == 'keyword_for':
        need_lvl["children"].append({"kind": token.token_type,
                                     "init": "",
                                     "test": "",
                                     "increment": "",
                                     "position": token.position,
                                     "children": []
                                     })

    if token.token_type == 'exp':
        need_lvl["children"].append({"kind": token.token_type,
                                     "position": token.position,
                                     })


current_lvl = ast

#
# def search_lvl():
#     lvl = 0
#     for el in nesting_stack:
#         if el == '{':
#             lvl += 1
#         if el == '}':
#             lvl -= 1
#     return lvl


def parsing(current_tok, next_tok):
    global ast
    global prev_lvl
    str_exp = ""
    if next_tok.token_type in parser_table[current_tok.token_type]:
        #block_php
        if current_tok.position == "0:0" and current_tok.token_type == 'keyword_<?php':
            return 'Next'
        #endblock

        #block for
        if current_tok.token_type == 'keyword_for' or keyword_construction.token_type == 'keyword_for':
            # prev_lvl = search_lvl(stack_nodes_hierarchy, ast)
            node_creating(current_tok)

            keyword_construction.token_type = 'keyword_for'
            if current_tok.token_type == 'keyword_for':
                stack_nodes_hierarchy.append(keyword_construction.token_type)  # LVL

            if current_tok.lexeme == ';':
                keyword_construction.position += 1
                if (keyword_construction.position == 2 or 1 or 0) and next_tok.position == 'end_str':
                    return current_tok.position
                # tree insert

            if keyword_construction.position != 2 and check_construction(current_tok, next_tok, keyword_construction) \
                    == 'End_construction':
                return current_tok.position

            if current_tok.token_type in constructions[keyword_construction.token_type][keyword_construction.position] \
                    == False:
                return current_tok.position

            if check_construction(current_tok, next_tok, keyword_construction) == -1:
                return current_tok.position
            elif check_construction(current_tok, next_tok, keyword_construction) == 'End_construction':
                keyword_construction.token_type = 'None'
                keyword_construction.position = 0

        #block exp
        # print(current_tok.lexeme, next_tok.lexeme)
        if current_tok.token_type == 'identifier_variable' and next_tok.token_type == 'operator_assignment' and \
                keyword_construction.token_type != 'keyword_for':
            keyword_construction.token_type = 'exp'
            node_creating(keyword_construction)

            if current_tok.token_type == 'semi':
                keyword_construction.token_type = 'None'
        #endblock

        if current_tok.lexeme == '}':
            stack_nodes_hierarchy.pop()
        #endfor

        # if current_tok.token_type == 'keyword_if' or keyword_construction.token_type == 'keyword_if':
        #     keyword_construction.token_type = 'keyword_if'
        #     if check_construction(current_tok, next_tok, keyword_construction) == -1:
        #         return current_tok.position
        #     elif check_construction(current_tok, next_tok, keyword_construction) == 'End_construction':
        #         # print(keyword_construction.token_type, keyword_construction.position)
        #         keyword_construction.token_type = 'None'
        #         keyword_construction.position = 0



        if current_tok.lexeme == '(' or current_tok.lexeme == ')' \
                or current_tok.lexeme == '{' or current_tok.lexeme == '}':
            nesting_stack.append(current_tok.lexeme)
            print(nesting_stack) # <---
            check_nesting()
        return 'Next'
    else:
        print(current_tok.lexeme)
        return current_tok.position


def check_construction(curent_tok,  next_tok, keyword_construction):
    if curent_tok.token_type in constructions[keyword_construction.token_type]:
        return 'Next'
    elif (curent_tok.lexeme == ';' and next_tok.token_type == 'None') or curent_tok.lexeme == '{':
        return 'End_construction'


count_paren = 0
count_brace = 0


def check_nesting():
    global count_paren
    global count_brace
    for i in range(len(nesting_stack)):
        if nesting_stack[i] == '(':
            count_paren += 1

        if nesting_stack[i] == '{':
            count_brace += 1
            if count_paren != 0: return -1

        if nesting_stack[i] == ')':
            count_paren -= 1
            if count_paren == -1: return -1

        if nesting_stack[i] == '}':
            count_brace -= 1
            if count_brace == -1: return -1


def build_parse_tree():
    pass

# ['(']
# ['(', ')']
# ['(', ')', '{']
# ['(', ')', '{', '(']
# ['(', ')', '{', '(', ')']
# ['(', ')', '{', '(', ')', '{']
# ['(', ')', '{', '(', ')', '{', '}']
# ['(', ')', '{', '(', ')', '{', '}', '}']
