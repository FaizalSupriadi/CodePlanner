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

    def goTo(self, idx):
        self.idx = idx
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
    TT_IDENTIFIER	= 'IDENTIFIER'
    TT_KEYWORD		= 'KEYWORD'
    TT_EE           = 'EE'
    TT_NE           = 'NE'
    TT_NOT          = 'NOT'
    TT_LT           = 'LT'
    TT_GT           = 'GT'
    TT_LTE          = 'LTE'
    TT_GTE          = 'GTE'
    TT_EQ           = 'EQ'
    TT_EOF          = 'EOF'

    KEYWORDS = [
        'VEHICLE', # Variable
        'AND', 
        'OR', 
        'NOT', 
        'IF', 
        'THEN', 
        'ELIF', 
        'ELSE', 
        'FOR', 
        'TO', 
        'STEP', 
        'WHILE'
        ]


class Token:
    def __init__(self, type_=None, value=None):
        self.type = type_
        self.value = value
    
    def matches(self, type_, value_):
        return self.type == type_ and self.value == value_

    def __repr__(self):
        if self.value: return f'{self.type}:{self.value}'
        return f'{self.type}'

DIGITS = '0123456789'
LETTERS = string.ascii_letters
LETTERS_DIGITS = LETTERS + DIGITS

def add_token(token:Token, pos:Position, tokens:list) -> tuple:
    tokens.append(token)
    return tokens, pos

def make_tokens(tokens:list, curr_pos:Position, text:str) -> Union[list, Error]:
    curr_char = get_curr_char(text, curr_pos)
    if curr_char == None:
        return tokens, None
    elif curr_char in ' \t':
        pass
    elif curr_char in DIGITS:
        return make_tokens(*add_token(*make_number(curr_pos,text), tokens), text) 
    elif curr_char in LETTERS:
        return make_tokens(*add_token(*make_identifier(curr_pos,text),tokens), text)
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

    return make_tokens(tokens, curr_pos.advance(curr_char), text) 
    
def clean_tokens(tokens=[]) -> list:
    return list(filter(None, tokens))

def make_identifier(curr_pos:Position = Position(),text:str = '',keyword:str = '') -> Union[Token, Position]:
    curr_char = get_curr_char(text, curr_pos)
    if keyword != '' and keyword[0] in DIGITS:
        return Token(), curr_pos.goTo(curr_pos.idx-len(keyword))
    if curr_char != None and curr_char in LETTERS_DIGITS:
        return make_identifier(curr_pos.advance(curr_char),text,keyword+curr_char)
    if(keyword == 'and'):
        return Token(TokenTypes.TT_PLUS), curr_pos
    elif(keyword == 'returns'):
        return Token(TokenTypes.TT_MINUS), curr_pos
    elif(keyword == 'shortcuts'):
        return Token(TokenTypes.TT_MUL), curr_pos
    elif(keyword == 'ghostrides'):
        return Token(TokenTypes.TT_DIV), curr_pos
    elif(keyword == 'travels'):
        return make_equals(curr_pos,text)
    elif(keyword == 'less'):
        return Token(TokenTypes.TT_LT), curr_pos
    elif(keyword == 'more'):
        return Token(TokenTypes.TT_GT), curr_pos
    elif(keyword == 'cancelled'):
        return Token(TokenTypes.TT_NOT), curr_pos
    else:
        return Token(TokenTypes.TT_KEYWORD if keyword in TokenTypes.KEYWORDS else TokenTypes.TT_IDENTIFIER, keyword), curr_pos

def make_equals(curr_pos:Position = Position(), text:str=''):
    curr_char = get_curr_char(text, curr_pos)
    token, new_pos = make_identifier(curr_pos.advance(curr_char),text)
    if token.type == 'KEYWORD' or token.type == 'IDENTIFIER':
        return Token(TokenTypes.TT_EQ), curr_pos.goTo(curr_pos.idx - len(token.value)) 
    if token.type == 'EQ':
        return Token(TokenTypes.TT_EE), new_pos
    elif token.type == 'LT':
        return Token(TokenTypes.TT_LTE), new_pos
    elif token.type == 'GT':
        return Token(TokenTypes.TT_GTE), new_pos
    elif token.type == 'NOT':
        return Token(TokenTypes.TT_NE), new_pos
    else:
        return Token(TokenTypes.TT_EQ), curr_pos
    
def make_number(curr_pos:Position = Position(), text:str='', num_str:str = '', dot_count:int = 0 ) -> Union[Token, Position]:
    curr_char = get_curr_char(text, curr_pos)
    if curr_char != None and curr_char in DIGITS + '.':
        if curr_char == '.':
            if dot_count == 0: 
                return make_number(curr_pos.advance(curr_char),text,num_str+'.', dot_count+1)
        else:
            return make_number(curr_pos.advance(curr_char),text,num_str+curr_char, dot_count)

    if dot_count == 0:
        return Token(TokenTypes.TT_INT, int(num_str)), curr_pos
    else:
        return Token(TokenTypes.TT_FLOAT, float(num_str)), curr_pos

def get_curr_char(text:str='', curr_pos:Position = Position()):
    return text[curr_pos.idx] if curr_pos.idx < len(text) else None

def run(fn:str='', text:str=''):
    tokens, error = make_tokens([], Position(0, 0, 0, fn, text), text)
    if error: return None, error
    return clean_tokens(tokens), error
    # print(tokens)
    # return tokens, error