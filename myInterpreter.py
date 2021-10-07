import myParser
from myParser import TokenTypes,CallNode, FuncDefNode, BinOpNode, NumberNode, UnaryOpNode, Node, VarAccesNode, VarAssignNode, IfNode,ForNode, WhileNode


def interpreter(ast, symbol_table):
    res, new_symbol_table = visit(ast, symbol_table)
    return res, new_symbol_table

class SymbolTable:
    def __init__(self, symbols={}, parent=None, symbol_list:list=[]) -> None:
        self.symbols = symbols
        self.symbol_list = symbol_list
        self.parent = parent

    def look_up(self, name):
        value = self.symbols.get(name, None)
        if value == None:
            return None
        return value

    def insert(self, name, value):
        if name in self.symbol_list:
            return SymbolTable(self.symbols, self.parent )
        return SymbolTable({**self.symbols, **{name:value}}, self.parent )

    def insert_basic_function(self, name, value):
        self.symbol_list.append(name)
        return SymbolTable({**self.symbols, **{name:value}}, self.parent,self.symbol_list )

    def __repr__(self) -> str:
        return f'{self.symbols}'

class Value:
    def __init__(self,symbol_table:SymbolTable = SymbolTable()):
        self.symbol_table = symbol_table

    def added_to(self, other):
        return None, self.illegal_operation(other)

    def subbed_by(self, other):
        return None, self.illegal_operation(other)

    def multed_by(self, other):
        return None, self.illegal_operation(other)

    def dived_by(self, other):
        return None, self.illegal_operation(other)

    def powed_by(self, other):
        return None, self.illegal_operation(other)

    def get_comparison_eq(self, other):
        return None, self.illegal_operation(other)

    def get_comparison_ne(self, other):
        return None, self.illegal_operation(other)

    def get_comparison_lt(self, other):
        return None, self.illegal_operation(other)

    def get_comparison_gt(self, other):
        return None, self.illegal_operation(other)

    def get_comparison_lte(self, other):
        return None, self.illegal_operation(other)

    def get_comparison_gte(self, other):
        return None, self.illegal_operation(other)

    def anded_by(self, other):
        return None, self.illegal_operation(other)

    def ored_by(self, other):
        return None, self.illegal_operation(other)

    def notted(self,other):
        return None, self.illegal_operation(other)

    def is_true(self):
        return False

    def illegal_operation(self, other=None):
        if not other: other = self
        return None
class Number:
    def __init__(self, value=None):
        self.value = value
    # other is een number/ kan in haskell
    def added_to(self, other):
        if isinstance(other, Number):
            return Number(self.value + other.value)

    def subtracted_by(self, other):
        if isinstance(other, Number):
            return Number(self.value - other.value)

    def multiplied_by(self, other):
        if isinstance(other, Number):
            return Number(self.value * other.value)

    def divided_by(self, other):
        if isinstance(other, Number):
            if other.value == 0:
                return None
            return Number(self.value / other.value)
    def get_comparison_eq(self, other):
        if isinstance(other, Number):
            return Number(int(self.value == other.value))

    def get_comparison_ne(self, other):
        if isinstance(other, Number):
            return Number(int(self.value != other.value))

    def get_comparison_lt(self, other):
        if isinstance(other, Number):
            return Number(int(self.value < other.value))

    def get_comparison_gt(self, other):
        if isinstance(other, Number):
            return Number(int(self.value > other.value))

    def get_comparison_lte(self, other):
        if isinstance(other, Number):
            return Number(int(self.value <= other.value))

    def get_comparison_gte(self, other):
        if isinstance(other, Number):
            return Number(int(self.value >= other.value))

    def anded_by(self, other):
        if isinstance(other, Number):
            return Number(int(self.value and other.value))

    def ored_by(self, other):
        if isinstance(other, Number):
            return Number(int(self.value or other.value))

    def notted(self):
        return Number(1 if self.value == 0 else 0)
    
    def is_true(self):
        return self.value != 0

    def __repr__(self):
        return str(self.value)

