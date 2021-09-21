import myParser

while True:
    text = input('CodePlanner > ')
    result, error = myParser.run('<stdin>', text)
    if error: print(error.as_string())
    else: print(result)
