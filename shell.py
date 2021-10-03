from myLexer import Error
import myInterpreter
from myInterpreter import SymbolTable, Number


def run_shell(text, symbol_table):
    if text == 'quit':
        return
    # print('symbol_table', symbol_table)
    result, error, symbol_table = myInterpreter.run('<stdin>', text, symbol_table)
    # print('symbol_table_after', symbol_table)
    if error: print(error.as_string())
    else: print(result)
    text = input('CodePlanner > ')
    return run_shell(text, symbol_table)

symbol_table = SymbolTable().insert_basic_function("null", Number(0)).insert_basic_function("GREEN", Number(1)).insert_basic_function("RED", Number(0))
text = input('CodePlanner > ')  
run_shell(text, symbol_table)
# remember curr token - advance to next character - put function in right - create binop node,