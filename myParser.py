from typing import List
from myLexer import Token
from myLexer import TokenTypes
import myLexer


class Node:
    def __init__(
        self, tok: Token = Token(), left_node: any = None,
        op_tok: Token = Token(), right_node: any = None, node: any = None,
        var_name_tok: any = None, value_node: any = None, cases: list = [], else_case: list = [],
        start_value_node:any=None, end_value_node:any=None, step_value_node:any=None, body_node:any=None,
        condition_node:any=None) -> None:
            self.tok = tok
            self.left_node = left_node
            self.op_tok = op_tok
            self.right_node = right_node
            self.node = node
            self.var_name_tok = var_name_tok
            self.value_node = value_node
            self.cases = cases
            self.else_case = else_case
            self.var_name_tok
            self.start_value_node = start_value_node
            self.end_value_node = end_value_node
            self.step_value_node = step_value_node
            self.body_node = body_node
            self.condition_node = condition_node
    def __repr__(self) -> str:
        return f'NODE: {self.tok}'


class VarAccesNode(Node):
    def __init__(self, var_name_tok: any) -> None:
        super().__init__(var_name_tok=var_name_tok)

    def __repr__(self) -> str:
        return f'VarAccesNode: {self.var_name_tok}'


class VarAssignNode(Node):
    def __init__(self, var_name_tok: any, value_node: any) -> None:
        super().__init__(var_name_tok=var_name_tok, value_node=value_node)

    def __repr__(self) -> str:
        return f'VarAssignNode: {self.var_name_tok}, {self.value_node}'


class NumberNode(Node):
    def __init__(self, tok: Token) -> None:
        super().__init__(tok=tok)

    def __repr__(self) -> str:
        return f'NumberNode: {self.tok}'


class BinOpNode(Node):
    def __init__(self, left_node: any, op_tok: Token, right_node: any) -> None:
        super().__init__(left_node=left_node, op_tok=op_tok, right_node=right_node)

    def __repr__(self) -> str:
        return f'(BinOpNode: {self.left_node}, {self.op_tok}, {self.right_node})'


class UnaryOpNode(Node):
    def __init__(self, op_tok: Token, node: any) -> None:
        super().__init__(op_tok=op_tok, node=node)

    def __repr__(self) -> str:
        return f'(UnaryOpNode: {self.op_tok}, {self.node})'

class IfNode(Node):
    def __init__(self, cases, else_case):
        self.cases = cases
        self.else_case = else_case
    def __repr__(self) -> str:
        return f'(IFNODE: {self.cases}, {self.else_case})'

class ForNode(Node):
    def __init__(self, var_name_tok, start_value_node, end_value_node, step_value_node, body_node):
        self.var_name_tok = var_name_tok
        self.start_value_node = start_value_node
        self.end_value_node = end_value_node
        self.step_value_node = step_value_node
        self.body_node = body_node

    def __repr__(self) -> str:
        return f'(FORNODE: {self.var_name_tok}, {self.start_value_node}, {self.end_value_node}, {self.step_value_node}, BODY: {self.body_node})'
class WhileNode(Node):
    def __init__(self, condition_node, body_node):
        self.condition_node = condition_node
        self.body_node = body_node
    
    def __repr__(self) -> str:
        return f'(WhileNode: {self.condition_node}, body_node:{self.body_node})'

def not_keyword_check(tokens: List[Token] = [], idx: int = 0, keyword:str='', func: callable = None):
    curr_tok: Token = get_curr_tok(tokens, idx)
    if not curr_tok.matches(TokenTypes.TT_KEYWORD, keyword):
        return None, idx
    return func(tokens, idx+1)

def parse(tokens: List[Token] = []) -> any:
    return expression(tokens)

def for_expr(tokens: List[Token] = [], idx: int = 0) -> tuple:
    curr_tok: Token = get_curr_tok(tokens, idx)
    if not curr_tok.matches(TokenTypes.TT_KEYWORD, 'FOR'):
        return None, idx
    
    curr_tok_1: Token = get_curr_tok(tokens, idx+1)
    if curr_tok_1.type != TokenTypes.TT_IDENTIFIER:
        return None, idx+1
    
    curr_tok_2: Token = get_curr_tok(tokens, idx+2)
    if curr_tok_2.type != TokenTypes.TT_EQ:
        return None, idx+2
    start_value, idx_1 = expression(tokens, idx+3)
    end_value, idx_2 = not_keyword_check(tokens, idx_1, 'TO', expression)
    curr_tok_3: Token = get_curr_tok(tokens, idx_2)
    if curr_tok_3.matches(TokenTypes.TT_KEYWORD, 'STEP'):
        step_value, idx_3 = expression(tokens, idx_2)
        body, idx_4 = expression(tokens, idx_3)
        return ForNode(curr_tok_2, start_value, end_value, step_value, body), idx_4
    else: 
        body, idx_3 = expression(tokens, idx_2+1)
        return ForNode(curr_tok_1, start_value, end_value, None, body), idx_3

def while_expr(tokens: List[Token] = [], idx: int = 0) -> tuple:
    condition, idx_1 = not_keyword_check(tokens, idx, 'WHILE', expression)
    body, idx_2 = not_keyword_check(tokens, idx_1, 'THEN', expression)
    return WhileNode(condition, body), idx_2

