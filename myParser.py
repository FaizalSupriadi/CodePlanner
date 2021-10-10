from typing import List, Tuple
from myLexer import Token
from myLexer import TokenTypes
import myLexer


class Node:
    def __init__(self, node_name='NODE') -> None:
            self.node_name = node_name

    def __repr__(self) -> str:
        return f'{self.node_name}: {self.node_name}'


class VarAccesNode(Node):
    def __init__(self, var_name_tok: any) -> None:
        super().__init__('VARACCESNODE')
        self.var_name_tok=var_name_tok

    def __repr__(self) -> str:
        return f'{self.node_name}: {self.var_name_tok}'


class VarAssignNode(Node):
    def __init__(self, var_name_tok: any, value_node: any) -> None:
        super().__init__('VARASSIGNNODE')
        self.var_name_tok=var_name_tok
        self.value_node=value_node
    def __repr__(self) -> str:
        return f'{self.node_name}: {self.var_name_tok}, {self.value_node}'


class NumberNode(Node):
    def __init__(self, tok: Token) -> None:
        super().__init__('NUMBERNODE')
        self.tok=tok
    def __repr__(self) -> str:
        return f'{self.node_name}: {self.tok}'


class BinOpNode(Node):
    def __init__(self, left_node: any, op_tok: Token, right_node: any) -> None:
        super().__init__('BINOPNODE')
        self.left_node=left_node
        self.op_tok=op_tok
        self.right_node=right_node
    def __repr__(self) -> str:
        return f'({self.node_name}: {self.left_node}, {self.op_tok}, {self.right_node})'


class UnaryOpNode(Node):
    def __init__(self, op_tok: Token, node: any) -> None:
        super().__init__('UNARYOPNODE')
        self.op_tok=op_tok
        self.node=node
    def __repr__(self) -> str:
        return f'({self.node_name}: {self.op_tok}, {self.node})'

class IfNode(Node):
    def __init__(self, cases, else_case):
        super().__init__('IFNODE')
        self.cases = cases
        self.else_case = else_case
    def __repr__(self) -> str:
        return f'({self.node_name}: {self.cases}, ELSECASE: {self.else_case})'

class ForNode(Node):
    def __init__(
        self, var_name_tok, start_value_node, end_value_node, 
        step_value_node, body_node, should_return_null
        ):
        super().__init__('FORNODE')
        self.var_name_tok = var_name_tok
        self.start_value_node = start_value_node
        self.end_value_node = end_value_node
        self.step_value_node = step_value_node
        self.body_node = body_node
        self.should_return_null = should_return_null

    def __repr__(self) -> str:
        return f'({self.node_name}: {self.var_name_tok}, {self.start_value_node}, {self.end_value_node}, {self.step_value_node}, BODY: {self.body_node})'
class WhileNode(Node):
    def __init__(self, condition_node, body_node, should_return_null):
        super().__init__('WHILENODE')
        self.condition_node = condition_node
        self.body_node = body_node
        self.should_return_null = should_return_null
    def __repr__(self) -> str:
        return f'({self.node_name}: {self.condition_node}, body_node:{self.body_node})'

class FuncDefNode(Node):
    def __init__(self, var_name_tok, arg_name_toks, body_node, should_return_null):
        super().__init__('FUNCDEFNODE')
        self.var_name_tok = var_name_tok
        self.arg_name_toks = arg_name_toks
        self.body_node = body_node
        self.should_return_null = should_return_null
    def __repr__(self) -> str:
        return f'({self.node_name}: {self.var_name_tok}, arg_name_toks{self.arg_name_toks}, body_node:{self.body_node})'
class CallNode(Node):
    def __init__(self, node_to_call, arg_nodes):
        super().__init__('CALLNODE')
        self.node_to_call = node_to_call
        self.arg_nodes = arg_nodes

    def __repr__(self) -> str:
        return f'({self.node_name}: {self.node_to_call}, arg_nodes:{self.arg_nodes})'

class ListNode(Node):
    def __init__(self, element_nodes):
        super().__init__('LISTNODE')
        self.element_nodes = element_nodes

    def __repr__(self) -> str:
        return f'({self.node_name}: ELEMNODES: {self.element_nodes})'
class ReturnNode(Node):
    def __init__(self, node_to_return):
        super().__init__('RETURNNODE')

        self.node_to_return = node_to_return
    def __repr__(self) -> str:
        return f'({self.node_name}: {self.node_to_return})'
class ContinueNode(Node):
    def __init__(self):
        super().__init__('CONTINUENODE')

    def __repr__(self) -> str:
        return f'({self.node_name})'
