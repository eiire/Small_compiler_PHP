from unittest import TestCase


class TestLexer(TestCase):
    file = open("result.txt", "r+")  # clean file

    def test_check_family_token(self):
        from src.lexer import check_family_token
        my_list_tokens = ['class', 'use', 'if', 'namespace', 'for', 'while', 'main', 'my_function_name', 'function',
                          'return', 'echo', '"gggg', 'ffff"', 'ццkkц', '$*nhh*n', '$_var', '11', '0x10', '01111001',
                          '088', '0b1111']
        expected_name_tokens = ['keyword_class', 'keyword_use', 'keyword_if', 'keyword_namespace', 'keyword_for',
                                'keyword_while', 'identifier', 'identifier', 'keyword_function', 'keyword_return',
                                'identifier', 'unknown', 'unknown', 'unknown', 'unknown', 'identifier_variable',
                                'numeric_constant', 'numeric_constant_hex', 'numeric_constant_oct', 'unknown',
                                'numeric_constant_binary']
        i = 0
        for word in my_list_tokens:
            self.assertEqual(expected_name_tokens[i], check_family_token(word), "good")
            i += 1

    def test_my_str_split(self):
        from src.lexer import my_str_split
        test_str = "&frg_23 function(frfr);}{-[]+"
        expected_true = "&frg_23 function ( frfr )  ;  }  {  -  [  ]  + "
        self.assertTrue(my_str_split(test_str) == expected_true, "Should be True")

    def test_tokens_in_line(self):
        file_clear = open("result.txt", 'w')  # clear file
        from src.lexer import tokens_in_line
        test_str = "function qwe("
        expected_true = ['Loc=<4:0>   keyword_function function\n', 'Loc=<4:9>   identifier qwe\n',
                         'Loc=<4:12>   l_paren (\n']
        file = open("result.txt", 'r+')
        tokens_in_line(test_str, 4, file)
        i = 0
        for line in file:
            self.assertTrue(line == expected_true[i], "Should be True")
            # print(line)
            i += 1
        file.close()
        file_clear.close()
        return


    def test_lexer_comment(self):
        from src.lexer import tokens_in_line, check_thist_heshteg_after_cov
        file = open("for_check_cooment.txt", 'r')
        file_res = open("result.txt", 'w') #  clear file
        line_number = 0
        for line in file:
            line_number += 1
            if line.find('"') < line.find('#') < line.rfind(
                    '"'):  # "ff#ff" line[0:check_thist_heshteg_after_cov(line) - 1!!!]
                tokens_in_line(line[0:check_thist_heshteg_after_cov(line) - 1], line_number,
                               file_res)  # slize for thist # beginning left
            else:
                tokens_in_line(line.partition('#')[0], line_number, file_res)  # "ffff"

        file_res.close()
        file_res = open("result.txt", "r")
        for line in file:
            if line.rfind('#') and line.rfind('#') > line.rfind('"'):  # if find # after " (working from right becouse test for comment, not "")
                self.assertEqual(line.rfind('#'), -1)
        file.close()
        file_res.close()

    file.close()
