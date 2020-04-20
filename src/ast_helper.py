from .parser_helper import *


# Describe all constructions
def create_node_for(current_token, next_token, need_lvl):
    if current_construction.token_type == 'keyword_for':
        if current_token.token_type == 'keyword_for' and current_construction.token_type == 'keyword_for':
            need_lvl["children"].append({"kind": current_token.token_type,
                                         "init": "",
                                         "test": "",
                                         "increment": "",
                                         "position": current_token.position,
                                         "children": []
                                         })
        elif current_construction.token_type == 'keyword_for' and current_construction.position == 0:
            if current_token.lexeme != '(' and current_token.lexeme != ';' and current_token.lexeme != ')':
                need_lvl["init"] = need_lvl["init"] + current_token.lexeme + ' '
        elif current_construction.token_type == 'keyword_for' and current_construction.position == 1:
            if current_token.lexeme != '(' and current_token.lexeme != ';' and current_token.lexeme != ')':
                need_lvl["test"] = need_lvl["test"] + current_token.lexeme + ' '
        elif current_construction.token_type == 'keyword_for' and current_construction.position == 2:
            if current_token.lexeme != '(' and current_token.lexeme != ';' and current_token.lexeme != ')':
                need_lvl["increment"] = need_lvl["increment"] + current_token.lexeme + ' '


def create_node_assign(current_token, next_token, need_lvl):
    if current_construction.token_type == 'assign' and current_construction.position == 0:
        need_lvl["children"].append({"kind": current_construction.token_type,
                                     "left": current_token.lexeme,
                                     "right": "",
                                     "position": current_token.position,
                                     })
    elif current_construction.token_type == 'assign' and current_construction.position == 1 \
            and current_token.lexeme != '=':
        need_lvl["children"][-1]["right"] = need_lvl["children"][-1]["right"] + current_token.lexeme + ' '


def create_node_echo(current_token, next_token, need_lvl):
    if current_token.token_type == 'keyword_echo':
        need_lvl["children"].append({
            "kind": current_token.token_type,
            "position": current_token.position,
            "elements": ""
        })
    elif current_construction.token_type == 'keyword_echo' and current_token.token_type != 'keyword_echo' \
            and current_token.token_type != 'l_paren' and current_token.token_type != 'r_paren'\
            and current_token.token_type != 'dot':
        need_lvl["children"][-1]["elements"] += current_token.lexeme + ' '
