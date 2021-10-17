from typing import Tuple
from myLexer import Error
import myParser
from myParser import TokenTypes,DestinationNode,CallNode,ListNode, PrintNode,FuncDefNode, BinOpNode, NumberNode, UnaryOpNode, Node, VarAccesNode, VarAssignNode, IfNode,ForNode, WhileNode
from myClock import Clock


# The symbol table contains all the variables or functions that have been made
# By calling the correct name you can use the corresponding value
class SymbolTable:
    def __init__(self, symbols:dict={}, should_return:bool=False, symbol_list:list=[]) -> None:
        self.symbols = symbols
        self.symbol_list = symbol_list
        self.should_return = should_return

    def look_up(self, name):
        value = self.symbols.get(name, None)
        if value == None:
            return None
        return value

    def insert(self, name, value):
        if name in self.symbol_list:
            return SymbolTable(self.symbols, self.should_return )
        return SymbolTable({**self.symbols, **{name:value}}, self.should_return )

    def insert_static(self, name, value):
        self.symbol_list.append(name)
        return SymbolTable({**self.symbols, **{name:value}}, self.should_return,self.symbol_list )

    def copy(self):
        return self

    def __repr__(self) -> str:
        return f'SymbolTable: {self.symbols}'

# Value is a class that is used to make sure that value is not used in the binopnode
class Value:
    def __init__(self,symbol_table:SymbolTable = SymbolTable()):
        self.symbol_table = symbol_table

    #(self, other: Value)
    def added_to(self, other) -> Tuple[None, None]:
        return None, self.illegal_operation(other)

    #(self, other: Value)
    def subbed_by(self, other) -> Tuple[None, None]:
        return None, self.illegal_operation(other)

    #(self, other: Value)
    def multed_by(self, other) -> Tuple[None, None]:
        return None, self.illegal_operation(other)

    #(self, other: Value)
    def dived_by(self, other) -> Tuple[None, None]:
        return None, self.illegal_operation(other)

    #(self, other: Value)
    def powed_by(self, other) -> Tuple[None, None]:
        return None, self.illegal_operation(other)

    #(self, other: Value)
    def get_comparison_eq(self, other) -> Tuple[None, None]:
        return None, self.illegal_operation(other)

    #(self, other: Value)
    def get_comparison_ne(self, other) -> Tuple[None, None]:
        return None, self.illegal_operation(other)

    #(self, other: Value)
    def get_comparison_lt(self, other) -> Tuple[None, None]:
        return None, self.illegal_operation(other)

    #(self, other: Value)
    def get_comparison_gt(self, other) -> Tuple[None, None]:
        return None, self.illegal_operation(other)

    #(self, other: Value)
    def get_comparison_lte(self, other) -> Tuple[None, None]:
        return None, self.illegal_operation(other)

    #(self, other: Value)
    def get_comparison_gte(self, other) -> Tuple[None, None]:
        return None, self.illegal_operation(other)

    #(self, other: Value)
    def anded_by(self, other) -> Tuple[None, None]:
        return None, self.illegal_operation(other)

    #(self, other: Value)
    def ored_by(self, other) -> Tuple[None, None]:
        return None, self.illegal_operation(other)

    #(self, other: Value)
    def notted(self,other) -> Tuple[None, None]:
        return None, self.illegal_operation(other)

    def is_true(self) -> bool:
        return False

    def illegal_operation(self, other=None):
        if not other: other = self
        return None