def if_expr(tokens: List[Token] = [], idx: int = 0) -> tuple:
    cases = []
    condition, idx_1 = not_keyword_check(tokens, idx, 'IF', expression)
    expr, idx_2 = not_keyword_check(tokens, idx_1, 'THEN', expression)
    cases.append((condition, expr))
    return if_expr_loop(tokens, idx_2, cases)
        

def if_expr_loop(tokens, idx, cases=[]):
    
    curr_tok: Token = get_curr_tok(tokens, idx)
    if curr_tok.matches(TokenTypes.TT_KEYWORD, 'ELIF'):
        condition, idx_1 = expression(tokens, idx+1)
        expr, idx_2 = not_keyword_check(tokens, idx_1, 'THEN', expression)
        cases.append((condition, expr))
        return if_expr_loop(tokens, idx_2, cases)
    elif curr_tok.matches(TokenTypes.TT_KEYWORD, 'ELSE'):
        else_case, idx_2 = expression(tokens, idx + 1)
        return IfNode(cases, else_case), idx_2
    return IfNode(cases, []), idx

def comp_expr(tokens: List[Token] = [], idx: int = 0) -> tuple:
    curr_tok: Token = get_curr_tok(tokens, idx)
    if curr_tok.matches(TokenTypes.TT_KEYWORD, 'NOT'):
        exp, idx_1 = comp_expr(tokens, idx+1)
        return UnaryOpNode(curr_tok, exp), idx_1
    return bin_op_left(arith_expr, (TokenTypes.TT_EE, TokenTypes.TT_NE, TokenTypes.TT_LT, TokenTypes.TT_GT, TokenTypes.TT_LTE, TokenTypes.TT_GTE), tokens, idx)

def arith_expr(tokens: List[Token] = [], idx: int = 0) -> tuple:
    return bin_op_left(term, (TokenTypes.TT_PLUS, TokenTypes.TT_MINUS), tokens, idx)

def expression(tokens: List[Token] = [], idx: int = 0) -> tuple:
    curr_tok: Token = get_curr_tok(tokens, idx)
    if curr_tok.matches(TokenTypes.TT_KEYWORD, 'VEHICLE'):
        next_tok: Token = get_curr_tok(tokens, idx+1)
        if next_tok.type != TokenTypes.TT_IDENTIFIER:
            return None, idx+1
        next_next_tok: Token = get_curr_tok(tokens, idx+2)
        if next_next_tok.type != TokenTypes.TT_EQ:
            return None, idx+2
        expr, idx_1 = expression(tokens, idx+3)
        return VarAssignNode(next_tok, expr), idx_1
    return bin_op_left(comp_expr, ((TokenTypes.TT_KEYWORD, "AND"),(TokenTypes.TT_KEYWORD, "OR")), tokens, idx)


def term(tokens: List[Token] = [], idx: int = 0) -> tuple:
    return bin_op_left(factor, (TokenTypes.TT_MUL, TokenTypes.TT_DIV), tokens, idx)


def factor(tokens: List[Token] = [], idx: int = 0) -> tuple:
    curr_tok: Token = get_curr_tok(tokens, idx)
    if curr_tok is None:
        return None, idx+1
    if curr_tok.type in (TokenTypes.TT_PLUS, TokenTypes.TT_MINUS):
        facts, idx_1 = factor(tokens, idx+1)
        return UnaryOpNode(curr_tok, facts), idx_1
    elif curr_tok.type == TokenTypes.TT_IDENTIFIER:
        return VarAccesNode(curr_tok), idx+1
    elif curr_tok.type in (TokenTypes.TT_INT, TokenTypes.TT_FLOAT):
        return NumberNode(curr_tok), idx+1
    elif curr_tok.type == TokenTypes.TT_LPAREN:
        expr, idx_1 = expression(tokens, idx+1)
        next_tok: Token = get_curr_tok(tokens, idx_1)
        if next_tok == None:
            return None, idx_1
        elif next_tok.type == TokenTypes.TT_RPAREN:
            return expr, idx_1+1
    elif curr_tok.matches(TokenTypes.TT_KEYWORD, 'IF'):
        return if_expr(tokens,idx)
    elif curr_tok.matches(TokenTypes.TT_KEYWORD, 'FOR'):
        return for_expr(tokens,idx)
    elif curr_tok.matches(TokenTypes.TT_KEYWORD, 'WHILE'):
        return while_expr(tokens,idx)
    return None, idx


def bin_op_left(func: callable, ops: tuple, tokens: List[Token] = [], idx: int = 0) -> tuple:
    funct, i = func(tokens, idx)
    return bin_op_right(func, ops, tokens, i, funct)


def bin_op_right(func: callable, ops: tuple, tokens: List[Token], idx: int, left: any) -> tuple:
    curr_tok: Token = get_curr_tok(tokens, idx)
    if curr_tok is None:
        return left, idx

    if curr_tok.type in ops or (curr_tok.type, curr_tok.value) in ops:
        right, i = func(tokens, idx+1)
        return bin_op_right(func, ops, tokens, i, BinOpNode(left, curr_tok, right))
    return left, idx

def get_curr_tok(tokens:List[Token]=[], idx:int=0) -> Token or None:
    return tokens[idx] if idx < len(tokens) else Token()

def run(fn: str = '', text: str = '') -> tuple:
    tokens, error = myLexer.run(fn, text)
    print('TOKENS:', tokens)
    if error:
        return None, error
    ast, _ = parse(tokens)

    return ast, None
