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

if __name__ == '__main__':
    unittest.main()