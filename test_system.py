import unittest
import myLexer as lex
import myParser as parser
import myInterpreter as interpreter

from myLexer import TokenTypes as tt
from myInterpreter import SymbolTable
class TestSystem(unittest.TestCase):

    #Test to check functionality with "system.traffic" script
    def test_lexer(self):
        # Create tokens from function
        with open("tests/test_system.traffic", "r") as f:
            text = f.read()
        tokens, _ = lex.make_tokens([], lex.Position(0, 0, 0, "functions", text), text)
        
        # All script token types
        types = [tt.TT_KEYWORD, tt.TT_LPAREN, tt.TT_INT, tt.TT_PLUS, tt.TT_INT, tt.TT_RPAREN, tt.TT_NEWLINE, tt.TT_KEYWORD, tt.TT_LPAREN, tt.TT_INT, tt.TT_MINUS, 
            tt.TT_INT, tt.TT_RPAREN, tt.TT_NEWLINE, tt.TT_KEYWORD, tt.TT_LPAREN, tt.TT_INT, tt.TT_DIV, tt.TT_INT, tt.TT_RPAREN, tt.TT_NEWLINE, 
            tt.TT_KEYWORD, tt.TT_LPAREN, tt.TT_INT, tt.TT_MUL, tt.TT_INT, tt.TT_RPAREN, tt.TT_NEWLINE, tt.TT_KEYWORD, tt.TT_LPAREN, tt.TT_LPAREN, tt.TT_INT, tt.TT_PLUS, 
            tt.TT_INT, tt.TT_RPAREN, tt.TT_MUL, tt.TT_INT, tt.TT_RPAREN]

        # All script token type values
        values = ["PRINT", None, 1, None, 1, None, None, "PRINT", None, 1, None, 1, None, None, "PRINT", None, 4, None, 2, None, None, "PRINT", None, 2, None, 2, 
        None, None, "PRINT", None, None, 3, None, 3, None, None, 3, None]

        for i in range(len(tokens)):
            self.assertEqual(tokens[i].type, types[i])
            self.assertEqual(tokens[i].value, values[i])
    
    def test_parser(self):
        # Create tokens from function
        with open("tests/test_system.traffic", "r") as f:
            text = f.read()
        tokens, _ = lex.make_tokens([], lex.Position(0, 0, 0, "functions", text), text)
        ast, _ = parser.parse(tokens)
        str_ast = repr(ast)
        self.assertEqual(str_ast, "(LISTNODE: ELEMNODES: [(PRINTNODE, (BINOPNODE: NUMBERNODE: INT:1, PLUS, NUMBERNODE: INT:1)), (PRINTNODE, (BINOPNODE: NUMBERNODE: INT:1, MINUS, NUMBERNODE: INT:1)), (PRINTNODE, (BINOPNODE: NUMBERNODE: INT:4, DIV, NUMBERNODE: INT:2)), (PRINTNODE, (BINOPNODE: NUMBERNODE: INT:2, MUL, NUMBERNODE: INT:2)), (PRINTNODE, (BINOPNODE: (BINOPNODE: NUMBERNODE: INT:3, PLUS, NUMBERNODE: INT:3), MUL, NUMBERNODE: INT:3))])")
    
    def test_interpreter(self):
        with open("tests/test_system.traffic", "r") as f:
            text = f.read()
        tokens, _ = lex.make_tokens([], lex.Position(0, 0, 0, "functions", text), text)
        ast, _ = parser.parse(tokens)
        result, new_symbol_table = interpreter.interpreter(ast,SymbolTable())
        self.assertEqual(repr(result),"[PRINTED, PRINTED, PRINTED, PRINTED, PRINTED]")
        self.assertEqual(repr(new_symbol_table),"SymbolTable: {}")

if __name__ == '__main__':
    unittest.main()