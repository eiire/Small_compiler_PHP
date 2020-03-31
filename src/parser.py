from src.lexer import Token

parser_table = {
    'keyword_for': ['l_paren'],
    'identifier_variable': ['operator_assignment', 'operator_sum', 'operator_grater', 'operator_less', 'r_paren', 'semi'],
    'l_paren': ['semi', 'identifier_variable', 'string_literal', 'identifier_variable'],
    'operator_less': ['numeric_constant', 'identifier_variable'],
    'keyword_if': ['l_paren'],
    'identifier': ['operator_assignment', 'semi', 'operator_sum', 'identifier_variable'],
    'semi': ['None', 'keyword_for', 'semi', 'r_paren', 'numeric_constant', 'identifier_variable'],
    'numeric_constant': ['semi', 'r_paren', 'l_brace'],
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
}

nesting_stack = []

constructions = {'keyword_for': [['identifier_variable', 'operator_assignment', 'numeric_constant'],
                                 ['r_paren', 'l_paren', 'operator_grater', 'operator_less', 'identifier_variable',
                                  'numeric_constant'],
                                 ['identifier_variable', 'operator_assignment', 'operator_sum', 'numeric_constant']],
                 'keyword_if': ['r_paren', 'l_paren', 'operator_grater', 'operator_less', 'identifier_variable',
                                'numeric_constant']
                 }

ast = {
    "kind": "program",
    "children": [
        # array of nodes
    ]
}

stack_nodes_hierarchy = ['program']
keyword_construction = Token('None', 'None', 0)  # расширить стеком


# ----->MAIN FUNC for AST<------
def node_creating(current_token, next_token, keyword_construction):
    need_lvl = ast

    for construction in stack_nodes_hierarchy:
        for el_on_lvl in reversed(need_lvl["children"]):
            if el_on_lvl["kind"] == construction: #  BODY
                need_lvl = el_on_lvl
                break

    # Describe all constructions
    if keyword_construction.token_type == 'keyword_for':
        if current_token.token_type == 'keyword_for' and keyword_construction.token_type == 'keyword_for' \
                and current_token.lexeme != '{' and current_token.lexeme != '}':
            need_lvl["children"].append({"kind": current_token.token_type,
                                         "init": "",
                                         "test": "",
                                         "increment": "",
                                         "position": current_token.position,
                                         "children": []
                                         })
        elif keyword_construction.token_type == 'keyword_for' and keyword_construction.position == 0:
            if current_token.lexeme != '(' and current_token.lexeme != ';' and current_token.lexeme != ')':
                need_lvl["init"] = need_lvl["init"] + current_token.lexeme + ' '
        elif keyword_construction.token_type == 'keyword_for' and keyword_construction.position == 1:
            if current_token.lexeme != '(' and current_token.lexeme != ';' and current_token.lexeme != ')':
                need_lvl["test"] = need_lvl["test"] + current_token.lexeme + ' '
        elif keyword_construction.token_type == 'keyword_for' and keyword_construction.position == 2:
            if current_token.lexeme != '(' and current_token.lexeme != ';' and current_token.lexeme != ')':
                need_lvl["increment"] = need_lvl["increment"] + current_token.lexeme + ' '

    if keyword_construction.token_type == 'assign' and keyword_construction.position == 0 \
            and current_token.lexeme != '{' and current_token.lexeme != '}':
        need_lvl["children"].append({"kind": keyword_construction.token_type,
                                     "left": current_token.lexeme,
                                     "right": "",
                                     "position": keyword_construction.position,
                                     })
    elif keyword_construction.token_type == 'assign' and keyword_construction.position == 1 \
            and current_token.lexeme != '=':
        need_lvl["children"][-1]["right"] = need_lvl["children"][-1]["right"] + current_token.lexeme + ' '


current_lvl = ast


def parsing(current_tok, next_tok):
    # print(current_tok.lexeme, next_tok.lexeme)
    try:
        if next_tok.token_type in parser_table[current_tok.token_type]:
            #block_php
            if current_tok.position == "1:0" and current_tok.token_type == 'keyword_<?php':
                return 'Next'
            elif current_tok.position != "1:0" and current_tok.token_type == 'keyword_<?php':
                return current_tok.position

            check_for(current_tok, next_tok)

            check_instruction(current_tok, next_tok)

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
        print("Non-existent: ", current_tok.lexeme, current_tok.position)


# general case (если конструкция не определена, значит конструкция - инструкция)
def check_instruction(current_tok, next_tok):
    if keyword_construction.token_type == 'None' or keyword_construction.token_type == 'assign':
        keyword_construction.token_type = 'assign'

        # left and right part instruction
        if current_tok.lexeme == '=' or current_tok.lexeme == '<' or current_tok.lexeme == '>':
            keyword_construction.position += 1

        if current_tok.token_type == 'semi':
            keyword_construction.token_type = 'None'
            keyword_construction.position = 0

        node_creating(current_tok, next_tok, keyword_construction)


def check_for(current_tok, next_tok):
    if current_tok.token_type == 'keyword_for' or keyword_construction.token_type == 'keyword_for':
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

        # if current_tok.token_type in constructions[keyword_construction.token_type][keyword_construction.position]:
        #     print(current_tok.lexeme, next_tok.lexeme)
        #     # return current_tok.position

        if check_construction(current_tok, next_tok, keyword_construction) == -1:
            return current_tok.position
        elif check_construction(current_tok, next_tok, keyword_construction) == 'End_construction':
            keyword_construction.token_type = 'None'
            keyword_construction.position = 0

        node_creating(current_tok, next_tok, keyword_construction)

        return 1

    return 0


def check_construction(curent_tok,  next_tok, keyword_construction):
    if curent_tok.token_type in constructions[keyword_construction.token_type]:
        return 'Next'
    elif (curent_tok.lexeme == ';' and next_tok.token_type == 'None') or curent_tok.lexeme == '{':
        return 'End_construction'


count_paren = 0
count_brace = 0


def check_nesting():
    pass


# ['(']
# ['(', ')']
# ['(', ')', '{']
# ['(', ')', '{', '(']
# ['(', ')', '{', '(', ')']
# ['(', ')', '{', '(', ')', '{']
# ['(', ')', '{', '(', ')', '{', '}']
# ['(', ')', '{', '(', ')', '{', '}', '}']

#block if
# if current_tok.token_type == 'keyword_if' or keyword_construction.token_type == 'keyword_if':
#     keyword_construction.token_type = 'keyword_if'
#     if check_construction(current_tok, next_tok, keyword_construction) == -1:
#         return current_tok.position
#     elif check_construction(current_tok, next_tok, keyword_construction) == 'End_construction':
#         # print(keyword_construction.token_type, keyword_construction.position)
#         keyword_construction.token_type = 'None'
#         keyword_construction.position = 0
#endif