# Number is a class used to do calculations
class Number:
    def __init__(self, value=None):
        self.value = value

    #(self, other: Number) -> Number
    def added_to(self, other):
        if isinstance(other, Number):
            return Number(self.value + other.value)

    #(self, other: Number) -> Number
    def subtracted_by(self, other):
        if isinstance(other, Number):
            return Number(self.value - other.value)
            
    #(self, other: Number) -> Number
    def multiplied_by(self, other):
        if isinstance(other, Number):
            return Number(self.value * other.value)

    #(self, other: Number) -> Number
    def divided_by(self, other):
        if isinstance(other, Number):
            if other.value == 0:
                return None
            return Number(self.value / other.value)

    #(self, other: Number) -> Number
    def get_comparison_eq(self, other):
        if isinstance(other, Number):
            return Number(int(self.value == other.value))
            
    #(self, other: Number) -> Number
    def get_comparison_ne(self, other):
        if isinstance(other, Number):
            return Number(int(self.value != other.value))

    #(self, other: Number) -> Number
    def get_comparison_lt(self, other):
        if isinstance(other, Number):
            return Number(int(self.value < other.value))

    #(self, other: Number) -> Number
    def get_comparison_gt(self, other):
        if isinstance(other, Number):
            return Number(int(self.value > other.value))

    #(self, other: Number) -> Number
    def get_comparison_lte(self, other):
        if isinstance(other, Number):
            return Number(int(self.value <= other.value))

    #(self, other: Number) -> Number
    def get_comparison_gte(self, other):
        if isinstance(other, Number):
            return Number(int(self.value >= other.value))

    #(self, other: Number) -> Number
    def anded_by(self, other):
        if isinstance(other, Number):
            return Number(int(self.value and other.value))

    #(self, other: Number) -> Number
    def ored_by(self, other):
        if isinstance(other, Number):
            return Number(int(self.value or other.value))

    #(self) -> Number
    def notted(self):
        return Number(1 if self.value == 0 else 0)
    
    def is_true(self) -> bool:
        return self.value != 0

    def __repr__(self) -> str:
        return str(self.value)
# List inherits value and will use their functions to append, pop, to get the value at index and add at index
class List(Value):
    def __init__(self, elements:list=[],symbol_table:SymbolTable= SymbolTable()):
        super().__init__(symbol_table)
        self.elements = elements

    def added_to(self, other:Number) -> list or None:
        self.elements.append(other)
        return self.elements

    def subtracted_by(self, other:Number) -> list or None:
        if isinstance(other, Number):
            try:
                self.elements.pop(other.value)
                return self.elements
            except:
                return None
        else:
            return None

    def multiplied_by(self, other:Number) -> list or None:
        if isinstance(other, List):
            index = other.elements[0].value
            if len(self.elements) < index:
                self.elements.append(other.elements[1])
            else:
                self.elements[index] = other.elements[1]
            return self.elements
        else:
            return None

    def divided_by(self, other:Number) -> list or None:
        if isinstance(other, Number):
            try:
                return self.elements[other.value]
            except:
                return None
        else:
            return None
    # copy(self) -> List
    def copy(self):
        return List(self.elements[:], self.symbol_table)

    def __repr__(self) -> str:
        return f'[{", ".join([str(x) for x in self.elements])}]'

Number.null = Number(0)
# The function class inherits value and will execute the given arguments
class Function(Value):
    def __init__(self, name, body_node, arg_names, symbol_table:SymbolTable= SymbolTable(),should_return_null:bool = False):
        super().__init__(symbol_table)
        self.name = name or "<anonymous>"
        self.body_node = body_node
        self.arg_names = arg_names
        self.should_return_null = should_return_null

    def execute(self, args, symbol_table) -> Tuple[any, SymbolTable]:

        if len(args) > len(self.arg_names):
            return None, symbol_table
        if len(args) < len(self.arg_names):
            return None, symbol_table
        symbol_table_2 = self.set_args(args, 0, symbol_table)
        visitted, tmp_symbol_table =visit(self.body_node, symbol_table_2)
        key_diff = self.seperate_symbols([*symbol_table_2.symbols],[*tmp_symbol_table.symbols])
        diff = self.set_dict(key_diff,tmp_symbol_table,0, symbol_table)

        return visitted, diff
    # The functions set_args, set_symbol_table, seperate_symbols and set_dict 
    # are used to remove values from the symbol table that do not belong there
    def set_args(self, args,idx,symbol_table:SymbolTable) -> SymbolTable:
        if len(args) <= idx:
            return symbol_table
        return self.set_args(args, idx+1, symbol_table.insert(self.arg_names[idx], args[idx]))

    # set_symbol_table(self, symbol_table) -> Function:
    def set_symbol_table(self, symbol_table):
        return Function(self.name, self.body_node, self.arg_names, symbol_table)

    def seperate_symbols(self, old_symbol_table:list, new_symbol_table:list, idx:int = 0, diff:list = []) -> SymbolTable:
        if len(old_symbol_table) <= idx:
            if len(new_symbol_table) > idx:
                diff.append(new_symbol_table[idx])
                return self.seperate_symbols(old_symbol_table, new_symbol_table, idx+1, diff)
            else: return diff
        if len(new_symbol_table) <= idx:
            return diff
        if old_symbol_table[idx] != new_symbol_table[idx]:
            diff.append(new_symbol_table[idx])
        return self.seperate_symbols(old_symbol_table, new_symbol_table, idx+1, diff)
    
    def set_dict(self, key_diff:list = [], symbols_table:SymbolTable = SymbolTable(), idx:int=0, diff:SymbolTable=SymbolTable()) -> SymbolTable:
        if len(key_diff) <= idx:
            return diff
        return self.set_dict(key_diff, symbols_table, idx+1, diff.insert(key_diff[idx],symbols_table.look_up(key_diff[idx])))

    def __repr__(self) -> str:
        return f'FUNCTION: (NAME: {self.name}: BODY: {self.body_node}, ARG_NAMES:{self.arg_names})'

