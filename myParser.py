from typing import List, Tuple
from myLexer import Error, Token
from myLexer import TokenTypes
import myLexer

# These nodes is what the AST exists of
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
        super().__init__('TRAFFICNODE')
        self.cases = cases
        self.else_case = else_case
    def __repr__(self) -> str:
        return f'({self.node_name}: {self.cases}, FLEECASE: {self.else_case})'

class ForNode(Node):
    def __init__(
        self, var_name_tok, start_value_node, end_value_node, 
        step_value_node, body_node, should_return_null
        ):
        super().__init__('DRIVINGNODE')
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
        super().__init__('SPEEDINGNODE')
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
# Return node
class DestinationNode(Node):
    def __init__(self, node_to_return):
        super().__init__('DESTINATIONNODE')

        self.node_to_return = node_to_return
    def __repr__(self) -> str:
        return f'({self.node_name}: {self.node_to_return})'
class PrintNode(Node):
    def __init__(self, printable):
        super().__init__('PRINTNODE')
        self.printable = printable

    def __repr__(self) -> str:
        return f'({self.node_name}, {self.printable})'

# If the current token does not match with the keyword, then execute the given function
def not_keyword_check(tokens: List[Token] = [], idx: int = 0, keyword:str='', func: callable = None) -> Tuple[any, int]:
    if not get_curr_tok(tokens, idx).matches(TokenTypes.TT_KEYWORD, keyword):
        return None, idx
    return func(tokens, idx+1)

# This will go through the token list and propels the current tokens through the ast, puts everything in a listnode at the end
def statements( tokens: List[Token] = [], idx: int = 0 ) -> Node:
    if len(tokens) == 0: return None, 0
    statements_list = []
    _, idx_1 = if_newline(tokens, idx, 0)
    statement, idx_2 = statement_keywords(tokens, idx_1)
    statements_list.append(statement)
    statements_list_1, idx_3 = statement_loop(tokens, idx_2, statements_list)
    return ListNode(statements_list_1), idx_3

# Keep recursing through the ast until there are no more statements
def statement_loop(tokens: List[Token] = [], idx: int = 0, statements_list:list = []) -> Tuple[List[Node], int]:
    count, idx_1 = if_newline(tokens, idx, 0)
    if count == 0:
        return statements_list, idx_1
    statement, idx_2 = statement_keywords(tokens, idx_1)
    if not statement:
        return statements_list, idx_2
    statements_list.append(statement)
    return statement_loop(tokens, idx_2, statements_list )

# This will check for a return or a print node
def  statement_keywords(tokens: List[Token] = [], idx: int = 0) -> Tuple[Node, int]:
    if get_curr_tok(tokens, idx).matches(TokenTypes.TT_KEYWORD, 'DESTINATION'):
        expr, idx_1 = expression(tokens, idx+1)
        return DestinationNode(expr), idx_1
    if get_curr_tok(tokens, idx).matches(TokenTypes.TT_KEYWORD, 'PRINT'):
        expr, idx_1 = expression(tokens, idx+1)
        return PrintNode(expr), idx_1
    expr, idx_1 = expression(tokens, idx)
    return expr, idx_1

# If ; or \n is seen it's a newline token, we want to skip that
def if_newline(tokens: List[Token] = [], idx: int = 0, count:int = 0) -> Tuple[int, int]:
    curr_tok:Token = get_curr_tok(tokens, idx)
    if curr_tok.type == None:
        return 0, idx
    elif curr_tok.type == TokenTypes.TT_NEWLINE:
        return if_newline(tokens,idx+1, count+1)

    return count, idx

# This will define the function node
def func_def(tokens: List[Token] = [], idx: int = 0) -> Tuple[Node, int]:
    if not get_curr_tok(tokens, idx).matches(TokenTypes.TT_KEYWORD, 'ROUTE'):
        return None, idx
    curr_tok:Token = get_curr_tok(tokens, idx+1)
    if curr_tok.type == TokenTypes.TT_IDENTIFIER:
        return func_def_if(tokens, idx+2, curr_tok)
    else:
        return func_def_else(tokens, idx+1, curr_tok)

