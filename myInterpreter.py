import myParser
from myParser import TokenTypes,ReturnNode,CallNode,ListNode, PrintNode,FuncDefNode, BinOpNode, NumberNode, UnaryOpNode, Node, VarAccesNode, VarAssignNode, IfNode,ForNode, WhileNode


def interpreter(ast, symbol_table):
    res, new_symbol_table = visit(ast, symbol_table)
    return res, new_symbol_table

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

    def insert_basic_function(self, name, value):
        self.symbol_list.append(name)
        return SymbolTable({**self.symbols, **{name:value}}, self.should_return,self.symbol_list )

    def copy(self):
        return self

    def __repr__(self) -> str:
        return f'SymbolTable: {self.symbols}'

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

class List(Value):
    def __init__(self, elements:list=[],symbol_table:SymbolTable= SymbolTable()):
        super().__init__(symbol_table)
        self.elements = elements

    def added_to(self, other):
        #print('add')
        self.elements.append(other)
        return self.elements

    def subtracted_by(self, other):
        #print('subbed_by')
        if isinstance(other, Number):
            try:
                self.elements.pop(other.value)
                return self.elements
            except:
                return None
        else:
            return None

    def multiplied_by(self, other):
        #print('multed_by')
        if isinstance(other, List):
            self.elements.extend(other.elements)
            return self.elements
        else:
            return None

    def divided_by(self, other):
        #print('dived_by')
        if isinstance(other, Number):
            try:
                return self.elements[other.value]
            except:
                return None
        else:
            return None
    
    def copy(self):
        return List(self.elements[:], self.symbol_table)

    def __repr__(self):
        return f'[{", ".join([str(x) for x in self.elements])}]'

Number.null = Number(0)

class Function(Value):
    def __init__(self, name, body_node, arg_names, symbol_table:SymbolTable= SymbolTable(),should_return_null:bool = False):
        super().__init__(symbol_table)
        self.name = name or "<anonymous>"
        self.body_node = body_node
        self.arg_names = arg_names
        self.should_return_null = should_return_null

    def execute(self, args, symbol_table):

        if len(args) > len(self.arg_names):
            return None, symbol_table
        if len(args) < len(self.arg_names):
            return None, symbol_table
        symbol_table_2 = self.set_args(args, 0, symbol_table)
        visitted, tmp_symbol_table =visit(self.body_node, symbol_table_2)
        key_diff = self.seperate_symbols([*symbol_table_2.symbols],[*tmp_symbol_table.symbols])
        diff = self.set_dict(key_diff,tmp_symbol_table,0, symbol_table)

        return visitted, diff

    def set_args(self, args,idx,symbol_table:SymbolTable):
        if len(args) <= idx:
            return symbol_table
        return self.set_args(args, idx+1, symbol_table.insert(self.arg_names[idx], args[idx]))
    
    def set_symbol_table(self, symbol_table):
        return Function(self.name, self.body_node, self.arg_names, symbol_table)

    def seperate_symbols(self, old_symbol_table:list, new_symbol_table:list, idx:int = 0, diff:list = []):
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
    
    def set_dict(self, key_diff:list = [], symbols_table:SymbolTable = SymbolTable(), idx:int=0, diff:SymbolTable=SymbolTable()):
        if len(key_diff) <= idx:
            return diff
        return self.set_dict(key_diff, symbols_table, idx+1, diff.insert(key_diff[idx],symbols_table.look_up(key_diff[idx])))

    def __repr__(self) -> str:
        return f'FUNCTION: (NAME: {self.name}: BODY: {self.body_node}, ARG_NAMES:{self.arg_names})'