class BreakNode(Node):
    def __init__(self):
        super().__init__('BREAKNODE')

    def __repr__(self) -> str:
        return f'({self.node_name})'

class PrintNode(Node):
    def __init__(self, printable):
        super().__init__('PRINTNODE')
        self.printable = printable

    def __repr__(self) -> str:
        return f'({self.node_name}, {self.printable})'
def not_keyword_check(tokens: List[Token] = [], idx: int = 0, keyword:str='', func: callable = None) -> Tuple[any, int]:
    if not get_curr_tok(tokens, idx).matches(TokenTypes.TT_KEYWORD, keyword):
        return None, idx
    return func(tokens, idx+1)

def parse(tokens: List[Token] = []) -> any:
    return statements(tokens)

def statements( tokens: List[Token] = [], idx: int = 0 ):
    #print('statements',get_curr_tok(tokens, idx))
    if len(tokens) == 0: return None, 0
    statements_list = []
    _, idx_1 = if_newline(tokens, idx, 0)
    statement, idx_2 = statement_keywords(tokens, idx_1)
    #print('sfdas')
    statements_list.append(statement)
    statements_list_1, idx_3 = statement_loop(tokens, idx_2, statements_list)
    return ListNode(statements_list_1), idx_3

def statement_loop(tokens: List[Token] = [], idx: int = 0, statements_list:list = []):
    #print('statement_loop',get_curr_tok(tokens, idx))
    count, idx_1 = if_newline(tokens, idx, 0)
    if count == 0:
        return statements_list, idx_1
    statement, idx_2 = statement_keywords(tokens, idx_1)
    if not statement:
        return statements_list, idx_2
    statements_list.append(statement)
    return statement_loop(tokens, idx_2, statements_list )

def statement_keywords(tokens: List[Token] = [], idx: int = 0):
    #print('statement_keywords',get_curr_tok(tokens, idx))
    if get_curr_tok(tokens, idx).matches(TokenTypes.TT_KEYWORD, 'RETURN'):
        expr, idx_1 = expression(tokens, idx+1)
        #print('asdasdasd',get_curr_tok(tokens, idx_1))
        return ReturnNode(expr), idx_1
    if get_curr_tok(tokens, idx).matches(TokenTypes.TT_KEYWORD, 'CONTINUE'):
        return ContinueNode(), idx+1    
    if get_curr_tok(tokens, idx).matches(TokenTypes.TT_KEYWORD, 'BREAK'):
        return BreakNode(), idx+1
    if get_curr_tok(tokens, idx).matches(TokenTypes.TT_KEYWORD, 'PRINT'):
        
        expr, idx_1 = expression(tokens, idx+1)
        #print('TEST',expr,get_curr_tok(tokens, idx+1))
        return PrintNode(expr), idx_1
    expr, idx_1 = expression(tokens, idx)
    return expr, idx_1
    
def if_newline(tokens: List[Token] = [], idx: int = 0, count:int = 0):
    #print('if_newline',get_curr_tok(tokens, idx))
    curr_tok:Token = get_curr_tok(tokens, idx)
    if curr_tok.type == None:
        return 0, idx
    elif curr_tok.type == TokenTypes.TT_NEWLINE:
        return if_newline(tokens,idx+1, count+1)

    return count, idx

def func_def_if(tokens: List[Token] = [], idx: int = 0, curr_tok:Token=Token()):
    #print('func_def_if',get_curr_tok(tokens, idx))
    if get_curr_tok(tokens, idx).type != TokenTypes.TT_LPAREN:
        return None, idx
    curr_tok_1:Token = get_curr_tok(tokens, idx+1)
    if curr_tok_1.type == TokenTypes.TT_IDENTIFIER:
        arg_list, idx_1 = func_def_inputs(tokens, idx+2, [curr_tok_1])
        if get_curr_tok(tokens, idx_1).type != TokenTypes.TT_RPAREN:
            return None, idx_1
        return func_def_colon(tokens, idx_1+1, curr_tok,arg_list)

    else:
        if get_curr_tok(tokens, idx+1).type != TokenTypes.TT_RPAREN:
            return None, idx+1
        return func_def_colon(tokens, idx+2, curr_tok,[])

def func_def_else(tokens: List[Token] = [], idx: int = 0, curr_tok:Token=Token()):
    #print('func_def_else',get_curr_tok(tokens, idx))
    if get_curr_tok(tokens, idx) != TokenTypes.TT_LPAREN:
            return None, idx
    curr_tok_1:Token = get_curr_tok(tokens, idx+2)
    if curr_tok_1.type == TokenTypes.TT_IDENTIFIER:
        arg_list, idx_1 = func_def_inputs(tokens, idx, [curr_tok_1])
        if get_curr_tok(tokens, idx_1).type != TokenTypes.TT_RPAREN:
            return None, idx_1
        return func_def_colon(tokens, idx_1, curr_tok,arg_list)
    else:
        if get_curr_tok(tokens, idx+2).type != TokenTypes.TT_RPAREN:
            return None, idx+2
        return func_def_colon(tokens, idx+2, curr_tok,[])
            