# If there is an function name we want to go through this function to remember the name
def func_def_if(tokens: List[Token] = [], idx: int = 0, curr_tok:Token=Token()) -> Tuple[Node, int]:
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

# If there is no function name it's an anonymous function and has to go through this function
def func_def_else(tokens: List[Token] = [], idx: int = 0, curr_tok:Token=Token()) -> Tuple[Node, int]:
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

# Defines what the function does
def func_def_colon(tokens: List[Token] = [], idx: int = 0, var_name:Token=Token(),arg_list:list=[]) -> Tuple[Node, int]:
    if get_curr_tok(tokens, idx).type == TokenTypes.TT_COLON:
        body, idx_1 = expression(tokens, idx+1)
        return FuncDefNode(var_name, arg_list ,body, False), idx_1
    
    if get_curr_tok(tokens, idx).type != TokenTypes.TT_NEWLINE:
        return None, idx+1
    body, idx_1 = statements(tokens, idx+1)
    if not get_curr_tok(tokens, idx_1).matches(TokenTypes.TT_KEYWORD, 'REFUEL'):
        return None, idx_1
    return FuncDefNode(var_name, arg_list ,body, True), idx_1+1

# The arguments given to the function will be defined here
def func_def_inputs(tokens: List[Token] = [], idx: int = 0, arg_name_toks:list=[]) -> Tuple[list, int]:
    if get_curr_tok(tokens, idx).type == TokenTypes.TT_COMMA:
        curr_tok:Token = get_curr_tok(tokens, idx+1)
        if curr_tok.type != TokenTypes.TT_IDENTIFIER:
            return arg_name_toks, idx+2
        arg_name_toks.append(curr_tok)
        return func_def_inputs(tokens, idx+2, arg_name_toks)
    else:
        return arg_name_toks, idx

# This will return a callnode with the function that needs to be called
def call(tokens: List[Token] = [], idx: int = 0) -> Tuple[Node, int]:

    fact, idx_1 = factor(tokens, idx)
    if get_curr_tok(tokens, idx_1).type == TokenTypes.TT_LPAREN:
        if get_curr_tok(tokens, idx_1+1).type == TokenTypes.TT_RPAREN:
            return CallNode(fact, []), idx_1+1
        else:
            expr, idx_2 = expression(tokens,idx_1+1)
            arg_nodes, idx_3 = args_inputs(tokens, idx_2, [expr])
            if get_curr_tok(tokens, idx_3).type != TokenTypes.TT_RPAREN:
                return None, idx_3
            return CallNode(fact, arg_nodes), idx_3+1
    return fact, idx_1

# The arguments given to the function will be defined here
def args_inputs(tokens: List[Token] = [], idx: int = 0, arg_nodes:list = []) -> Tuple[list, int]:
    if get_curr_tok(tokens, idx).type == TokenTypes.TT_COMMA:
        expr, idx_1 = expression(tokens, idx+1)
        arg_nodes.append(expr)
        return args_inputs(tokens, idx_1, arg_nodes)
    return arg_nodes, idx

# This will create the for loop node, it will have to check what the range and steps are
def for_expr(tokens: List[Token] = [], idx: int = 0) -> Tuple[Node, int]:
    curr_tok: Token = get_curr_tok(tokens, idx)
    if not curr_tok.matches(TokenTypes.TT_KEYWORD, 'DRIVING'):
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
        if not get_curr_tok(tokens, idx_3).matches(TokenTypes.TT_KEYWORD, 'GPS'):
            return None, idx_3
        if get_curr_tok(tokens, idx_3+1).type == TokenTypes.TT_NEWLINE:
            body, idx_4 = statements(tokens, idx_3+2)
            if not get_curr_tok(tokens, idx_4).matches(TokenTypes.TT_KEYWORD, 'REFUEL'):
                return None, idx_4
            return ForNode(curr_tok_2, start_value, end_value, step_value, body, True), idx_4
    else: 
        if not get_curr_tok(tokens, idx_2).matches(TokenTypes.TT_KEYWORD, 'GPS'):
            return None, idx_2
        body, idx_3 = statements(tokens, idx_2+1)
        return ForNode(curr_tok_1, start_value, end_value, None, body, False), idx_3

