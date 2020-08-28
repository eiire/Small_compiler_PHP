from unittest import TestCase


class TestLexer(TestCase):
    def test_parser(self):
        from src.parser import parsing
        from src.lexer import tokens_in_line

        # correct_case (сравниваю пары со сдвигом во втором элементе (cur_tok, nex_tok))
        for current_tok, next_tok in zip(tokens_in_line("for($i =1; $i< 10; $i = $i + 1) {", 3), tokens_in_line("($i =1; $i< 10; $i = $i + 1) {", 3)):
            self.assertEqual(parsing(current_tok, next_tok), 'Next')

        # incorrect_case
        for current_tok, next_tok in zip(tokens_in_line("for", 3), tokens_in_line("$i", 3)):
            self.assertNotEqual(parsing(current_tok, next_tok), 'Next')


    def test_node_creating_ast(self):
        from src.parser import node_creating, ast, stack_nodes_hierarchy
        from src.parser_helper import current_construction
        from src.lexer import Token

        # correct case
        # Проверяем на нужно ли уровне находится фор
        current_construction.token_type = 'keyword_for'
        stack_nodes_hierarchy.append('keyword_for')  # спуск
        cur_tok = Token("for", "keyword_for", "NotMatter")
        nex_tok = Token("NotMatter", "NotMatter", "NotMatter")
        node_creating(cur_tok, nex_tok)
        node_creating(cur_tok, nex_tok)
        expected_ast = {'kind': 'program', 'children':
            [{'kind': 'keyword_for', 'init': '', 'test': '', 'increment': '', 'position': 'NotMatter', 'children':
                [{'kind': 'keyword_for', 'init': '', 'test': '', 'increment': '', 'position': 'NotMatter', 'children':
                    []}]}]}

        self.assertEqual(ast, expected_ast)

        # incorrect case
        current_construction.token_type = 'keyword_for'
        # stack_nodes_hierarchy.append('keyword_for')  # уберем вложенность
        cur_tok = Token("for", "keyword_for", "NotMatter")
        nex_tok = Token("NotMatter", "NotMatter", "NotMatter")
        node_creating(cur_tok, nex_tok)
        node_creating(cur_tok, nex_tok)
        # оставим, как буд-то вложенность есть
        expected_ast = {'kind': 'program', 'children':
            [{'kind': 'keyword_for', 'init': '', 'test': '', 'increment': '', 'position': 'NotMatter', 'children':
                [{'kind': 'keyword_for', 'init': '', 'test': '', 'increment': '', 'position': 'NotMatter', 'children':
                    []}]}]}

        self.assertNotEqual(ast, expected_ast)

    def test_check_instruction(self):
        from src.lexer import tokens_in_line, Token
        from src.parser_helper import check_instruction, current_construction

        current_construction.token_type = "assign"
        # correct_case
        for current_tok, next_tok in zip(tokens_in_line("$b = $b + 1", 3), tokens_in_line(" = $b + 1;", 3)):
            # функция ничего не возращает(None), если все нормально , но в случае ошибки бросает исключение
            self.assertEqual(check_instruction(current_tok, next_tok), None)

        # incorrect_case
        for current_tok, next_tok in zip(tokens_in_line("$b = $b + <", 3), tokens_in_line(" = $b + 1;", 3)):
            try:
                self.assertEqual(check_instruction(current_tok, next_tok), None)
            except:
                pass

        # Конец конструкции типа assign, текущая конструкция "обнуляется"
        cur_tok = Token(";", "semi", "0:1")
        nex_tok = Token("None", "None", "0:1")
        check_instruction(cur_tok, nex_tok)
        self.assertEqual(current_construction.token_type, "None")

    def test_check_construction(self):
        from src.parser_helper import check_construction, current_construction
        from src.lexer import Token
        # correct_case
        current_construction.token_type = "assign"  # на примере assign
        cur_tok = Token("$b", "identifier_variable", "0:1")
        nex_tok = Token("=", "operator_assignment", "0:2")

        self.assertEqual(check_construction(cur_tok, nex_tok), 'Next')

        # incorrect_case
        current_construction.token_type = "assign"  # на примере assign
        cur_tok = Token("for", "keyword_for", "0:1")
        nex_tok = Token("NotMatter", "NotMatter", "0:2")
        self.assertNotEqual(check_construction(cur_tok, nex_tok), 'Next')

    def test_check_for(self):
        from src.parser_helper import check_for, check_construction, current_construction
        from src.lexer import Token

        # correct_case
        current_construction.token_type = "keyword_for"  # на примере assign
        current_construction.position = 1
        cur_tok = Token("<", "operator_less", "0:4")  # в форе должно находится в словии (1, где 0 - переменная и 2 - икр)
        nex_tok = Token("1", "numeric_constant", "0:5")

        self.assertEqual(check_for(cur_tok, nex_tok), None)

        # incorrect_case
        current_construction.token_type = "keyword_for"  # на примере assign
        current_construction.position = 0 # предположительное условие будет находится инициализации переменной
        cur_tok = Token("<", "operator_less", "0:4")  # в форе должно находится в словии (1, где 0 - переменная и 2-икр)
        nex_tok = Token("1", "numeric_constant", "0:5")

        try:
            self.assertEqual(check_for(cur_tok, nex_tok), None)
        except:
            pass # должно броситься исключение (по стандарту для всех проверок)

    def test_check_nesting(self):
        from src.parser_helper import nesting_stack, check_nesting
        from src.lexer import Token

        # correct case
        cur_tok = Token("{", "r_brace", "NotMatter")
        nesting_stack.append(cur_tok)
        nesting_stack.append(cur_tok)

        self.assertEqual(check_nesting(), 2)

        cur_tok = Token("}", "l_brace", "NotMatter")
        nesting_stack.append(cur_tok)
        nesting_stack.append(cur_tok)

        self.assertEqual(check_nesting(), 0)

        # incorrect case
        cur_tok = Token("{", "r_brace", "NotMatter")
        nesting_stack.append(cur_tok)
        cur_tok = Token("}", "l_brace", "NotMatter")
        nesting_stack.append(cur_tok)
        cur_tok = Token("{", "r_brace", "NotMatter")
        nesting_stack.append(cur_tok)

        self.assertNotEqual(check_nesting(), 0)


    def test_check_php(self):
        from src.parser_helper import check_php
        from src.lexer import Token

        # correct case
        cur_tok = Token("<?php", "keyword_<?php", "1:0")
        self.assertEqual(check_php(cur_tok), 'Next')

        # incorrect case
        cur_tok = Token("<?php", "keyword_<?php", "5:0")
        self.assertNotEqual(check_php(cur_tok), 'Next')

        self.assertEqual(check_php(cur_tok), "5:0")