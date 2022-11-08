import unittest
import myLexer as lex
import myParser as parser

class TestParser(unittest.TestCase):

    #Test to check if the parser creates the correct AST and if they have their correct values.
    def test_correct_ast(self):
        with open("tests/test_parser.traffic", "r") as f:
            text = f.read()
        tokens, _ = lex.make_tokens([], lex.Position(0, 0, 0, "parser_test", text), text)
        ast, _ = parser.parse(tokens)
        str_ast = repr(ast)
        self.assertEqual(str_ast, "(LISTNODE: ELEMNODES: [(PRINTNODE, (BINOPNODE: NUMBERNODE: INT:1, PLUS, NUMBERNODE: INT:1))])")
    
    def test_math(self):
        # Create tokens from function
        with open("tests/test_math.traffic", "r") as f:
            text = f.read()
        tokens, _ = lex.make_tokens([], lex.Position(0, 0, 0, "functions", text), text)
        ast, _ = parser.parse(tokens)
        str_ast = repr(ast)
        self.assertEqual(str_ast, "(LISTNODE: ELEMNODES: [(PRINTNODE, (BINOPNODE: NUMBERNODE: INT:1, PLUS, NUMBERNODE: INT:1)), (PRINTNODE, (BINOPNODE: NUMBERNODE: INT:1, MINUS, NUMBERNODE: INT:1)), (PRINTNODE, (BINOPNODE: NUMBERNODE: INT:4, DIV, NUMBERNODE: INT:2)), (PRINTNODE, (BINOPNODE: NUMBERNODE: INT:2, MUL, NUMBERNODE: INT:2)), (PRINTNODE, (BINOPNODE: (BINOPNODE: NUMBERNODE: INT:3, PLUS, NUMBERNODE: INT:3), MUL, NUMBERNODE: INT:3))])")
if __name__ == '__main__':
    unittest.main()