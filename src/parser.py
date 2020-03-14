parser_table = {
    'keyword_for': ['l_paren'],
    'identifier_variable': ['operator_assignment', 'operator_sum', 'operator_grater', 'r_paren', 'semi'],
    'l_paren': ['semi', 'identifier_variable', 'string_literal'],
    'operator_less': ['numeric_constant', 'identifier_variable'],
    'keyword_if': ['l_paren'],
    'identifier': ['operator_assignment', 'semi', 'operator_sum', 'identifier_variable'],
    'semi': ['None', 'keyword_for', 'semi', 'r_paren'],  # if str end --> None, else --> next_tok may be same tok(example 'for')
    'numeric_constant': ['semi', 'r_paren', 'l_brace'],
    'keyword_<?php': ['None'],
    'operator_assignment': ['numeric_constant', 'identifier_variable'],
    'r_paren': ['l_brace', 'r_brace'],
    'l_brace': ['None', 'identifier'],
    'operator_grater': ['numeric_constant'],
    'keyword_break': ['semi'],
    'r_brace': ['None'],
    'operator_sum': ['numeric_constant', 'identifier_variables'],
    'keyword_?>': ['None'],
    'operator_multiplication': ['identifier_variables', 'constant_numeric'],
}

nesting_stack = []


def parsing(current_tok, next_tok):
    if next_tok.token_type in parser_table[current_tok.token_type]:
        if current_tok.lexeme == '(' or current_tok.lexeme == ')' \
                or current_tok.lexeme == '{' or current_tok.lexeme == '}':
            nesting_stack.append(current_tok.lexeme)
            # print(nesting_stack)
            check_nesting(nesting_stack)
        return 'Next'
    else:
        return current_tok.position


def check_nesting(nesting_stack):
    # count_paren = 0
    # count_brace = 0
    # for i in range(len(nesting_stack)):
    #     if nesting_stack[i] == '(':
    #         count_paren += 1
    pass
# ['(']
# ['(', ')']
# ['(', ')', '{']
# ['(', ')', '{', '(']
# ['(', ')', '{', '(', ')']
# ['(', ')', '{', '(', ')', '{']
# ['(', ')', '{', '(', ')', '{', '}']
# ['(', ')', '{', '(', ')', '{', '}', '}']