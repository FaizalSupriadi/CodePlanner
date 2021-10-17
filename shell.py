
from myLexer import Error
import myInterpreter
from myInterpreter import SymbolTable, Number
from myClock import Clock

def run_shell(text, symbol_table:SymbolTable= SymbolTable(),curr_path:str='') -> None:
    if text == 'quit':
        return
    result, error, symbol_table = myInterpreter.run('<stdin>', text, symbol_table)
    if error:
        print(result, error)
    text = input('CodePlanner > ')

    return run_script(text, symbol_table, curr_path)

def run_script(text, symbol_table, curr_path) -> None:
    if '.' in text[0]:
        with open(curr_path, "r") as f:
            script = f.read()
            return run_shell(script, symbol_table, curr_path)

    if 'RUN' in text:
        file = text.strip('RUN(')
        with open("examples/" + file[:-1], "r") as f:
            script = f.read()
            return run_shell(script, symbol_table, "ATP/examples/" + file[:-1])
    else:
        return run_shell(text, symbol_table,curr_path)

if __name__ == "__main__":
    symbol_table = SymbolTable().insert_static("NULL", Number.null).insert_static("GREEN", Number(1)).insert_static("RED", Number(0))
    run_script("RUN(excercises/even_odd.traffic)", symbol_table, "")