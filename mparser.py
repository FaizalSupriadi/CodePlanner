from typing import List
from example import Token
from example import TokenTypes
from example import InvalidSyntaxError
from example import Position
from example import make_tokens
from example import clean_tokens

class NumberNode:
    def __init__(self, tok) -> None:
        self.tok = tok

    def __repr__(self) -> str:
        return f'{self.tok}'
    
class BinOpNode:
    def __init__(self, left_node, op_tok, right_node) -> None:
        self.left_node = left_node
        self.op_tok = op_tok
        self.right_node = right_node

    def __repr__(self) -> str:
        return f'({self.left_node}, {self.op_tok}, {self.right_node})'

class UnaryOpNode:
	def __init__(self, op_tok, node):
		self.op_tok = op_tok
		self.node = node

	def __repr__(self):
		return f'({self.op_tok}, {self.node})'

def parse(tokens):
    expr = expression(tokens)
    return expr

def expression(tokens=[],idx=0):
    print('expr1')
    exp, i = bin_op_left(term, (TokenTypes.TT_PLUS, TokenTypes.TT_MINUS), tokens, idx)
    print('expr', exp)
    return exp, i
def term(tokens,idx):
    print('term1')
    ter, i = bin_op_left(factor, (TokenTypes.TT_MUL, TokenTypes.TT_DIV),tokens, idx)
    print('term',ter)
    return ter, i
def factor(tokens,idx):
    print('facts')
    curr_tok:Token = tokens[idx] if idx < len(tokens) else None
    if curr_tok is None: return None, idx+1

    if curr_tok.type in (TokenTypes.TT_PLUS, TokenTypes.TT_MINUS):
        return UnaryOpNode(curr_tok, factor(tokens, idx+1)), idx+1

    elif curr_tok.type in (TokenTypes.TT_INT, TokenTypes.TT_FLOAT):
        return NumberNode(curr_tok), idx+1
    elif curr_tok.type == TokenTypes.TT_LPAREN:
        expr, i = expression(tokens, idx+1)
        print('fact_exp', expr)
        next_tok:Token = tokens[i] if i < len(tokens) else None
        if next_tok == None: return None, i
        if next_tok.type == TokenTypes.TT_RPAREN:
            return expr, i+1
    return None, idx

def bin_op_left(func, ops, tokens, idx):
    funct, i = func(tokens, idx)
    print('bin_left','idx', idx,'f', func,'left', funct, 'i', i)
    return bin_op_right(func, ops, tokens, i, funct)


def bin_op_right(func, ops, tokens, idx, left):
    print('bin_op_right',tokens, idx)
    curr_tok = tokens[idx] if idx < len(tokens) else None
    if curr_tok is None: return left, idx
    print('ops',ops)
    if curr_tok.type in ops:
        op_tok = curr_tok
        right, i = func(tokens, idx+1)
        print('right', right, 'i', i)
        return bin_op_right(func, ops, tokens, i, BinOpNode(left, op_tok, right))
    return left, idx

def run(fn, text:str):
    pos = Position(0, 0, 0, fn, text)
    tokens, error = make_tokens([],pos, text)
    if error: return None, error
    tokens = clean_tokens(tokens)

    ast, _ = parse(tokens)
    return ast, None