def func_def(tokens: List[Token] = [], idx: int = 0) -> Tuple[any, int]:
    #print('func_def',get_curr_tok(tokens, idx))
    if not get_curr_tok(tokens, idx).matches(TokenTypes.TT_KEYWORD, 'ROUTE'):
        return None, idx
    curr_tok:Token = get_curr_tok(tokens, idx+1)
    if curr_tok.type == TokenTypes.TT_IDENTIFIER:
        return func_def_if(tokens, idx+2, curr_tok)
    else:
        return func_def_else(tokens, idx+1, curr_tok)
     

def func_def_colon(tokens: List[Token] = [], idx: int = 0, var_name:Token=Token(),arg_list:list=[]):
    #print('func_def_colon',get_curr_tok(tokens, idx))
    if get_curr_tok(tokens, idx).type == TokenTypes.TT_COLON:
        body, idx_1 = expression(tokens, idx+1)
        #print(body)
        return FuncDefNode(var_name, arg_list ,body, False), idx_1
    
    if get_curr_tok(tokens, idx).type != TokenTypes.TT_NEWLINE:
        return None, idx+1
    #print('TEST1',get_curr_tok(tokens, idx+1))
    body, idx_1 = statements(tokens, idx+1)
    #print('TEST',body)
    #print('TEST3123',get_curr_tok(tokens, idx+1))
    if not get_curr_tok(tokens, idx_1).matches(TokenTypes.TT_KEYWORD, 'END'):
        return None, idx_1
    return FuncDefNode(var_name, arg_list ,body, True), idx_1+1

def func_def_inputs(tokens: List[Token] = [], idx: int = 0, arg_name_toks:list=[]):
    #print('func_def_inputs',get_curr_tok(tokens, idx))
    if get_curr_tok(tokens, idx).type == TokenTypes.TT_COMMA:
        curr_tok:Token = get_curr_tok(tokens, idx+1)
        if curr_tok.type != TokenTypes.TT_IDENTIFIER:
            return arg_name_toks, idx+2
        arg_name_toks.append(curr_tok)
        return func_def_inputs(tokens, idx+2, arg_name_toks)
    else:
        return arg_name_toks, idx

def call(tokens: List[Token] = [], idx: int = 0):
    #print('call',get_curr_tok(tokens, idx))
    fact, idx_1 = factor(tokens, idx)
    #print('THE fact')
    if get_curr_tok(tokens, idx_1).type == TokenTypes.TT_LPAREN:
        if get_curr_tok(tokens, idx_1+1).type == TokenTypes.TT_RPAREN:
            return CallNode(fact, []), idx_1+1
        else:
            expr, idx_2 = expression(tokens,idx_1+1)
            arg_nodes, idx_3 = args_inputs(tokens, idx_2, [expr])
            #print('WWWOOW',get_curr_tok(tokens, idx_3))
            if get_curr_tok(tokens, idx_3).type != TokenTypes.TT_RPAREN:
                return None, idx_3
            return CallNode(fact, arg_nodes), idx_3+1
    return fact, idx_1

def args_inputs(tokens: List[Token] = [], idx: int = 0, arg_nodes:list = []):
    #print('args_inputs',get_curr_tok(tokens, idx))   
    if get_curr_tok(tokens, idx).type == TokenTypes.TT_COMMA:
        expr, idx_1 = expression(tokens, idx+1)
        arg_nodes.append(expr)
        return args_inputs(tokens, idx_1, arg_nodes)
    return arg_nodes, idx

def for_expr(tokens: List[Token] = [], idx: int = 0) -> Tuple[Node, int]:
    #print('for_expr',get_curr_tok(tokens, idx)) 
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

    if get_curr_tok(tokens, idx_2).matches(TokenTypes.TT_KEYWORD, 'STEP'):
        step_value, idx_3 = expression(tokens, idx_2)
        if not get_curr_tok(tokens, idx_3).matches(TokenTypes.TT_KEYWORD, 'THEN'):
            return None, idx_3
        #print('STATETETAT',get_curr_tok(tokens, idx_3+1))
        if get_curr_tok(tokens, idx_3+1).type == TokenTypes.TT_NEWLINE:
            body, idx_4 = statements(tokens, idx_3+2)
            #print('BODY',body)
            if not get_curr_tok(tokens, idx_4).matches(TokenTypes.TT_KEYWORD, 'END'):
                return None, idx_4
            return ForNode(curr_tok_2, start_value, end_value, step_value, body, True), idx_4
    else: 
        if not get_curr_tok(tokens, idx_2).matches(TokenTypes.TT_KEYWORD, 'THEN'):
            return None, idx_2
        body, idx_3 = statements(tokens, idx_2+1)
        #print('BODYBUDY',body)
        return ForNode(curr_tok_1, start_value, end_value, None, body, False), idx_3