def visit(node:Node,symbol_table:SymbolTable) -> any:
    if isinstance(node,NumberNode):
        #print(node , 'visit_NumberNode')
        return visit_NumberNode(node,symbol_table)
    elif isinstance(node,BinOpNode):
        #print(node , 'visit_BinOpNode')
        return visit_BinOpNode(node,symbol_table)
    elif isinstance(node, UnaryOpNode):
        #print(node , 'visit_UnaryOpNode')
       
        return visit_UnaryOpNode(node,symbol_table)
    elif isinstance(node, VarAccesNode):
        #print(node, 'visit_VarAccesNode')
        return visit_VarAccesNode(node,symbol_table)
    elif isinstance(node, VarAssignNode):
        #print(node, 'visit_VarAssignNode')

        return visit_VarAssignNode(node,symbol_table)
    elif isinstance(node, IfNode):
        #print(node , 'visit_IfNode')

        return visit_IfNode(node,symbol_table)
    elif isinstance(node, ForNode):
        #print(node , 'visit_ForNode')
       
        return visit_ForNode(node,symbol_table)
    elif isinstance(node, WhileNode):
        #print(node , 'visit_WhileNode')

        return visit_WhileNode(node,symbol_table)
    elif isinstance(node, FuncDefNode):
        #print(node , 'visit_FuncDefNode')

        return visit_FuncDefNode(node,symbol_table)
    elif isinstance(node, CallNode):
        #print(node , ' visit_CallNode')

        return visit_CallNode(node,symbol_table)
    elif isinstance(node, ListNode):
        #print(node , 'visit_ListNode')

        return visit_ListNode(node,symbol_table, 0, [])
    elif isinstance(node, ReturnNode):
        #print(node , 'visit_ReturnNode')

        return visit_ReturnNode(node,symbol_table)
    elif isinstance(node, PrintNode):
        #print(node , 'visit_PrintNode')

        return visit_PrintNode(node,symbol_table)
    elif node == None:
        pass

def no_visit_method(node: Node):
    raise Exception(f'No visit_{type(node).__name__} method defined{node}')

def visit_NumberNode(node: Node,symbol_table:SymbolTable):
    return Number(node.tok.value), symbol_table

def visit_BinOpNode(node: Node,symbol_table:SymbolTable):
    left:Number or Value
    right:Number or Value
    # #print('TEST',node.left_node, node.right_node)

    left, symbol_table_1 = visit(node.left_node,symbol_table)
    if symbol_table_1.should_return: return left, symbol_table_1

    right,symbol_table_2= visit(node.right_node,symbol_table_1)
    if symbol_table_2.should_return: return right, symbol_table_2

    # #print(left,right)
    # #print(type(left),type(right))
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


def visit_UnaryOpNode(node:Node,symbol_table:SymbolTable):
    number, symbol_table_1 = visit(node.node,symbol_table)
    if symbol_table_1.should_return: return number, symbol_table_1

    if node.op_tok.type == TokenTypes.TT_MINUS:
        number = number.multiplied_by(Number(-1))

    return number, symbol_table

def visit_PrintNode(node:Node,symbol_table:SymbolTable):
    printable, symbol_table_1 = visit(node.printable,symbol_table)
    #print('PRINT',printable)
    if symbol_table_1.should_return: return printable, symbol_table_1
    return printable, symbol_table_1

def visit_VarAccesNode(node: Node,symbol_table:SymbolTable):
    value = symbol_table.look_up(node.var_name_tok.value)
    if not value:
        return None, symbol_table
    return value, symbol_table

def visit_VarAssignNode(node: Node,symbol_table:SymbolTable):
    value, symbol_table_1 = visit(node.value_node, symbol_table)
    if symbol_table_1.should_return: return value, symbol_table_1
    return value, symbol_table_1.insert(node.var_name_tok.value, value)

def visit_IfNode(node: Node, symbol_table:SymbolTable):
    condition, symbol_table_1 = IfNode_loop(node, symbol_table)
    if symbol_table_1.should_return: return condition, symbol_table_1
    if node.else_case:
        expr, should_return_null = node.else_case
        if expr != None:
            else_value, symbol_table_2 = visit(expr, symbol_table_1)
            if symbol_table_2.should_return: return else_value, symbol_table_2
            return Number.null if should_return_null else else_value, symbol_table_2
    return condition, symbol_table_1

