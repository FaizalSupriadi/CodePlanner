import unittest
import myLexer as lex
from myLexer import TokenTypes as tt

class TestLexer(unittest.TestCase):

    #Test to check if the lexer creates all tokens and if they have their correct values.
    def test_all_token_creation(self):

        # Create tokens from function
        with open("tests/test_lex.traffic", "r") as f:
            text = f.read()
        tokens, _ = lex.make_tokens([], lex.Position(0, 0, 0, "lex_test", text), text)

        # All token types
        types = [tt.TT_PLUS, tt.TT_MINUS, tt.TT_MUL, tt.TT_DIV, tt.TT_PLUS, tt.TT_MINUS, tt.TT_MUL, tt.TT_DIV, tt.TT_LT, tt.TT_GT, tt.TT_IDENTIFIER, tt.TT_EQ, 
            tt.TT_KEYWORD, tt.TT_IDENTIFIER, tt.TT_IDENTIFIER, tt.TT_KEYWORD, tt.TT_KEYWORD, tt.TT_KEYWORD, tt.TT_KEYWORD, tt.TT_KEYWORD, tt.TT_KEYWORD,  
            tt.TT_KEYWORD, tt.TT_KEYWORD, tt.TT_KEYWORD, tt.TT_KEYWORD, tt.TT_NEWLINE, tt.TT_IDENTIFIER, tt.TT_LPAREN, tt.TT_RPAREN, tt.TT_LSQUARE, 
            tt.TT_RSQUARE, tt.TT_LCURLY, tt.TT_RCURLY, tt.TT_COMMA, tt.TT_COLON]

        # All token type values
        values = [None, None, None, None, None, None, None, None, None, None, 
            "equals", None, "NOT", "RED", "GREEN", "DESTINATION", "TRAFFIC", 
            "BYPASS", "FLEE", "GPS", "REFUEL", "ROUTE", "VEHICLE", "DRIVING", 
            "SPEEDING", None, "Identity", None, None, None, None, None, None, 
            None, None,]

        for i in range(len(tokens)):
            self.assertEqual(tokens[i].type, types[i])
            self.assertEqual(tokens[i].value, values[i])

    #Test to check functionality with "comments.traffic" script
    def test_run_lexer_on_script(self):

        # Create tokens from function
        with open("examples/comments.traffic", "r") as f:
            text = f.read()
        tokens, _ = lex.make_tokens([], lex.Position(0, 0, 0, "comments", text), text)

        # All script token types
        types = [tt.TT_NEWLINE, tt.TT_KEYWORD, tt.TT_INT, tt.TT_EE, tt.TT_INT, tt.TT_KEYWORD, 
            tt.TT_NEWLINE, tt.TT_NEWLINE, tt.TT_KEYWORD, tt.TT_LPAREN, tt.TT_INT, tt.TT_RPAREN]

        # All script token type values
        values = [None, "TRAFFIC", 2, None, 2, "GPS", None, None, "PRINT", None, 100, None]

        for i in range(len(tokens)):
            self.assertEqual(tokens[i].type, types[i])
            self.assertEqual(tokens[i].value, values[i])



if __name__ == '__main__':
    unittest.main()