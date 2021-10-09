from myLexer import Error
import myInterpreter
from myInterpreter import SymbolTable, Number, List


def run_shell(text, symbol_table,curr_path):
    if text == 'quit':
        return
    result, error, symbol_table = myInterpreter.run('<stdin>', text, symbol_table)
    if len(result.elements) == 1:
        print(result.elements[0])
    else:
        print(result)
    text = input('CodePlanner > ')

    return run_script(text, symbol_table, curr_path)

def run_script(text, symbol_table, curr_path):
    if '.' in text[0]:
        with open(curr_path, "r") as f:
            script = f.read()
            return run_shell(script, symbol_table, curr_path)

    if 'RUN' in text:
        file = text.strip('RUN(')
        with open("ATP/examples/" + file[:-1], "r") as f:
            script = f.read()
            return run_shell(script, symbol_table, "ATP/examples/" + file[:-1])
    else:
        return run_shell(text, symbol_table,curr_path)

symbol_table = SymbolTable().insert_basic_function("NULL", Number.null).insert_basic_function("GREEN", Number(1)).insert_basic_function("RED", Number(0))
run_script("RUN(for_loop.traffic)", symbol_table, '')