class Function(Value):
    def __init__(self, name, body_node, arg_names, symbol_table:SymbolTable= SymbolTable()):
        super().__init__(symbol_table)
        self.name = name or "<anonymous>"
        self.body_node = body_node
        self.arg_names = arg_names
    
    def execute(self, args, symbol_table):
        print(args)
        print(len(args),len(self.arg_names))
        if len(args) > len(self.arg_names):
            return None, symbol_table
        if len(args) < len(self.arg_names):
            return None, symbol_table
        symbol_table_1 = self.set_args(args, 0, symbol_table)
        return visit(self.body_node, symbol_table_1)

    def set_args(self, args,idx,symbol_table:SymbolTable):
        if len(args) <= idx:
            return symbol_table
        return self.set_args(args, idx+1, symbol_table.insert(self.arg_names[idx], args[idx]))
    def set_symbol_table(self, symbol_table):
        return Function(self.name, self.body_node, self.arg_names, symbol_table)

def visit(node:Node,symbol_table:SymbolTable) -> any:
    if isinstance(node,NumberNode):
        return visit_NumberNode(node,symbol_table)
    elif isinstance(node,BinOpNode):
        return visit_BinOpNode(node,symbol_table)
    elif isinstance(node, UnaryOpNode):
        return visit_UnaryOpNode(node,symbol_table)
    elif isinstance(node, VarAccesNode):
        return visit_VarAccesNode(node,symbol_table)
    elif isinstance(node, VarAssignNode):
        return visit_VarAssignNode(node,symbol_table)
    elif isinstance(node, IfNode):
        return visit_IfNode(node,symbol_table)
    elif isinstance(node, ForNode):
        return visit_ForNode(node,symbol_table)
    elif isinstance(node, WhileNode):
        return visit_WhileNode(node,symbol_table)
    elif isinstance(node, FuncDefNode):
        return visit_FuncDefNode(node,symbol_table)
    elif isinstance(node, CallNode):
        return visit_CallNode(node,symbol_table)
    elif node == None:
        pass

def no_visit_method(node: Node):
    raise Exception(f'No visit_{type(node).__name__} method defined{node}')

def visit_NumberNode(node: Node,symbol_table:SymbolTable):
    return Number(node.tok.value), symbol_table

def visit_BinOpNode(node: Node,symbol_table:SymbolTable):
    left:Number
    right:Number
    left, _= visit(node.left_node,symbol_table)
    right,_= visit(node.right_node,symbol_table)
    if node.op_tok.type == TokenTypes.TT_PLUS:
        return left.added_to(right), symbol_table
    elif node.op_tok.type == TokenTypes.TT_MINUS:
        return left.subtracted_by(right), symbol_table
    elif node.op_tok.type == TokenTypes.TT_MUL:
        return left.multiplied_by(right), symbol_table
    elif node.op_tok.type == TokenTypes.TT_DIV:
        return left.divided_by(right), symbol_table
    elif node.op_tok.type == TokenTypes.TT_EE:
        return left.get_comparison_eq(right), symbol_table
    elif node.op_tok.type == TokenTypes.TT_NE:
        return left.get_comparison_ne(right), symbol_table
    elif node.op_tok.type == TokenTypes.TT_LT:
        return left.get_comparison_lt(right), symbol_table
    elif node.op_tok.type == TokenTypes.TT_GT:
        return left.get_comparison_gt(right), symbol_table
    elif node.op_tok.type == TokenTypes.TT_LTE:
        return left.get_comparison_lte(right), symbol_table
    elif node.op_tok.type == TokenTypes.TT_GTE:
        return left.get_comparison_gte(right), symbol_table
    elif node.op_tok.matches(TokenTypes.TT_KEYWORD, 'AND'):
        return left.anded_by(right), symbol_table
    elif node.op_tok.matches(TokenTypes.TT_KEYWORD, 'OR'):
        return left.ored_by(right), symbol_table
    return None, symbol_table


def visit_UnaryOpNode(node:Node,symbol_table:SymbolTable):
    number, _ = visit(node.node,symbol_table)

    if node.op_tok.type == TokenTypes.TT_MINUS:
        number = number.multiplied_by(Number(-1))

    return number, symbol_table

def visit_VarAccesNode(node: Node,symbol_table:SymbolTable):
    value = symbol_table.look_up(node.var_name_tok.value)
    if not value:
        return None, symbol_table
    return value, symbol_table

