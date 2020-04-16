from unittest import TestCase
import subprocess


class TestSema(TestCase):
    def test_get_type_var(self):
        from src.lexer import Token
        from src.sema_helper import get_type_var
        symbol_table = {"1:1": ["$var1_lvl_1:NULL"]}
        list_res_expected = list()
        list_res_expected.append(get_type_var(symbol_table, Token("$var1_lvl_1", "identifier_variable", ""), "1:1",
                                     type_or_var='TYPE'))
        list_res_expected.append(get_type_var(symbol_table, Token("$var1_lvl_1", "identifier_variable", ""), "1:1",
                                     type_or_var='VAR'))
        self.assertEqual(['NULL', '$var1_lvl_1'], list_res_expected)

    def test_change_type_main_var(self):
        from src.lexer import Token
        from src.sema_helper import change_type_main_var
        symbol_table = {"1:1": ["$var1_lvl_1:NULL"]}
        change_type_main_var(symbol_table, Token("$var1_lvl_1", "", ""), Token("str", "string_literal", ""), "1")

        self.assertEqual({"1:1": ["$var1_lvl_1:string_literal"]}, symbol_table)

    def test_cut_type_var(self):
        from src.lexer import Token
        from src.sema_helper import cut_type_var
        list_vars = ['$var2:string_literal', '$var2:numeric_constant']
        expected_list_vars = cut_type_var(list_vars)

        self.assertEqual(['$var2', '$var2'], expected_list_vars)

    def test_find_var_above(self):
        from src.lexer import Token
        from src.sema_helper import find_var_above
        symbol_table = {
            "0:0": [
                "$var1_lvl_0:numeric_constant"
            ],
            "1:1": [
                "$var1_lvl_1:string_literal"
            ],
            "2:1": [
                "$var1_lvl_2:NULL",
                "$var4:NULL"
            ]
        }
        list_res = list()
        list_res.append(find_var_above(symbol_table, Token("$var1_lvl_1", "identifier_variable", "8:24"), 1))
        list_res.append(find_var_above(symbol_table, Token("$NonExistsVar", "identifier_variable", "8:24"), 1))

        self.assertEqual([True, False], list_res)


    def test_warnigs(self):
        from src.lexer import Token
        from src.sema_helper import warnings

        test_cur_tok_1 = Token("$var1_lvl_1", "identifier_variable", "8:24")

        test_cur_tok_2 = Token("$undefined_VAR", "identifier_variable", "8:24")
        tester_symbol_table = {
            "1:1": [
                "$var1_lvl_1:string_literal"
            ],
            "1:2": [
                "$undefined_VAR:NULL"
            ],
        }
        list_res = list()
        list_res.append(warnings(test_cur_tok_1, Token("", "", ""), tester_symbol_table, "1:1", None,
                                 "operator_multiplication"))
        list_res.append(warnings(test_cur_tok_1, Token("", "", ""), tester_symbol_table, "1:1", None,
                                 "operator_sum"))
        list_res.append(warnings(test_cur_tok_2, Token("", "", ""), tester_symbol_table, "1:2", None,
                                 "operator_multiplication"))

        self.assertEqual(list_res, ['Warning: A non-numeric value encountered in 8:24', None,
                                    'NOTICE Undefined variable: $undefined_VAR on 8:24'])





