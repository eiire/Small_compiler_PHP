from .parser_helper import *


# Describe all constructions
def create_node_for(current_token, next_token, need_lvl, cur_grandpa_childs):
    if current_construction.token_type == 'keyword_for':
        if current_token.token_type == 'keyword_for' and current_construction.token_type == 'keyword_for':
            need_lvl["childs"].append({"kind": current_token.token_type,
                                       "init": "",
                                       "test": "",
                                       "increment": "",
                                       "position": current_token.position,
                                       "childs": [],
                                       "cur_grandpa_childs": cur_grandpa_childs
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


def create_node_if(current_token, next_token, need_lvl, cur_grandpa_childs):
    if current_construction.token_type == 'keyword_if':
        if current_token.token_type == 'keyword_if' and current_construction.token_type == 'keyword_if':
            need_lvl["childs"].append({"kind": current_token.token_type,
                                       "condition": {},
                                       "position": current_token.position,
                                       "childs": [],
                                       "cur_grandpa_childs": cur_grandpa_childs
                                       })

        if current_token.token_type in ['identifier_variable', 'numeric_constant'] and next_token.token_type \
                in ['operator_identical', 'operator_less', 'operator_grater', 'operator_noteq']:
            need_lvl["condition"]["left"] = current_token.lexeme
            need_lvl["condition"]["op"] = next_token.lexeme

        if next_token.token_type in ['identifier_variable', 'numeric_constant'] and current_token.token_type \
                in ['operator_identical', 'operator_less', 'operator_grater', 'operator_noteq']:
            need_lvl["condition"]["right"] = next_token.lexeme


def create_node_while(current_token, next_token, need_lvl, cur_grandpa_childs):
    if current_construction.token_type == 'keyword_while':
        if current_token.token_type == 'keyword_while' and current_construction.token_type == 'keyword_while':
            need_lvl["childs"].append({"kind": current_token.token_type,
                                       "condition": {},
                                       "position": current_token.position,
                                       "childs": [],
                                       "cur_grandpa_childs": cur_grandpa_childs,
                                       })

        if current_token.token_type in ['identifier_variable', 'numeric_constant'] and next_token.token_type \
                in ['operator_identical', 'operator_less', 'operator_grater', 'operator_noteq']:
            need_lvl["condition"]["left"] = current_token.lexeme
            need_lvl["condition"]["op"] = next_token.lexeme

        if next_token.token_type in ['identifier_variable', 'numeric_constant'] and current_token.token_type \
                in ['operator_identical', 'operator_less', 'operator_grater', 'operator_noteq']:
            need_lvl["condition"]["right"] = next_token.lexeme


def create_node_function(current_token, next_token, need_lvl, cur_grandpa_childs):
    if current_construction.token_type == 'keyword_function':
        if current_token.token_type == 'keyword_function' and current_construction.token_type == 'keyword_function':
            need_lvl["childs"].append({"kind": current_token.token_type,
                                       "name": next_token.lexeme,
                                       "args": "",
                                       "childs": [],
                                       "cur_grandpa_childs": []
                                       })
        elif current_token.token_type != 'keyword_function' and current_construction.token_type == 'keyword_function' \
                and current_token.token_type != 'l_paren' \
                and current_token.token_type != 'r_paren' \
                and current_token.token_type != 'comma' \
                and current_token.token_type != 'identifier':
            need_lvl["args"] = need_lvl["args"] + current_token.lexeme + ' '


def create_node_call_func(current_token, next_token, need_lvl, cur_grandpa_childs):
    if current_construction.token_type == 'call_func':
        if current_token.token_type == 'identifier' and current_construction.token_type == 'call_func':
            need_lvl["childs"].append({"kind": current_token.token_type,
                                       "name": current_token.lexeme,
                                       "args": "",
                                       "cur_grandpa_childs": []
                                       })
        elif current_token.token_type != 'identifier' and current_construction.token_type == 'call_func' \
                and current_token.token_type != 'l_paren' \
                and current_token.token_type != 'r_paren' \
                and current_token.token_type != 'comma' \
                and current_token.token_type != 'identifier':
            need_lvl["childs"][-1]["args"] = need_lvl["childs"][-1]["args"] + current_token.lexeme + ' '


is_assign_expression = False


def create_node_assign(current_token, next_token, need_lvl, cur_grandpa_childs):
    global is_assign_expression
    if current_token.lexeme == ';':
        is_assign_expression = False

    if current_construction.token_type == 'assign' and current_construction.position == 0:
        need_lvl["childs"].append({"kind": current_construction.token_type,
                                   "left": current_token.lexeme,
                                   "right": "",
                                   "position": current_token.position,
                                   "cur_grandpa_childs": cur_grandpa_childs
                                   })
    elif current_construction.token_type == 'assign' and current_construction.position == 1 \
            and current_token.lexeme != '=':

        if (current_token.token_type == 'numeric_constant' or current_token.token_type == 'identifier_variable') \
                and (next_token.token_type == 'operator_sum'
                     or next_token.token_type == 'operator_substruction'
                     or next_token.token_type == 'operator_multiplication'
                     or next_token.token_type == 'operator_division'
                     or next_token.token_type == 'operator_mod'):
            is_assign_expression = True
            need_lvl["childs"][-1]["kind"] = "assign_expression"
            need_lvl["childs"][-1]["right"] = {
                "kind": next_token.token_type,
                "left": current_token.lexeme,
                "right": None
            }

        if (current_token.token_type == 'operator_sum'
            or current_token.token_type == 'operator_substruction'
            or current_token.token_type == 'operator_multiplication'
            or current_token.token_type == 'operator_division'
            or current_token.token_type == 'operator_mod') \
                and (next_token.token_type == 'numeric_constant' or next_token.token_type == 'identifier_variable') \
                and need_lvl["childs"][-1]["right"]["right"] is None:
            need_lvl["childs"][-1]["right"]["right"] = next_token.lexeme

        if not is_assign_expression:
            need_lvl["childs"][-1]["right"] = need_lvl["childs"][-1]["right"] + current_token.lexeme + ' '


def create_node_echo(current_token, next_token, need_lvl, cur_grandpa_childs):
    if current_token.token_type == 'keyword_echo':
        need_lvl["childs"].append({
            "kind": current_token.token_type,
            "position": current_token.position,
            "elements": "",
            "cur_grandpa_childs": cur_grandpa_childs
        })
    elif current_construction.token_type == 'keyword_echo' and current_token.token_type != 'keyword_echo' \
            and current_token.token_type != 'comma':
        need_lvl["childs"][-1]["elements"] += current_token.lexeme + ' '


def create_break(current_token, next_token, need_lvl, cur_grandpa_childs):
    if current_token.token_type == 'keyword_break':
        need_lvl["childs"].append({
            "kind": current_token.token_type,
        })
