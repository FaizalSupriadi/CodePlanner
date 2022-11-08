from types import new_class
import unittest
import myLexer as lex
import myParser as parser
import myInterpreter as interpreter
from myInterpreter import SymbolTable

class TestParser(unittest.TestCase):

    #Test to check if the lexer creates all tokens and if they have their correct values.
    def test_correct_output(self):
        # Create tokens from function
        with open("tests/test_interpreter.traffic", "r") as f:
            text = f.read()
        tokens, _ = lex.make_tokens([], lex.Position(0, 0, 0, "parser_test", text), text)
        ast, _ = parser.parse(tokens)
        result, new_symbol_table = interpreter.interpreter(ast,SymbolTable())
        self.assertEqual(repr(result),"[FUNCTION: (NAME: check: BODY: (LISTNODE: ELEMNODES: [(TRAFFICNODE: [((BINOPNODE: VARACCESNODE: IDENTIFIER:n, EE, NUMBERNODE: INT:2), (LISTNODE: ELEMNODES: [(PRINTNODE, NUMBERNODE: INT:100)]), True), ((BINOPNODE: VARACCESNODE: IDENTIFIER:n, EE, NUMBERNODE: INT:3), (LISTNODE: ELEMNODES: [(PRINTNODE, NUMBERNODE: INT:200)]), True)], FLEECASE: ((LISTNODE: ELEMNODES: [(PRINTNODE, NUMBERNODE: INT:300)]), True))]), ARG_NAMES:['n']), [[PRINTED]], [[PRINTED]], [0]]")
        self.assertEqual(repr(new_symbol_table),"SymbolTable: {'check': FUNCTION: (NAME: check: BODY: (LISTNODE: ELEMNODES: [(TRAFFICNODE: [((BINOPNODE: VARACCESNODE: IDENTIFIER:n, EE, NUMBERNODE: INT:2), (LISTNODE: ELEMNODES: [(PRINTNODE, NUMBERNODE: INT:100)]), True), ((BINOPNODE: VARACCESNODE: IDENTIFIER:n, EE, NUMBERNODE: INT:3), (LISTNODE: ELEMNODES: [(PRINTNODE, NUMBERNODE: INT:200)]), True)], FLEECASE: ((LISTNODE: ELEMNODES: [(PRINTNODE, NUMBERNODE: INT:300)]), True))]), ARG_NAMES:['n'])}")
    
if __name__ == '__main__':
    unittest.main()