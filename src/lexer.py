import re


class Token:
    def __init__(self, lexeme, token_type, position):
        self.lexeme = lexeme
        self.token_type = token_type
        self.position = position


def tokens_in_line(line, line_number):  # Generator line`s tokens
    new_line_tokens = []
    str_for_pos = line

    #  Cut: grg"entity"grg --> grggrg
    new_tok_slit = re.findall('["].+["]', line)
    new_line_tokens += new_tok_slit
    new_line = re.sub('["].+["]', ' ', line)
    line = new_line

    for word in line.split():  # --> create_list
        #  for "example example"
        new_line_tokens += my_str_split(word).split()  # str in list new_line_tokens =
    for word in new_line_tokens:  # ' '.join(new_line_tokens) # back to str
        res_check = check_family_token(word)
        tok = Token(word, res_check, str(line_number) + ":" + str(pos_tok_in_line(str_for_pos, word)))  # Create one tok

        yield tok  # Create generator`s from same tok


def check_thist_heshteg_after_cov(line):
    i = 0
    h = 0  # count cov
    for ch in line:
        i += 1
        if ch.find('"') != -1:
            h += 1
        elif ch == '#' and h % 2 == 0:  # need that break after last # , but no thirst
            break
    return i


def my_str_split(word):  # work with str
    part_res = ""
    fl = 0
    # print(word)
    # check for str_literal --> code <-- !!! "efef#gf""ewet)r#rr"#hhh

    # if ((token.find('"', len(token) - 1)) == (len(token) - 1) and token.find('"') == 0): return 'string_literal'
    # if ((word.find('"', len(word) - 1)) == (len(word) - 1) and token.find('"') != 0) or \
    #         ((token.find('"', len(token) - 1)) != (len(token) - 1) and token.find('"') == 0):
    # print(word)
    for ch in word:  # range(word)
        # if word.find("==") != -1: #  upper other code because flag may be rewrite <----TASK
        #     fl = 1

        if ch == ')' or ch == '}' or ch == ';' or ch == ':' or ch == '(' or ch == '{' or ch == '+' \
                or ch == '-' or ch == '[' or ch == ']' or ch == ',' \
                or (ch == '<' and word.lower().find('<?php') == -1) \
                or (ch == '>' and word.find('?>') == -1) \
                or (ch == '=' and (word.find('==') == -1 and word.find('===') == -1 and word.find('!=') == -1)):
            fl = 2  # or ch == '"'
        elif ch == '$':
            fl = 1

        if fl == 0:
            part_res += ch
            fl = 0
        elif fl == 2:
            part_res = part_res + ' ' + ch + ' '
            fl = 0
        else:
            part_res = part_res + ' ' + ch
            fl = 0  # print(part_res) put space only befor symbol/-->worked for PHP<--/ may be bug
    return part_res


def pos_tok_in_line(str_for_pos, word):
    return str_for_pos.find(word)


def check_family_token(token):
    # defined language
    if token == '{': return 'l_brace'
    if token == ';': return 'semi'
    if token == '}': return 'r_brace'
    if token == 'break': return 'keyword_break'
    if token == '(': return 'l_paren'
    if token == ')': return 'r_paren'
    if token == '-': return 'operator_substruction'
    if token == '+': return 'operator_sum'
    if token == ',': return 'comma'
    if token == '*': return 'operator_multiplication'
    if token == '/': return 'operator_division'
    if token == '%': return 'operator_mod'
    if token == '<': return 'operator_less'
    if token == '>': return 'operator_grater'
    if token == '=': return 'operator_assignment'
    # if token == '"': return 'Literal'
    if token == '++': return 'operator_increment'
    if token == '!=': return 'operator_noteq'
    if token == '--': return 'operator_decrement'
    if token == '===': return 'operator_identical'
    if token.lower() == 'class': return 'keyword_class'
    if token.lower() == 'use': return 'keyword_use'
    if token.lower() == 'namespace': return 'keyword_namespace'
    if token.lower() == 'if': return 'keyword_if'
    if token.lower() == 'for': return 'keyword_for'
    if token.lower() == 'main': return 'identifier'
    if token.lower() == 'while': return 'keyword_while'
    if token.lower() == 'function': return 'keyword_function'
    if token.lower() == '<?php': return 'keyword_<?php'
    if token == '?>': return 'keyword_?>'
    if token.lower() == 'int': return 'int'
    if token.lower() == 'echo': return 'identifier'
    if token.lower() == 'return': return 'keyword_return'
    if token.find('$') != -1 and token.find('$') == 0:  # check for normal variable
        check_correct = re.search('[a-zA-Z_\x7f-\xff][a-zA-Z0-9_\x7f-\xff]*', token[1:])
        if check_correct.group() == token[1:]:
            return 'identifier_variable'
        else:
            return 'unknown'

    # check numeric_constant_OCT&simple
    if token.isdigit() and token.find('0') == 0:
        if token.find('8') != -1 or token.find('9') != -1:
            return 'unknown'
        return 'numeric_constant_oct'

    if token.isdigit(): return 'numeric_constant'

    # check str_lit
    if ((token.find('"', len(token) - 1)) == (len(token) - 1) and token.find('"') != 0): return 'unknown'
    if ((token.find('"', len(token) - 1)) != (len(token) - 1) and token.find('"') == 0): return 'unknown'
    if ((token.find('"', len(token) - 1)) == (len(token) - 1) and token.find('"') == 0): return 'string_literal'

    # check num_const_HEX&BIN
    if token.find('0', 0) != -1 and token.find('x', 1) != -1:
        check_correct = re.search('[a-zA-Z_\x7f-\xff][a-zA-Z0-9_\x7f-\xff]*', token[1:])
        if check_correct.group() == token[1:]:
            return 'numeric_constant_hex'
        else:
            return 'unknown'

    if token.find('0', 0) != -1 and token.find('b', 1) != -1:
        check_correct = re.search('[a-zA-Z_\x7f-\xff][a-zA-Z0-1_\x7f-\xff]*', token[1:])
        if check_correct.group() == token[1:]:
            return 'numeric_constant_binary'
        else:
            return 'unknown'

    # check for in correct tok
    check_correct = re.match("[a-zA-Z_\x7f-\xff][a-zA-Z0-9_\x7f-\xff]*", token)  # check incorrect characters
    if check_correct is None:  # mey be None object
        return 'unknown'
    else:
        if check_correct.group() == token:
            return 'identifier'
        else:
            return 'unknown'