def IfNode_loop(node:Node, symbol_table:SymbolTable, idx=0):
    if idx == len(node.cases):
        return Number.null , symbol_table
    condition, expr, should_return_null = get_case(node.cases, idx)
    condition_value, symbol_table_1 = visit(condition, symbol_table)
    if symbol_table_1.should_return: return condition_value, symbol_table_1
    if condition_value.is_true():
        expr_value, symbol_table_2 = visit(expr, symbol_table_1)
        if symbol_table_2.should_return: return expr_value, symbol_table_2
        return expr_value,symbol_table_2
    return IfNode_loop(node, symbol_table_1, idx+1)

def visit_ForNode(node:Node, symbol_table:SymbolTable):
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

def ForNode_loop(node:Node, symbol_table:SymbolTable, start_value:int, end_value:int, step_value:int,elements:list ):
    if step_value >= 0:
        if start_value > end_value:
            return Number.null if node.should_return_null else List(elements), symbol_table
    else: 
        if start_value < end_value:
            return Number.null if node.should_return_null else List(elements), symbol_table
    value, symbol_table_2 = visit(node.body_node, symbol_table.insert(node.var_name_tok.value, Number(start_value)))
    if symbol_table_2.should_return: return value, symbol_table_2

    elements.append(value)
    return ForNode_loop(node, symbol_table_2.insert(node.var_name_tok.value, Number(start_value)), start_value + step_value, end_value, step_value)

def visit_WhileNode(node:Node, symbol_table:SymbolTable,elements:list = []):
    condition, symbol_table_1 = visit(node.condition_node, symbol_table)
    if symbol_table_1.should_return: return condition, symbol_table_1

    if not condition.is_true(): return Number.null if node.should_return_null else List(elements), symbol_table_1
    value, symbol_table_2 = visit(node.body_node, symbol_table_1)
    if symbol_table_2.should_return: return value, symbol_table_2

    elements.append(value)
    return visit_WhileNode(node, symbol_table_2,elements)

def visit_ListNode(node:Node=Node(), symbol_table:SymbolTable=SymbolTable(), idx:int=0, elements:list = []):
    if node.element_nodes is None:
        return elements, symbol_table
    if len(node.element_nodes) <= idx:
        return List(elements), symbol_table
    visitted, symbol_table_1 = visit(node.element_nodes[idx], symbol_table)
    if symbol_table_1.should_return: return visitted, symbol_table_1
    elements.append(visitted)
    # #print(elements)
    return visit_ListNode(node, symbol_table_1,idx+1, elements)

def visit_FuncDefNode(node:Node=Node(), symbol_table:SymbolTable=SymbolTable()):
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
def visit_CallNode(node:Node=Node(), symbol_table:SymbolTable=SymbolTable()):
    value_to_call, symbol_table_1 = visit(node.node_to_call, symbol_table)
    if symbol_table_1.should_return: return value_to_call, symbol_table_1
    args, symbol_table_2 = call_loop(node, symbol_table_1,0,[])
    # #print(node.node_to_call)
    return value_to_call.execute(args,symbol_table_2)

def call_loop(node:Node=Node(), symbol_table:SymbolTable=SymbolTable(), idx:int=0, args:list=[]):
    if len(node.arg_nodes) <= idx:
        return args, symbol_table
    visitted, symbol_table_1 = visit(node.arg_nodes[idx], symbol_table)
    if symbol_table_1.should_return: return visitted, symbol_table_1

    args.append(visitted)
    return call_loop(node, symbol_table_1, idx+1, args)
    
def visit_ReturnNode(node:Node=Node(), symbol_table:SymbolTable=SymbolTable()):
    if node.node_to_return:
        value, symbol_table_1 = visit(node.node_to_return, symbol_table)
        #print(value)
        if symbol_table_1.should_return: return value, symbol_table_1
        symbol_table_1.should_return = True
        return value, symbol_table_1
    else:
        value = Number.null
        return value, symbol_table


def get_case(cases:list = [], idx:int = 0):
    return cases[idx]

def run(fn: str = '', text: str = '', symbol_table:SymbolTable= SymbolTable()):
    ast = myParser.run(fn, text)
    print('AST:',ast)
    if ast == None: return None, None, symbol_table
    result, new_symbol_table = interpreter(ast, symbol_table)
    # #print('SYMBOL_TABLE:', new_symbol_table, 'RESULT:',result)
    return result, None, new_symbol_table