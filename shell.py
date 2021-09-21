import example

while True:
    text = input('CodePlanner > ')
    result, error = example.run('<stdin>', text)
    if error: print(error.as_string())
    else: print(result)
