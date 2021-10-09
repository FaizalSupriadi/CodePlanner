from myLexer import Error
import myInterpreter
from myInterpreter import SymbolTable, Number, List


def run_shell(text, symbol_table):
    if text == 'quit':
        return
    result, error, symbol_table = myInterpreter.run('<stdin>', text, symbol_table)
    # print(type(result.elements))
    # if error: print(error.as_string())
    # elif isinstance(result, List):
    #     if isinstance(result.elements, list):
    #         if len(result.elements) == 1: print(result.elements[0])
    #         else: print(result)
    #     else: print(result)
    # else: print(result)
    print("RESULT",result)
    text = input('CodePlanner > ')

    return run_script(text, symbol_table)

def run_script(text, symbol_table):
    if '.' in text:
        with open("ATP/myCode.traffic", "r") as f:
            script = f.read()
            return run_shell(script, symbol_table)

    if 'RUN' in text:
        file = text.strip('RUN(')
        with open(file[:-1], "r") as f:
            script = f.read()
            return run_shell(script, symbol_table)
    else:
        return run_shell(text, symbol_table)

symbol_table = SymbolTable().insert_basic_function("NULL", Number.null).insert_basic_function("GREEN", Number(1)).insert_basic_function("RED", Number(0))
# text = input('CodePlanner > ')
run_script("RUN(ATP/myCode.traffic)", symbol_table)
# run_shell(text, symbol_table)
# remember curr token - advance to next character - put function in right - create binop node,