def while_expr(tokens: List[Token] = [], idx: int = 0) -> Tuple[Node, int]:
    #print('while_expr',get_curr_tok(tokens, idx))
    condition, idx_1 = not_keyword_check(tokens, idx, 'WHILE', expression)
    #print('CONDITIONNNN',condition)
    #print('BVATCHEESET',get_curr_tok(tokens, idx_1))
    if not get_curr_tok(tokens, idx_1).matches(TokenTypes.TT_KEYWORD, 'THEN'):
            return None, idx_1
    #print('BVATCHEESET',get_curr_tok(tokens, idx_1+1))
    if get_curr_tok(tokens, idx_1+1).type == TokenTypes.TT_NEWLINE:
        body, idx_2 = statements(tokens, idx_1+2)
        #print('CONDITIONNNN',body)
        if not get_curr_tok(tokens, idx_2).matches(TokenTypes.TT_KEYWORD, 'END'):
            return None, idx_2
        return WhileNode(condition, body, True), idx_2+1
    body, idx_2 = statement_keywords(tokens, idx_1)
    return WhileNode(condition, body, False), idx_2


def if_expr(tokens: List[Token] = [], idx: int = 0) -> Tuple[Node, int]:
    #print('if_expr',get_curr_tok(tokens, idx))
    cases, else_case, idx_1 = if_expr_cases(tokens, idx, 'IF')
    #print('CASES',cases, else_case)
    return IfNode(cases, else_case), idx_1

def if_expr_cases(tokens: List[Token] = [], idx: int = 0, keyword:str=''):
    #print('if_expr_cases',get_curr_tok(tokens, idx))
    cases = []
    else_case = None

    if not get_curr_tok(tokens, idx).matches(TokenTypes.TT_KEYWORD, keyword):
        return None,None, idx
    
    condition, idx_1 = expression(tokens, idx+1)
    #print('TESTET',condition,get_curr_tok(tokens, idx_1))
    if not get_curr_tok(tokens, idx_1).matches(TokenTypes.TT_KEYWORD, 'THEN'):
        return None,None, idx_1
    #print('BAATCHEEST',get_curr_tok(tokens, idx_1+1))

    if get_curr_tok(tokens, idx_1+1).type == TokenTypes.TT_NEWLINE:
        statement, idx_2 = statements(tokens, idx_1+2)
        cases.append((condition, statement, True))
        #print('HERERERE',get_curr_tok(tokens, idx_2))

        if get_curr_tok(tokens, idx_2).matches(TokenTypes.TT_KEYWORD, 'END'):
            return cases, else_case, idx_2
        else:
            new_cases, else_case, idx_3 = if_expr_or(tokens, idx_2)
            #print(new_cases, else_case)
            cases.extend(new_cases)
            return cases, else_case, idx_3
    else:
        expr, idx_2 = statement_keywords(tokens, idx_1)
        cases.append((condition, expr, False))

        new_cases, else_case, idx_3 = if_expr_or(tokens, idx_2)
        cases.extend(new_cases)
        return cases, else_case, idx_3


def if_expr_or(tokens: List[Token] = [], idx: int = 0):
    #print('if_expr_or',get_curr_tok(tokens, idx))
    cases, else_case = [], None
    if get_curr_tok(tokens, idx).matches(TokenTypes.TT_KEYWORD, 'ELIF'):
        new_cases, else_case, idx_1= if_expr_elif(tokens, idx)
        return new_cases, else_case, idx_1
    else:
        else_case, idx_1 = if_expr_else(tokens, idx)
        return cases, else_case, idx_1

def if_expr_elif(tokens: List[Token] = [], idx: int = 0):
    #print('if_expr_elif',get_curr_tok(tokens, idx))
    return if_expr_cases(tokens, idx,'ELIF')