# This function will guide the node to the correct function
def visit(node:Node,symbol_table:SymbolTable) -> Tuple[any, SymbolTable]:
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
    elif isinstance(node, ListNode):
        return visit_ListNode(node,symbol_table, 0, [])
    elif isinstance(node, DestinationNode):
        return visit_DestinationNode(node,symbol_table)
    elif isinstance(node, PrintNode):
        return visit_PrintNode(node,symbol_table)
    elif node == None:
        return None, symbol_table

# Create and return number class
def visit_NumberNode(node: Node,symbol_table:SymbolTable) -> Tuple[Number, SymbolTable]:
    return Number(node.tok.value), symbol_table

# This is used to calculate numbers or to use a list function
def visit_BinOpNode(node: Node,symbol_table:SymbolTable) -> Tuple[Number or Value, SymbolTable]:
    left:Number or Value
    right:Number or Value

    left, symbol_table_1 = visit(node.left_node,symbol_table)
    if symbol_table_1.should_return: return left, symbol_table_1

    right,symbol_table_2= visit(node.right_node,symbol_table_1)
    if symbol_table_2.should_return: return right, symbol_table_2

    if node.op_tok.type == TokenTypes.TT_PLUS:
        return left.added_to(right), symbol_table_2
    elif node.op_tok.type == TokenTypes.TT_MINUS:
        return left.subtracted_by(right), symbol_table_2
    elif node.op_tok.type == TokenTypes.TT_MUL:
        return left.multiplied_by(right), symbol_table_2
    elif node.op_tok.type == TokenTypes.TT_DIV:
        return left.divided_by(right), symbol_table_2
    elif node.op_tok.type == TokenTypes.TT_EE:
        return left.get_comparison_eq(right), symbol_table_2
    elif node.op_tok.type == TokenTypes.TT_NE:
        return left.get_comparison_ne(right), symbol_table_2
    elif node.op_tok.type == TokenTypes.TT_LT:
        return left.get_comparison_lt(right), symbol_table_2
    elif node.op_tok.type == TokenTypes.TT_GT:
        return left.get_comparison_gt(right), symbol_table_2
    elif node.op_tok.type == TokenTypes.TT_LTE:
        return left.get_comparison_lte(right), symbol_table_2
    elif node.op_tok.type == TokenTypes.TT_GTE:
        return left.get_comparison_gte(right), symbol_table_2
    elif node.op_tok.matches(TokenTypes.TT_KEYWORD, 'AND'):
        return left.anded_by(right), symbol_table_2
    elif node.op_tok.matches(TokenTypes.TT_KEYWORD, 'OR'):
        return left.ored_by(right), symbol_table_2
    return None, symbol_table_2

