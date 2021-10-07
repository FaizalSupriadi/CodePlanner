from typing import List, Tuple
from myLexer import Token
from myLexer import TokenTypes
import myLexer


class Node:
    def __init__(self, node_name='Node') -> None:
            self.node_name = node_name

    def __repr__(self) -> str:
        return f'{self.node_name}: {self.node_name}'


class VarAccesNode(Node):
    def __init__(self, var_name_tok: any) -> None:
        super().__init__('VarAccesNode')
        self.var_name_tok=var_name_tok

    def __repr__(self) -> str:
        return f'{self.node_name}: {self.var_name_tok}'


class VarAssignNode(Node):
    def __init__(self, var_name_tok: any, value_node: any) -> None:
        super().__init__('VarAssignNode')
        self.var_name_tok=var_name_tok
        self.value_node=value_node
    def __repr__(self) -> str:
        return f'{self.node_name}: {self.var_name_tok}, {self.value_node}'


class NumberNode(Node):
    def __init__(self, tok: Token) -> None:
        super().__init__('NumberNode')
        self.tok=tok
    def __repr__(self) -> str:
        return f'{self.node_name}: {self.tok}'


class BinOpNode(Node):
    def __init__(self, left_node: any, op_tok: Token, right_node: any) -> None:
        super().__init__('BinOpNode')
        self.left_node=left_node
        self.op_tok=op_tok
        self.right_node=right_node
    def __repr__(self) -> str:
        return f'({self.node_name}: {self.left_node}, {self.op_tok}, {self.right_node})'


class UnaryOpNode(Node):
    def __init__(self, op_tok: Token, node: any) -> None:
        super().__init__('UnaryOpNode')
        self.op_tok=op_tok
        self.node=node
    def __repr__(self) -> str:
        return f'({self.node_name}: {self.op_tok}, {self.node})'

class IfNode(Node):
    def __init__(self, cases, else_case):
        super().__init__('IfNode')
        self.cases = cases
        self.else_case = else_case
    def __repr__(self) -> str:
        return f'({self.node_name}: {self.cases}, {self.else_case})'

class ForNode(Node):
    def __init__(self, var_name_tok, start_value_node, end_value_node, step_value_node, body_node):
        super().__init__('ForNode')
        self.var_name_tok = var_name_tok
        self.start_value_node = start_value_node
        self.end_value_node = end_value_node
        self.step_value_node = step_value_node
        self.body_node = body_node

    def __repr__(self) -> str:
        return f'({self.node_name}: {self.var_name_tok}, {self.start_value_node}, {self.end_value_node}, {self.step_value_node}, BODY: {self.body_node})'
class WhileNode(Node):
    def __init__(self, condition_node, body_node):
        super().__init__('WhileNode')
        self.condition_node = condition_node
        self.body_node = body_node
    
    def __repr__(self) -> str:
        return f'({self.node_name}: {self.condition_node}, body_node:{self.body_node})'

class FuncDefNode(Node):
    def __init__(self, var_name_tok, arg_name_toks, body_node):
        super().__init__('FuncDefNode')
        self.var_name_tok = var_name_tok
        self.arg_name_toks = arg_name_toks
        self.body_node = body_node

    def __repr__(self) -> str:
        return f'({self.node_name}: {self.var_name_tok}, arg_name_toks{self.arg_name_toks}, body_node:{self.body_node})'
class CallNode(Node):
    def __init__(self, node_to_call, arg_nodes):
        super().__init__('CallNode')
        self.node_to_call = node_to_call
        self.arg_nodes = arg_nodes

    def __repr__(self) -> str:
        return f'({self.node_name}: {self.node_to_call}, arg_nodes:{self.arg_nodes})'

def not_keyword_check(tokens: List[Token] = [], idx: int = 0, keyword:str='', func: callable = None) -> Tuple[any, int]:
    curr_tok: Token = get_curr_tok(tokens, idx)
    if not curr_tok.matches(TokenTypes.TT_KEYWORD, keyword):
        return None, idx
    return func(tokens, idx+1)