def if_expr_else(tokens: List[Token] = [], idx: int = 0):
    #print('if_expr_else',get_curr_tok(tokens, idx))
    else_case = None
    if get_curr_tok(tokens, idx).matches(TokenTypes.TT_KEYWORD, 'ELSE'):
        #print('BEEEEEEEEEES')
        if get_curr_tok(tokens, idx+1).type == TokenTypes.TT_NEWLINE:
            statement, idx_1 = statements(tokens, idx+2)
            else_case = (statement, True)
        if get_curr_tok(tokens, idx_1).matches(TokenTypes.TT_KEYWORD, 'END'):
            return else_case, idx_1
    else:
        expr, idx_1 = statement_keywords(tokens, idx)
        else_case = (expr, False)
        return else_case, idx_1

def if_expr_loop(tokens, idx, cases=[]) -> Tuple[Node, int]:
    #print('if_expr_loop',get_curr_tok(tokens, idx))
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

def list_expr(tokens: List[Token] = [], idx: int = 0):
    #print('list_expr',get_curr_tok(tokens, idx))
    element_nodes = []
    #print(get_curr_tok(tokens, idx))
    if get_curr_tok(tokens, idx).type != TokenTypes.TT_LSQUARE:
        return None, idx
    #print('test', get_curr_tok(tokens, idx+1))

    if get_curr_tok(tokens, idx+1).type == TokenTypes.TT_RSQUARE:
        return ListNode(element_nodes), idx+1
    else:
        expr, idx_1 = expression(tokens, idx+1)
        #print('exfdaafa',expr)
        element_nodes.append(expr)
        element_nodes_1, idx_2 = args_inputs(tokens, idx_1, element_nodes)
        #print('afasdfasd',element_nodes_1)
        if get_curr_tok(tokens, idx_2).type != TokenTypes.TT_RSQUARE:
            return None, idx_2
        #print('THORUGH')
        return ListNode(element_nodes_1), idx_2+1

def comp_expr(tokens: List[Token] = [], idx: int = 0) -> Tuple[Node, int]:
    #print('comp_expr',get_curr_tok(tokens, idx))
    curr_tok: Token = get_curr_tok(tokens, idx)
    if curr_tok.matches(TokenTypes.TT_KEYWORD, 'NOT'):
        exp, idx_1 = comp_expr(tokens, idx+1)
        return UnaryOpNode(curr_tok, exp), idx_1
    return bin_op_left(arith_expr, (TokenTypes.TT_EE, TokenTypes.TT_NE, TokenTypes.TT_LT, TokenTypes.TT_GT, TokenTypes.TT_LTE, TokenTypes.TT_GTE), tokens, idx)

def arith_expr(tokens: List[Token] = [], idx: int = 0) -> Tuple[Node, int]:
    #print('arith_expr',get_curr_tok(tokens, idx))
    return bin_op_left(term, (TokenTypes.TT_PLUS, TokenTypes.TT_MINUS), tokens, idx)

def expression(tokens: List[Token] = [], idx: int = 0) -> Tuple[Node, int]:
    #print('expression',get_curr_tok(tokens, idx))
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
    #print('term',get_curr_tok(tokens, idx))
    return bin_op_left(call, (TokenTypes.TT_MUL, TokenTypes.TT_DIV), tokens, idx)


def factor(tokens: List[Token] = [], idx: int = 0) -> Tuple[Node, int]:
    #print('factor',get_curr_tok(tokens, idx))
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
            #print('BEEP BOOP')
            return expr, idx_1+1
    elif curr_tok.type == TokenTypes.TT_LSQUARE:
        #print('here')
        return list_expr(tokens, idx)
    elif curr_tok.matches(TokenTypes.TT_KEYWORD, 'IF'):
        return if_expr(tokens,idx)
    elif curr_tok.matches(TokenTypes.TT_KEYWORD, 'FOR'):
        return for_expr(tokens,idx)
    elif curr_tok.matches(TokenTypes.TT_KEYWORD, 'WHILE'):
        return while_expr(tokens,idx)
    elif curr_tok.matches(TokenTypes.TT_KEYWORD, 'ROUTE'):
        return func_def(tokens,idx)
    #print('OUT?')
    return None, idx


def bin_op_left(func: callable, ops: tuple, tokens: List[Token] = [], idx: int = 0) -> Tuple[Node, int]: # dit zijn hoge orde functies
    #print('bin_op_left',get_curr_tok(tokens, idx))
    funct, i = func(tokens, idx)
    return bin_op_right(func, ops, tokens, i, funct)


def bin_op_right(func: callable, ops: tuple, tokens: List[Token], idx: int, left: any) -> Tuple[Node, int]:
    #print('bin_op_right',get_curr_tok(tokens, idx))
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
    # #print('TOKENS:', tokens)
    if error:
        return None, error
    ast, _ = parse(tokens)

    return ast
