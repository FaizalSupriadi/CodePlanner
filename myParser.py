from typing import List
from myLexer import Token
from myLexer import TokenTypes
from myLexer import Position
from myLexer import make_tokens
from myLexer import clean_tokens
import myLexer


class Node:
    def __init__(
        self, tok: Token = None, left_node: any = None,  
        op_tok: Token = None, right_node: any = None, node: any = None,
        var_name_tok:any = None,value_node:any=None ) -> None:
            self.tok = tok
            self.left_node = left_node
            self.op_tok = op_tok
            self.right_node = right_node
            self.node = node
            self.var_name_tok = var_name_tok
            self.value_node = value_node

    def __repr__(self) -> str:
        return f'{self.tok}'

class VarAccesNode(Node):
    def __init__(self, var_name_tok: any) -> None:
        super().__init__(var_name_tok=var_name_tok)

    def __repr__(self) -> str:
        return f'{self.var_name_tok}, {self.value_node}'
class VarAssignNode(Node):
    def __init__(self, var_name_tok:any, value_node: any) -> None:
        super().__init__(var_name_tok=var_name_tok, value_node=value_node)

    def __repr__(self) -> str:
        return f'{self.var_name_tok}, {self.value_node}'
class NumberNode(Node):
    def __init__(self, tok: Token) -> None:
        super().__init__(tok=tok)

    def __repr__(self) -> str:
        return f'{self.tok}'


class BinOpNode(Node):
    def __init__(self, left_node: any, op_tok: Token, right_node: any) -> None:
        super().__init__(left_node=left_node, op_tok=op_tok, right_node=right_node)

    def __repr__(self) -> str:
        return f'({self.left_node}, {self.op_tok}, {self.right_node})'


class UnaryOpNode(Node):
    def __init__(self, op_tok: Token, node: any) -> None:
        super().__init__(op_tok=op_tok, node=node)

    def __repr__(self) -> str:
        return f'({self.op_tok}, {self.node})'


def parse(tokens: List[Token] = []) -> any:
    expr, _ = expression(tokens)
    return expr


def expression(tokens: List[Token] = [], idx: int = 0) -> tuple:
    # #print('expr1')
    curr_tok: Token = tokens[idx] if idx < len(tokens) else None
    #print(curr_tok)
    if curr_tok.matches(TokenTypes.TT_KEYWORD, 'VEHICLE'):
        next_tok: Token = tokens[idx+1] if idx+1 < len(tokens) else None
        if next_tok.type != TokenTypes.TT_IDENTIFIER:
            return None, idx
        vehicle_name = next_tok
        next_next_tok: Token = tokens[idx+2] if idx+2 < len(tokens) else None

        if next_next_tok.type != TokenTypes.TT_EQ:
            return None, idx
        expr,_ = expression(tokens, idx+3)
        #print('ex', expr)
        return VarAssignNode(vehicle_name, expr), idx+3

    exp, i = bin_op_left(
        term, (TokenTypes.TT_PLUS, TokenTypes.TT_MINUS), tokens, idx)
    # #print('expr', exp)
    return exp, i


def term(tokens: List[Token] = [], idx: int = 0) -> tuple:
    # #print('term1')
    ter, i = bin_op_left(
        factor, (TokenTypes.TT_MUL, TokenTypes.TT_DIV), tokens, idx)
    # #print('term', ter)
    return ter, i


def factor(tokens: List[Token] = [], idx: int = 0) -> tuple:
    # #print('facts')
    curr_tok: Token = tokens[idx] if idx < len(tokens) else None
    #print('fac cur',curr_tok.type)
    if curr_tok is None:
        return None, idx+1

    if curr_tok.type in (TokenTypes.TT_PLUS, TokenTypes.TT_MINUS):
        facts, i = factor(tokens, idx+1)
        return UnaryOpNode(curr_tok, facts), i
    elif curr_tok.type == TokenTypes.TT_IDENTIFIER:
        #print('yep', curr_tok)
        return VarAccesNode(curr_tok), idx+1
    elif curr_tok.type in (TokenTypes.TT_INT, TokenTypes.TT_FLOAT):
        return NumberNode(curr_tok), idx+1

    elif curr_tok.type == TokenTypes.TT_LPAREN:
        expr, i = expression(tokens, idx+1)
        # #print('fact_exp', expr)
        next_tok: Token = tokens[i] if i < len(tokens) else None
        if next_tok == None:
            return None, i
        if next_tok.type == TokenTypes.TT_RPAREN:
            return expr, i+1
    return None, idx


def bin_op_left(func: callable, ops: tuple, tokens: List[Token] = [], idx: int = 0) -> tuple:
    funct, i = func(tokens, idx)
    #print('bin_left', 'idx', idx, 'f', func, 'left', funct, 'i', i)
    return bin_op_right(func, ops, tokens, i, funct)


def bin_op_right(func: callable, ops: tuple, tokens: List[Token], idx: int, left: any) -> tuple:
    # #print('bin_op_right', tokens, idx)
    curr_tok: Token = tokens[idx] if idx < len(tokens) else None
    if curr_tok is None:
        return left, idx
    # #print('ops', ops)
    if curr_tok.type in ops:
        op_tok = curr_tok
        right, i = func(tokens, idx+1)
        #print('right', right, 'i', i)
        return bin_op_right(func, ops, tokens, i, BinOpNode(left, op_tok, right))
    return left, idx


def run(fn: str = '', text: str = '') -> tuple:
    tokens, error = myLexer.run(fn, text)
    if error:
        return None, error
    ast = parse(tokens)
    print('parse ast',type(ast))
    print('ast1',type(ast.left_node),type(ast.op_tok),type(ast.right_node) )
    #print('norm', ast)
    return ast, None
