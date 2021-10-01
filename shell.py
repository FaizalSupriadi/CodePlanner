from myLexer import Error
import myInterpreter

while True:
    text = input('CodePlanner > ')
    result, error = myInterpreter.run('<stdin>', text)
    if error: print(error.as_string())
    else: print(result)

# remember curr token - advance to next character - put function in right - create binop node,