def parse(tokens: List[Token] = []) -> any:
    return expression(tokens)

def func_def(tokens: List[Token] = [], idx: int = 0) -> Tuple[any, int]:
    if not get_curr_tok(tokens, idx).matches(TokenTypes.TT_KEYWORD, 'ROUTE'):
        return None, idx
    curr_tok:Token = get_curr_tok(tokens, idx+1)
    if curr_tok.type == TokenTypes.TT_IDENTIFIER:
        if get_curr_tok(tokens, idx+2).type != TokenTypes.TT_LPAREN:
            return None, idx+2
        curr_tok_1:Token = get_curr_tok(tokens, idx+3)
        if curr_tok_1.type == TokenTypes.TT_IDENTIFIER:
            arg_list, idx_1 = func_def_inputs(tokens, idx+3, [curr_tok_1])
            if get_curr_tok(tokens, idx_1).type != TokenTypes.TT_RPAREN:
                return None, idx_1
            return func_def_colon(tokens, idx_1+1, curr_tok,arg_list)

        else:
            if get_curr_tok(tokens, idx+3).type != TokenTypes.TT_RPAREN:
                return None, idx+3
            return func_def_colon(tokens, idx+4, curr_tok,[])
    else:
        if get_curr_tok(tokens, idx+1) != TokenTypes.TT_LPAREN:
            return None, idx+1
        curr_tok_1:Token = get_curr_tok(tokens, idx+2)
        if curr_tok_1.type == TokenTypes.TT_IDENTIFIER:
            arg_list, idx_1 = func_def_inputs(tokens, idx, [curr_tok_1])
            if get_curr_tok(tokens, idx_1).type != TokenTypes.TT_RPAREN:
                return None, idx_1
            return func_def_colon(tokens, idx_1, curr_tok)
        else:
            if get_curr_tok(tokens, idx+2).type != TokenTypes.TT_RPAREN:
                return None, idx+2
            return func_def_colon(tokens, idx+2, curr_tok,[])


def func_def_colon(tokens: List[Token] = [], idx: int = 0, var_name:Token=Token(),arg_list:list=[]):
    if get_curr_tok(tokens, idx).type != TokenTypes.TT_COLON:
        return None, idx
    node_to_return, idx_1 = expression(tokens, idx+1)
    return FuncDefNode(var_name, arg_list ,node_to_return), idx_1

def func_def_inputs(tokens: List[Token] = [], idx: int = 0, arg_name_toks:list=[]):
    if get_curr_tok(tokens, idx+1).type == TokenTypes.TT_COMMA:
        curr_tok:Token = get_curr_tok(tokens, idx+2)
        if curr_tok.type != TokenTypes.TT_IDENTIFIER:
            return arg_name_toks, idx+2
        arg_name_toks.append(curr_tok)
    else:
        return arg_name_toks, idx+1
    return func_def_inputs(tokens, idx+2, arg_name_toks)

def call(tokens: List[Token] = [], idx: int = 0):
    fact, idx_1 = factor(tokens, idx)
    print(get_curr_tok(tokens, idx_1))
    if get_curr_tok(tokens, idx_1).type == TokenTypes.TT_LPAREN:
        if get_curr_tok(tokens, idx_1+1).type == TokenTypes.TT_RPAREN:
            return CallNode(fact, []), idx_1+1
        else:
            expr, idx_2 = expression(tokens,idx_1+1)
            print('exxxx',expr)
            arg_nodes, idx_3 = call_inputs(tokens, idx_2, [expr])
            if get_curr_tok(tokens, idx_3).type != TokenTypes.TT_RPAREN:
                return None, idx_3
            print(arg_nodes)
            return CallNode(fact, arg_nodes), idx_3
    return fact, idx_1

