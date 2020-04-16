from unittest import TestCase
import subprocess


class TestSema(TestCase):
    from src.lexer import Token
    test_cur_tok = Token()
    test_next_tok = Token()
    tester_symbol_table = {
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
    def test_warnigs(self):
        from src.sema_helper import warnings
        warnings()
