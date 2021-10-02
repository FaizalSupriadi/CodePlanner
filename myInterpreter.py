from myLexer import Token
import myParser
from myParser import TokenTypes, BinOpNode, NumberNode, UnaryOpNode, Node, VarAccesNode, VarAssignNode
import functools


def interpreter(ast, symbol_table):
    res, _ = visit(ast, symbol_table)
    return res, _

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
    def __init__(self, value):
        self.value = value

    def added_to(self, other):
        print('other',other)
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

    def __repr__(self):
        return 'NUMBER():' + str(self.value)


def visit(node:Node,symbol_table:SymbolTable) -> any:
    if isinstance(node,NumberNode):
        print('visit.NumberNode')
        return visit_NumberNode(node,symbol_table)
    elif isinstance(node,BinOpNode):
        print('visit.BinOpNode')
        return visit_BinOpNode(node,symbol_table)
    elif isinstance(node, UnaryOpNode):
        print('visit.UnaryOpNode')
        return visit_UnaryOpNode(node,symbol_table)
    elif isinstance(node, VarAccesNode):
        print('visit.VarAccesNode')   
        return visit_VarAccesNode(node,symbol_table)
    elif isinstance(node, VarAssignNode):
        print('visit.VarAssignNode')
        return visit_VarAssignNode(node,symbol_table)
    elif node == None:
        pass

def no_visit_method(node: Node):
    raise Exception(f'No visit_{type(node).__name__} method defined{node}')


def visit_NumberNode(node: Node,symbol_table:SymbolTable):
    print('num',node)
    return Number(node.tok.value), symbol_table

def visit_BinOpNode(node: Node,symbol_table:SymbolTable):
    print('llllll',type(node.left_node), node.right_node)
    left, _= visit(node.left_node,symbol_table)
    right,_= visit(node.right_node,symbol_table)
    print('left', type(left), right)

    if node.op_tok.type == TokenTypes.TT_PLUS:
        result = left.added_to(right)
        print(result)
    elif node.op_tok.type == TokenTypes.TT_MINUS:
        result = left.subtracted_by(right)
    elif node.op_tok.type == TokenTypes.TT_MUL:
        result = left.multiplied_by(right)
    elif node.op_tok.type == TokenTypes.TT_DIV:
        result = left.divided_by(right)
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
    print('valueee',type(value))
    return value, symbol_table
def visit_VarAssignNode(node: Node,symbol_table:SymbolTable):
    vehicle_name = node.var_name_tok.value
    value, _ = visit(node.value_node, symbol_table)
    return value, symbol_table.insert(vehicle_name, value)



def run(fn: str = '', text: str = '', symbol_table:SymbolTable= SymbolTable()):
    ast, _ = myParser.run(fn, text)
    print('ast in inter',ast)
    value, new_symbol_table = interpreter(ast, symbol_table)
    print('val',value)
    print('val.type',type(value))
    return value, None, new_symbol_table