# This will create the while node
def while_expr(tokens: List[Token] = [], idx: int = 0) -> Tuple[Node, int]:
    condition, idx_1 = not_keyword_check(tokens, idx, 'SPEEDING', expression)
    if not get_curr_tok(tokens, idx_1).matches(TokenTypes.TT_KEYWORD, 'GPS'):
            return None, idx_1

    if get_curr_tok(tokens, idx_1+1).type == TokenTypes.TT_NEWLINE:
        body, idx_2 = statements(tokens, idx_1+2)

        if not get_curr_tok(tokens, idx_2).matches(TokenTypes.TT_KEYWORD, 'REFUEL'):
            return None, idx_2
        return WhileNode(condition, body, True), idx_2+1
    body, idx_2 = statement_keywords(tokens, idx_1)
    return WhileNode(condition, body, False), idx_2

# This function will return the ifnode
def if_expr(tokens: List[Token] = [], idx: int = 0) -> Tuple[Node, int]:

    cases, else_case, idx_1 = if_expr_cases(tokens, idx, 'TRAFFIC')

    return IfNode(cases, else_case), idx_1

# This will fill the cases and else cases with their respective statements
def if_expr_cases(tokens: List[Token] = [], idx: int = 0, keyword:str='') -> Tuple[list, list, int]:

    cases = []
    else_case = None

    if not get_curr_tok(tokens, idx).matches(TokenTypes.TT_KEYWORD, keyword):
        return None,None, idx
    
    condition, idx_1 = expression(tokens, idx+1)

    if not get_curr_tok(tokens, idx_1).matches(TokenTypes.TT_KEYWORD, 'GPS'):
        return None,None, idx_1

    if get_curr_tok(tokens, idx_1+1).type == TokenTypes.TT_NEWLINE:
        statement, idx_2 = statements(tokens, idx_1+2)
        cases.append((condition, statement, True))


        if get_curr_tok(tokens, idx_2).matches(TokenTypes.TT_KEYWORD, 'REFUEL'):
            return cases, else_case, idx_2
        else:
            new_cases, else_case, idx_3 = if_expr_or(tokens, idx_2)

            cases.extend(new_cases)
            return cases, else_case, idx_3
    else:
        expr, idx_2 = statement_keywords(tokens, idx_1)
        cases.append((condition, expr, False))

        new_cases, else_case, idx_3 = if_expr_or(tokens, idx_2)
        cases.extend(new_cases)
        return cases, else_case, idx_3

# this will decide whether there is an elif or else
def if_expr_or(tokens: List[Token] = [], idx: int = 0) -> Tuple[list, list, int] :

    cases, else_case = [], None
    if get_curr_tok(tokens, idx).matches(TokenTypes.TT_KEYWORD, 'BYPASS'):
        new_cases, else_case, idx_1= if_expr_elif(tokens, idx)
        return new_cases, else_case, idx_1
    else:
        else_case, idx_1 = if_expr_else(tokens, idx)
        return cases, else_case, idx_1

# If there is an elif go to if_expr_cases to fill its case and else_cases
def if_expr_elif(tokens: List[Token] = [], idx: int = 0) -> Tuple[Node, int]:
    return if_expr_cases(tokens, idx,'BYPASS')

