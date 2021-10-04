from myLexer import Token
import myParser
from myParser import TokenTypes, BinOpNode, NumberNode, UnaryOpNode, Node, VarAccesNode, VarAssignNode, IfNode
import functools


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
        symbols = {**self.symbols, **{name:value}}
        return SymbolTable(symbols, self.parent )

    def insert_basic_function(self, name, value):
        self.symbol_list.append(name)
        symbols = {**self.symbols, **{name:value}}
        return SymbolTable(symbols, self.parent,self.symbol_list )

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
        #print('visit.NumberNode')
        return visit_NumberNode(node,symbol_table)
    elif isinstance(node,BinOpNode):
        #print('visit.BinOpNode')
        return visit_BinOpNode(node,symbol_table)
    elif isinstance(node, UnaryOpNode):
        #print('visit.UnaryOpNode')
        return visit_UnaryOpNode(node,symbol_table)
    elif isinstance(node, VarAccesNode):
        #print('visit.VarAccesNode')   
        return visit_VarAccesNode(node,symbol_table)
    elif isinstance(node, VarAssignNode):
        #print('visit.VarAssignNode')
        return visit_VarAssignNode(node,symbol_table)
    elif isinstance(node, IfNode):
        #print('visit.IfNode')
        return visit_IfNode(node,symbol_table)
    elif node == None:
        pass

def no_visit_method(node: Node):
    raise Exception(f'No visit_{type(node).__name__} method defined{node}')


def visit_NumberNode(node: Node,symbol_table:SymbolTable):
    return Number(node.tok.value), symbol_table

def visit_BinOpNode(node: Node,symbol_table:SymbolTable):
    left:Number = Number()
    right:Number = Number()
    left, _= visit(node.left_node,symbol_table)
    right,_= visit(node.right_node,symbol_table)
    print(node.op_tok.type)
    if node.op_tok.type == TokenTypes.TT_PLUS:
        result = left.added_to(right)
    elif node.op_tok.type == TokenTypes.TT_MINUS:
        result = left.subtracted_by(right)
    elif node.op_tok.type == TokenTypes.TT_MUL:
        result = left.multiplied_by(right)
    elif node.op_tok.type == TokenTypes.TT_DIV:
        result = left.divided_by(right)
    elif node.op_tok.type == TokenTypes.TT_EE:
        result = left.get_comparison_eq(right)
    elif node.op_tok.type == TokenTypes.TT_NE:
        result = left.get_comparison_ne(right)
    elif node.op_tok.type == TokenTypes.TT_LT:
        result = left.get_comparison_lt(right)
    elif node.op_tok.type == TokenTypes.TT_GT:
        result = left.get_comparison_gt(right)
    elif node.op_tok.type == TokenTypes.TT_LTE:
        result = left.get_comparison_lte(right)
    elif node.op_tok.type == TokenTypes.TT_GTE:
        result = left.get_comparison_gte(right)
    elif node.op_tok.matches(TokenTypes.TT_KEYWORD, 'AND'):
        result= left.anded_by(right)
    elif node.op_tok.matches(TokenTypes.TT_KEYWORD, 'OR'):
        result = left.ored_by(right)
    return result, symbol_table


def visit_UnaryOpNode(node:Node,symbol_table:SymbolTable):
    number,_ = visit(node.node,symbol_table)

    if node.op_tok.type == TokenTypes.TT_MINUS:
        number = number.multiplied_by(Number(-1))

    return number, symbol_table

def visit_VarAccesNode(node: Node,symbol_table:SymbolTable):
    vehicle_name = node.var_name_tok.value
    value = symbol_table.look_up(vehicle_name)

    if not value:
        return None, symbol_table
    return value, symbol_table
def visit_VarAssignNode(node: Node,symbol_table:SymbolTable):
    vehicle_name = node.var_name_tok.value
    value, new_symbol_table = visit(node.value_node, symbol_table)
    return value, new_symbol_table.insert(vehicle_name, value)

def visit_IfNode(node, symbol_table:SymbolTable):

    condition, symbol_table_1 = IfNode_loop(node, symbol_table)

    if condition == None and node.else_case:
        else_value, symbol_table_2 = visit(node.else_case, symbol_table_1)
        return else_value, symbol_table_2

    return condition, symbol_table_1
def IfNode_loop(node:Node, symbol_table:SymbolTable, idx=0):
    print('cases', node,len(node.cases))
    if idx == len(node.cases):
        return None, symbol_table
    condition, expr = node.cases[idx]
    condition_value, symbol_table_1 = visit(condition, symbol_table)

    if condition_value.is_true():
        expr_value, symbol_table_2  =visit(expr, symbol_table_1)
        return expr_value,symbol_table_2
    return IfNode_loop(node, symbol_table_1, idx+1)

def run(fn: str = '', text: str = '', symbol_table:SymbolTable= SymbolTable()):
    ast, _ = myParser.run(fn, text)
    # print('ast in inter',type(ast.right_node))
    value, new_symbol_table = interpreter(ast, symbol_table)
    print('new', new_symbol_table)
    print('val',value)
    print('val.type',type(value))
    return value, None, new_symbol_table