def visit_VarAssignNode(node: Node,symbol_table:SymbolTable):
    value, new_symbol_table = visit(node.value_node, symbol_table)
    return value, new_symbol_table.insert(node.var_name_tok.value, value)

def visit_IfNode(node: Node, symbol_table:SymbolTable):
    condition, symbol_table_1 = IfNode_loop(node, symbol_table)
    if condition == None and node.else_case:
        else_value, symbol_table_2 = visit(node.else_case, symbol_table_1)
        return else_value, symbol_table_2
    return condition, symbol_table_1

def IfNode_loop(node:Node, symbol_table:SymbolTable, idx=0):
    if idx == len(node.cases):
        return None, symbol_table
    condition, expr = get_case(node.cases, idx)
    condition_value, symbol_table_1 = visit(condition, symbol_table)

    if condition_value.is_true():
        expr_value, symbol_table_2 = visit(expr, symbol_table_1)
        return expr_value,symbol_table_2
    return IfNode_loop(node, symbol_table_1, idx+1)

def visit_ForNode(node:Node, symbol_table:SymbolTable):
    start_value, symbol_table_1 = visit(node.start_value_node, symbol_table)
    end_value, symbol_table_2 = visit(node.end_value_node, symbol_table_1)
    if node.step_value_node:
        step_value, symbol_table_3 = visit(node.end_value_node, symbol_table_2)
        return ForNode_loop(node, symbol_table_3, start_value.value, end_value.value, step_value.value)
    else:
        return ForNode_loop(node, symbol_table_2, start_value.value, end_value.value, 1)

def ForNode_loop(node:Node, symbol_table:SymbolTable, start_value:int, end_value:int, step_value ):
    if step_value >= 0:
        if start_value > end_value:
            return None, symbol_table
    else: 
        if start_value < end_value:
            return None, symbol_table
    value, symbol_table_2 = visit(node.body_node, symbol_table.insert(node.var_name_tok.value, Number(start_value)))

    return ForNode_loop(node, symbol_table_2.insert(node.var_name_tok.value, Number(start_value)), start_value + step_value, end_value, step_value)

def visit_WhileNode(node:Node, symbol_table:SymbolTable):
    condition, symbol_table_1 = visit(node.condition_node, symbol_table)
    if not condition.is_true(): return None, symbol_table_1
    value, symbol_table_2 = visit(node.body_node, symbol_table_1)
    return visit_WhileNode(node, symbol_table_2)

def visit_FuncDefNode(node:Node=Node(), symbol_table:SymbolTable=SymbolTable()):
    func_name = node.var_name_tok.value if node.var_name_tok else None
    func_value = Function(
        func_name, 
        node.body_node, 
        [arg_name.value for arg_name in node.arg_name_toks], 
        symbol_table
        )
    if node.var_name_tok:
        symbol_table_1 = symbol_table.insert(func_name, func_value)
        return func_value.set_symbol_table(symbol_table_1), symbol_table_1

    return func_value, symbol_table
def visit_CallNode(node:Node=Node(), symbol_table:SymbolTable=SymbolTable()):
    value_to_call, symbol_table_1 = visit(node.node_to_call, symbol_table)
    args, symbol_table_2 = call_loop(node, symbol_table_1,0,[])
    return value_to_call.execute(args,symbol_table_2)

def call_loop(node:Node=Node(), symbol_table:SymbolTable=SymbolTable(), idx:int=0, args:list=[]):
    print(len(node.arg_nodes), idx)
    if len(node.arg_nodes) <= idx:
        return args, symbol_table
    visitted, symbol_table_1 = visit(node.arg_nodes[idx], symbol_table)
    args.append(visitted)
    return call_loop(node, symbol_table_1, idx+1, args)

def get_case(cases:list = [], idx:int = 0):
    return cases[idx]

def run(fn: str = '', text: str = '', symbol_table:SymbolTable= SymbolTable()):
    ast = myParser.run(fn, text)
    print('AST:',ast)
    result, new_symbol_table = interpreter(ast, symbol_table)
    print('SYMBOL_TABLE:', new_symbol_table, 'RESULT:',result)
    return result, None, new_symbol_table