# If there is an else fill the else_case with its statements
def if_expr_else(tokens: List[Token] = [], idx: int = 0) -> Tuple[list, int]:
    else_case = None
    if get_curr_tok(tokens, idx).matches(TokenTypes.TT_KEYWORD, 'FLEE'):

        if get_curr_tok(tokens, idx+1).type == TokenTypes.TT_NEWLINE:
            statement, idx_1 = statements(tokens, idx+2)
            else_case = (statement, True)
        if get_curr_tok(tokens, idx_1).matches(TokenTypes.TT_KEYWORD, 'REFUEL'):
            return else_case, idx_1
    else:
        expr, idx_1 = statement_keywords(tokens, idx)
        else_case = (expr, False)
        return else_case, idx_1

# This will create the list node
def list_expr(tokens: List[Token] = [], idx: int = 0) -> Tuple[Node, int]:
    element_nodes = []

    if get_curr_tok(tokens, idx).type != TokenTypes.TT_LSQUARE:
        return None, idx
    if get_curr_tok(tokens, idx+1).type == TokenTypes.TT_RSQUARE:
        return ListNode(element_nodes), idx+1
    else:
        expr, idx_1 = expression(tokens, idx+1)
        element_nodes.append(expr)
        element_nodes_1, idx_2 = args_inputs(tokens, idx_1, element_nodes)
        if get_curr_tok(tokens, idx_2).type != TokenTypes.TT_RSQUARE:
            return None, idx_2
        return ListNode(element_nodes_1), idx_2+1

# This checks whether there is a NOT sign and will return the unarynode if so
def comp_expr(tokens: List[Token] = [], idx: int = 0) -> Tuple[Node, int]:
    curr_tok: Token = get_curr_tok(tokens, idx)
    if curr_tok.matches(TokenTypes.TT_KEYWORD, 'NOT'):
        exp, idx_1 = comp_expr(tokens, idx+1)
        return UnaryOpNode(curr_tok, exp), idx_1
    return bin_op_left(arith_expr, (TokenTypes.TT_EE, TokenTypes.TT_NE, TokenTypes.TT_LT, TokenTypes.TT_GT, TokenTypes.TT_LTE, TokenTypes.TT_GTE), tokens, idx)

def arith_expr(tokens: List[Token] = [], idx: int = 0) -> Tuple[Node, int]:
    return bin_op_left(term, (TokenTypes.TT_PLUS, TokenTypes.TT_MINUS), tokens, idx)

# If a variable matches then it must be assigned to the value, this will return the varassign node
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

def term(tokens: List[Token] = [], idx: int = 0) -> Tuple[Node, int]:
    return bin_op_left(call, (TokenTypes.TT_MUL, TokenTypes.TT_DIV), tokens, idx)
# This function will check whether there are keywords that match, if there are then go to their corresponding functions and return the correct node
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
    elif curr_tok.type == TokenTypes.TT_LSQUARE:
        return list_expr(tokens, idx)
    elif curr_tok.matches(TokenTypes.TT_KEYWORD, 'TRAFFIC'):
        return if_expr(tokens,idx)
    elif curr_tok.matches(TokenTypes.TT_KEYWORD, 'DRIVING'):
        return for_expr(tokens,idx)
    elif curr_tok.matches(TokenTypes.TT_KEYWORD, 'SPEEDING'):
        return while_expr(tokens,idx)
    elif curr_tok.matches(TokenTypes.TT_KEYWORD, 'ROUTE'):
        return func_def(tokens,idx)
    return None, idx

# This is the binary operator split into two function, left and right. 
# Left will execute its given function and gives it to right
def bin_op_left(func: callable, ops: tuple, tokens: List[Token] = [], idx: int = 0) -> Tuple[Node, int]:
    funct, i = func(tokens, idx)
    return bin_op_right(func, ops, tokens, i, funct)
# Right will check if the current token is or is in ops, 
# if that is the case then it will recurse until it is not
# The result is that there is that the node can contain multiple nodes in their right value
# Which is useful for calculations
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

def parse(tokens: List[Token] = []) -> any:
    return statements(tokens)

def run(fn: str = '', text: str = '') -> Tuple[Node, Error]:
    tokens, error = myLexer.run(fn, text)
    if error:
        return None, error
    ast, _ = parse(tokens)

    return ast, error