# This will take into account negative numbers
def visit_UnaryOpNode(node:Node,symbol_table:SymbolTable) -> Tuple[Number, SymbolTable]:
    number, symbol_table_1 = visit(node.node,symbol_table)
    if symbol_table_1.should_return: return number, symbol_table_1

    if node.op_tok.type == TokenTypes.TT_MINUS:
        number = number.multiplied_by(Number(-1))

    return number, symbol_table

# This will print the given value
def visit_PrintNode(node:Node,symbol_table:SymbolTable) -> Tuple[str, SymbolTable]:
    printable, symbol_table_1 = visit(node.printable,symbol_table)
    print("PRINT:",printable)
    if symbol_table_1.should_return: return printable, symbol_table_1
    return "PRINTED", symbol_table_1

# This gives acces to the symboltable and will return the given value corresponding to the name
def visit_VarAccesNode(node: Node,symbol_table:SymbolTable) -> Tuple[any, SymbolTable]:
    value = symbol_table.look_up(node.var_name_tok.value)
    if not value:
        return None, symbol_table
    return value, symbol_table
# Assign a name to its value and set it in the symbol_table
def visit_VarAssignNode(node: Node,symbol_table:SymbolTable) -> Tuple[any, SymbolTable]:
    value, symbol_table_1 = visit(node.value_node, symbol_table)
    if symbol_table_1.should_return: return value, symbol_table_1
    return value, symbol_table_1.insert(node.var_name_tok.value, value)

# This will handle the if statements
def visit_IfNode(node: Node, symbol_table:SymbolTable) -> Tuple[any, SymbolTable]:
    condition, symbol_table_1 = IfNode_loop(node, symbol_table)
    if symbol_table_1.should_return: return condition, symbol_table_1
    if condition == None and node.else_case:
        expr, should_return_null = node.else_case
        if expr != None:
            else_value, symbol_table_2 = visit(expr, symbol_table_1)
            if symbol_table_2.should_return: return else_value, symbol_table_2
            return Number.null if should_return_null else else_value, symbol_table_2
    return condition, symbol_table_1

def IfNode_loop(node:Node, symbol_table:SymbolTable, idx=0) -> Tuple[any, SymbolTable]:
    if idx == len(node.cases):
        return None , symbol_table
    condition, expr, _ = get_case(node.cases, idx)
    condition_value, symbol_table_1 = visit(condition, symbol_table)
    if symbol_table_1.should_return: return condition_value, symbol_table_1
    if condition_value.is_true():
        expr_value, symbol_table_2 = visit(expr, symbol_table_1)
        if symbol_table_2.should_return: return expr_value, symbol_table_2
        return expr_value,symbol_table_2
    return IfNode_loop(node, symbol_table_1, idx+1)

# This will handle the for loops
def visit_ForNode(node:Node, symbol_table:SymbolTable) -> Tuple[Number or List, SymbolTable]:
    elements = []
    start_value, symbol_table_1 = visit(node.start_value_node, symbol_table)
    if symbol_table_1.should_return: return start_value, symbol_table_1

    end_value, symbol_table_2 = visit(node.end_value_node, symbol_table_1)
    if symbol_table_2.should_return: return end_value, symbol_table_2
    if node.step_value_node:
        step_value, symbol_table_3 = visit(node.end_value_node, symbol_table_2)
        if symbol_table_3.should_return: return step_value, symbol_table_3
        return ForNode_loop(node, symbol_table_3, start_value.value, end_value.value, step_value.value, elements)
    else:
        return ForNode_loop(node, symbol_table_2, start_value.value, end_value.value, 1, elements)
def ForNode_loop(node:Node, symbol_table:SymbolTable, start_value:int, end_value:int, step_value:int,elements:list ) -> Tuple[List, SymbolTable]:
    if step_value >= 0:
        if start_value > end_value:
            return Number.null if node.should_return_null else List(elements), symbol_table
    else: 
        if start_value < end_value:
            return Number.null if node.should_return_null else List(elements), symbol_table
    value, symbol_table_2 = visit(node.body_node, symbol_table.insert(node.var_name_tok.value, Number(start_value)))
    if symbol_table_2.should_return: return value, symbol_table_2

    elements.append(value)
    return ForNode_loop(node, symbol_table_2.insert(node.var_name_tok.value, Number(start_value)), start_value + step_value, end_value, step_value, elements)

