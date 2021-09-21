import string

class Error:
    def __init__(self, pos_start, pos_end, error_name, details):
        self.pos_start = pos_start
        self.pos_end = pos_end
        self.error_name = error_name
        self.details = details
    
    def as_string(self):
        result  = f'{self.error_name}: {self.details}\n'
        result += f'File {self.pos_start.fn}, line {self.pos_start.ln + 1}'
        return result

class IllegalCharError(Error):
    def __init__(self, pos_start, pos_end, details):
        super().__init__(pos_start, pos_end, 'Illegal Character', details)

class Position:
    def __init__(self, idx, ln, col, fn, ftxt):
        self.idx = idx
        self.ln = ln
        self.col = col
        self.fn = fn
        self.ftxt = ftxt

    def advance(self, current_char):
        self.idx += 1
        self.col += 1

        if current_char == '\n':
            self.ln += 1
            self.col = 0

        return self

    def copy(self):
        return Position(self.idx, self.ln, self.col, self.fn, self.ftxt)

class TokenTypes():
    TT_INT		    = 'INT'
    TT_FLOAT        = 'FLOAT'
    TT_PLUS         = 'PLUS'
    TT_MINUS        = 'MINUS'
    TT_MUL          = 'MUL'
    TT_DIV          = 'DIV'
    TT_LPAREN       = 'LPAREN'
    TT_RPAREN       = 'RPAREN'
    TT_SEMICOLON    = 'SEMICOLON'
    TT_LCURLY       = 'LCURLY'
    TT_RCURLY       = 'RCURLY'

class Token:
    def __init__(self, type_, value=None):
        self.type = type_
        self.value = value
    
    def __repr__(self):
        if self.value: return f'{self.type}:{self.value}'
        return f'{self.type}'


class Lexer:
    def __init__(self, fn, text):
        self.fn = fn
        self.text = text
        self.pos = Position(-1, 0, -1, fn, text)
        self.current_char = None
        self.advance()
        self.digits = '0123456789'
        self.letters = string.ascii_letters  
    
    def advance(self):
        self.pos.advance(self.current_char)
        self.current_char = self.text[self.pos.idx] if self.pos.idx < len(self.text) else None

    def make_tokens(self, tokens):
        if self.current_char == None:
            return tokens, None
        elif self.current_char in ' \t':
            self.advance()
        elif self.current_char in self.digits:
            tokens.append(self.make_number())
        elif self.current_char == '+':
            tokens.append(Token(TokenTypes.TT_PLUS))
            self.advance()
        elif self.current_char in self.letters:
            tokens.append(self.make_text())
            self.advance()    
        elif self.current_char == '-':
            tokens.append(Token(TokenTypes.TT_MINUS))
            self.advance()
        elif self.current_char == '*':
            tokens.append(Token(TokenTypes.TT_MUL))
            self.advance()
        elif self.current_char == '/':
            tokens.append(Token(TokenTypes.TT_DIV))
            self.advance()
        elif self.current_char == '(':
            tokens.append(Token(TokenTypes.TT_LPAREN))
            self.advance()
        elif self.current_char == ')':
            tokens.append(Token(TokenTypes.TT_RPAREN))
            self.advance()
        elif self.current_char == '{':
            tokens.append(Token(TokenTypes.TT_LCURLY))
            self.advance()
        elif self.current_char == '}':
            tokens.append(Token(TokenTypes.TT_RCURLY))
            self.advance()
        elif self.current_char == ';':
            tokens.append(Token(TokenTypes.TT_SEMICOLON))
            self.advance()
        else:
            pos_start = self.pos.copy()
            char = self.current_char
            self.advance()
            return [], IllegalCharError(pos_start, self.pos, "'" + char + "'")

        return self.make_tokens(tokens)
        
    def clean_tokens(self, tokens=[]):
        return list(filter(None, tokens))

    def make_text(self, text = ''):
        if self.current_char != None and self.current_char in self.letters:
            text += self.current_char
            self.advance()
            return self.make_text(text)
        if(text == 'and'):
            return Token(TokenTypes.TT_PLUS)
        elif(text == 'returns'):
            return Token(TokenTypes.TT_MINUS)
        elif(text == 'shortcuts'):
            return Token(TokenTypes.TT_MUL)
        elif(text == 'ghostrides'):
            return Token(TokenTypes.TT_DIV)
        
    def make_number(self, num_str = '', dot_count = 0 ):
        if self.current_char != None and self.current_char in self.digits + '.':
            if self.current_char == '.':
                if dot_count == 0: 
                    dot_count += 1
                    num_str += '.'
                    self.advance()
                    return self.make_number(num_str, dot_count)
            else:
                num_str += self.current_char
                self.advance()
                return self.make_number(num_str, dot_count)

        if dot_count == 0:
            return Token(TokenTypes.TT_INT, int(num_str))
        else:
            return Token(TokenTypes.TT_FLOAT, float(num_str))


def run(fn, text):
    lexer = Lexer(fn, text)
    tokens, error = lexer.make_tokens([])
    tokens = lexer.clean_tokens(tokens);
    return tokens, error