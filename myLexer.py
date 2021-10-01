import string
from typing import Union
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
class InvalidSyntaxError(Error):
		def __init__(self, pos_start, pos_end, details=''):
				super().__init__(pos_start, pos_end, 'Invalid Syntax', details)
                
class Position:
    def __init__(self, idx=0, ln=0, col=0, fn='', ftxt=''):
        self.idx = idx
        self.ln = ln
        self.col = col

        self.prevIdx = idx
        self.prevLn = ln
        self.prevCol = col

        self.fn = fn
        self.ftxt = ftxt
    
    def __repr__(self) -> str:
        return f'{self.idx}{self.ln}{self.col}'

    def advance(self, current_char:str=None):
        self.prevIdx = self.idx
        self.prevLn = self.ln
        self.prevCol = self.col

        self.idx += 1
        self.col += 1

        if current_char == '\n':
            self.ln += 1
            self.col = 0

        return self
    
    def copyPrev(self):
        return Position(self.prevIdx, self.prevLn, self.prevCol, self.fn, self.ftxt)

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
    TT_EOF          = 'EOF'

class Token:
    def __init__(self, type_, value=None):
        self.type = type_
        self.value = value
    
    def __repr__(self):
        if self.value: return f'{self.type}:{self.value}'
        return f'{self.type}'

digits = '0123456789'
letters = string.ascii_letters

def make_tokens(tokens:list, curr_pos:Position, text:str) -> Union[list, Error]:
    curr_char = text[curr_pos.idx] if curr_pos.idx < len(text) else None
    # print('idx', curr_pos.idx, 'curr char',curr_char)

    if curr_char == None:
        return tokens, None
    elif text[curr_pos.idx] in ' \t':
        pass
    elif curr_char in digits:
        token, pos = make_number(curr_pos,text)
        tokens.append(token)
        return make_tokens(tokens, pos, text) 
    elif curr_char in letters:
        token, pos = make_text(curr_pos,text)
        tokens.append(token)
        return make_tokens(tokens, pos, text)
    elif curr_char == '+':
        tokens.append(Token(TokenTypes.TT_PLUS))
    elif curr_char == '-':
        tokens.append(Token(TokenTypes.TT_MINUS))
    elif curr_char == '*':
        tokens.append(Token(TokenTypes.TT_MUL))
    elif curr_char == '/':
        tokens.append(Token(TokenTypes.TT_DIV))
    elif curr_char == '(':
        tokens.append(Token(TokenTypes.TT_LPAREN))
    elif curr_char == ')':
        tokens.append(Token(TokenTypes.TT_RPAREN))
    elif curr_char == '{':
        tokens.append(Token(TokenTypes.TT_LCURLY))
    elif curr_char == '}':
        tokens.append(Token(TokenTypes.TT_RCURLY))
    elif curr_char == ';':
        tokens.append(Token(TokenTypes.TT_SEMICOLON))

        # pos_start = self.pos.copy()
        # char = current_char
        # return [], IllegalCharError(pos_start, self.pos, "'" + char + "'")

    return make_tokens(tokens, curr_pos.advance(curr_char), text) 
    
def clean_tokens(tokens=[]) -> list:
    return list(filter(None, tokens))

def make_text(curr_pos:Position = Position(),text:str = '',keyword:str = '') -> Union[Token, Position]:
    curr_char = text[curr_pos.idx] if curr_pos.idx < len(text) else None
    if curr_char != None and curr_char in letters:
        keyword += curr_char
        return make_text(curr_pos.advance(curr_char),text,keyword)
    
    if(keyword == 'and'):
        return Token(TokenTypes.TT_PLUS), curr_pos
    elif(keyword == 'returns'):
        return Token(TokenTypes.TT_MINUS), curr_pos
    elif(keyword == 'shortcuts'):
        return Token(TokenTypes.TT_MUL), curr_pos
    elif(keyword == 'ghostrides'):
        return Token(TokenTypes.TT_DIV), curr_pos
    else:
        return None, curr_pos
    
def make_number(curr_pos:Position = Position(), text:str='', num_str:str = '', dot_count:int = 0 ) -> Union[Token, Position]:
    curr_char = text[curr_pos.idx] if curr_pos.idx < len(text) else None
    if curr_char != None and curr_char in digits + '.':
        if curr_char == '.':
            if dot_count == 0: 
                dot_count += 1
                num_str += '.'
                return make_number(curr_pos.advance(curr_char),text,num_str, dot_count)
        else:
            num_str += curr_char
            return make_number(curr_pos.advance(curr_char),text,num_str, dot_count)

    if dot_count == 0:
        return Token(TokenTypes.TT_INT, int(num_str)), curr_pos
    else:
        return Token(TokenTypes.TT_FLOAT, float(num_str)), curr_pos

def run(fn:str='', text:str=''):
    pos = Position(0, 0, 0, fn, text)
    tokens, error = make_tokens([], pos, text)
    if error: return None, error
    tokens = clean_tokens(tokens)
    return tokens, error