# This will handle the while loops
def visit_WhileNode(node:Node, symbol_table:SymbolTable,elements:list = []) -> Tuple[any, SymbolTable]:
    condition, symbol_table_1 = visit(node.condition_node, symbol_table)
    if symbol_table_1.should_return: return condition, symbol_table_1

    if not condition.is_true(): return Number.null if node.should_return_null else List(elements), symbol_table_1
    value, symbol_table_2 = visit(node.body_node, symbol_table_1)
    if symbol_table_2.should_return: return value, symbol_table_2

    elements.append(value)
    return visit_WhileNode(node, symbol_table_2,elements)

# This will handle the List loops
def visit_ListNode(node:Node=Node(), symbol_table:SymbolTable=SymbolTable(), idx:int=0, elements:list = []) -> Tuple[any, SymbolTable]:
    if node.element_nodes is None:
        return elements, symbol_table
    if len(node.element_nodes) <= idx:
        return List(elements), symbol_table
    visitted, symbol_table_1 = visit(node.element_nodes[idx], symbol_table)
    if symbol_table_1.should_return: return visitted, symbol_table_1
    elements.append(visitted)
    return visit_ListNode(node, symbol_table_1,idx+1, elements)

# This will create a function class and put it inside the symbol table
def visit_FuncDefNode(node:Node=Node(), symbol_table:SymbolTable=SymbolTable()) -> Tuple[any, SymbolTable]:
    func_name = node.var_name_tok.value if node.var_name_tok else None
    func_value = Function(
        func_name, 
        node.body_node, 
        [arg_name.value for arg_name in node.arg_name_toks], 
        symbol_table,
        node.should_return_null
        )
    if node.var_name_tok:
        symbol_table_1 = symbol_table.insert(func_name, func_value)
        return func_value.set_symbol_table(symbol_table_1), symbol_table_1

    return func_value, symbol_table

# This will call the given function name
def visit_CallNode(node:Node=Node(), symbol_table:SymbolTable=SymbolTable()) -> Tuple[any, SymbolTable]:
    value_to_call, symbol_table_1 = visit(node.node_to_call, symbol_table)
    if symbol_table_1.should_return: return value_to_call, symbol_table_1
    args, symbol_table_2 = call_loop(node, symbol_table_1,0,[])
    return value_to_call.execute(args,symbol_table_2)

def call_loop(node:Node=Node(), symbol_table:SymbolTable=SymbolTable(), idx:int=0, args:list=[]) -> Tuple[list, SymbolTable]:
    if len(node.arg_nodes) <= idx:
        return args, symbol_table
    visitted, symbol_table_1 = visit(node.arg_nodes[idx], symbol_table)
    if symbol_table_1.should_return: return visitted, symbol_table_1

    args.append(visitted)
    return call_loop(node, symbol_table_1, idx+1, args)

# This will handle the return statement
def visit_DestinationNode(node:Node=Node(), symbol_table:SymbolTable=SymbolTable()) -> Tuple[any, SymbolTable]:
    if node.node_to_return:
        value, symbol_table_1 = visit(node.node_to_return, symbol_table)
        if symbol_table_1.should_return: return value, symbol_table_1
        symbol_table_1.should_return = True
        return value, symbol_table_1
    else:
        value = Number.null
        return value, symbol_table


def get_case(cases:list = [], idx:int = 0) -> list:
    return cases[idx]

def interpreter(ast:list=[], symbol_table:SymbolTable = SymbolTable()) -> Tuple[any, SymbolTable]:
    res, new_symbol_table = visit(ast, symbol_table)
    return res, new_symbol_table
    
@Clock.time_this
def run(fn: str = '', text: str = '', symbol_table:SymbolTable= SymbolTable()) -> Tuple[any, Error, SymbolTable]:
    ast, error = myParser.run(fn, text)
    if ast == None: return None, error, symbol_table
    result, new_symbol_table = interpreter(ast, symbol_table)
    return result, error, new_symbol_table