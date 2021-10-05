import myParser
from myParser import TokenTypes, BinOpNode, NumberNode, UnaryOpNode, Node, VarAccesNode, VarAssignNode, IfNode,ForNode, WhileNode


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


class Number:
    def __init__(self, value=None):
        self.value = value

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

def get_case(cases:list = [], idx:int = 0):
    return cases[idx]

def run(fn: str = '', text: str = '', symbol_table:SymbolTable= SymbolTable()):
    ast, _ = myParser.run(fn, text)
    print('AST:',ast)
    result, new_symbol_table = interpreter(ast, symbol_table)
    print('SYMBOL_TABLE:', new_symbol_table, 'RESULT:',result)
    return result, None, new_symbol_table