def call_inputs(tokens: List[Token] = [], idx: int = 0, arg_nodes:list = []):
    print(get_curr_tok(tokens, idx))
    if get_curr_tok(tokens, idx).type == TokenTypes.TT_COMMA:
        expr, idx_1 = expression(tokens, idx+1)
        arg_nodes.append(expr)
        print('expr!',expr)
        return call_inputs(tokens, idx_1, arg_nodes)
    return arg_nodes, idx

def for_expr(tokens: List[Token] = [], idx: int = 0) -> Tuple[Node, int]:
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

def while_expr(tokens: List[Token] = [], idx: int = 0) -> Tuple[Node, int]:
    condition, idx_1 = not_keyword_check(tokens, idx, 'WHILE', expression)
    body, idx_2 = not_keyword_check(tokens, idx_1, 'THEN', expression)
    return WhileNode(condition, body), idx_2

def if_expr(tokens: List[Token] = [], idx: int = 0) -> Tuple[Node, int]:
    cases = []
    condition, idx_1 = not_keyword_check(tokens, idx, 'IF', expression)
    expr, idx_2 = not_keyword_check(tokens, idx_1, 'THEN', expression)
    cases.append((condition, expr))
    return if_expr_loop(tokens, idx_2, cases)
        

def if_expr_loop(tokens, idx, cases=[]) -> Tuple[Node, int]:
    
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

def comp_expr(tokens: List[Token] = [], idx: int = 0) -> Tuple[Node, int]:
    curr_tok: Token = get_curr_tok(tokens, idx)
    if curr_tok.matches(TokenTypes.TT_KEYWORD, 'NOT'):
        exp, idx_1 = comp_expr(tokens, idx+1)
        return UnaryOpNode(curr_tok, exp), idx_1
    return bin_op_left(arith_expr, (TokenTypes.TT_EE, TokenTypes.TT_NE, TokenTypes.TT_LT, TokenTypes.TT_GT, TokenTypes.TT_LTE, TokenTypes.TT_GTE), tokens, idx)

def arith_expr(tokens: List[Token] = [], idx: int = 0) -> Tuple[Node, int]:
    return bin_op_left(term, (TokenTypes.TT_PLUS, TokenTypes.TT_MINUS), tokens, idx)

def expression(tokens: List[Token] = [], idx: int = 0) -> Tuple[Node, int]:
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
    return bin_op_left(call, (TokenTypes.TT_MUL, TokenTypes.TT_DIV), tokens, idx)


def factor(tokens: List[Token] = [], idx: int = 0) -> Tuple[Node, int]:
    curr_tok: Token = get_curr_tok(tokens, idx)

    if curr_tok is None:
        return None, idx
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
    elif curr_tok.matches(TokenTypes.TT_KEYWORD, 'ROUTE'):
        return func_def(tokens,idx)
    return bin_op_left(call, (), tokens, idx)


def bin_op_left(func: callable, ops: tuple, tokens: List[Token] = [], idx: int = 0) -> Tuple[Node, int]: # dit zijn hoge orde functies
    funct, i = func(tokens, idx)
    return bin_op_right(func, ops, tokens, i, funct)


def bin_op_right(func: callable, ops: tuple, tokens: List[Token], idx: int, left: any) -> Tuple[Node, int]:
    curr_tok: Token = get_curr_tok(tokens, idx)
    if curr_tok is None:
        return left, idx

    if curr_tok.type in ops or (curr_tok.type, curr_tok.value) in ops:
        right, i = func(tokens, idx+1)
        return bin_op_right(func, ops, tokens, i, BinOpNode(left, curr_tok, right))
    return left, idx

def get_curr_tok(tokens:List[Token]=[], idx:int=0) -> Token:
    return tokens[idx] if idx < len(tokens) else Token()

def run(fn: str = '', text: str = '') -> Node:
    tokens, error = myLexer.run(fn, text)
    print('TOKENS:', tokens)
    if error:
        return None, error
    ast, _ = parse(tokens)

    return ast
