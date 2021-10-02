from myLexer import Error
import myInterpreter
from myInterpreter import SymbolTable, Number

symbol_table = SymbolTable().insert_basic_function("null", Number(0)) 

while True:
    text = input('CodePlanner > ')
    print('symbol_table', symbol_table)
    result, error, symbol_table = myInterpreter.run('<stdin>', text, symbol_table)
    print('symbol_table_after', symbol_table)
    if error: print(error.as_string())
    else: print(result)

# remember curr token - advance to next character - put function in right - create binop node,