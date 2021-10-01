import myParser
from myParser import TokenTypes
from myParser import Node
from myParser import BinOpNode, NumberNode, UnaryOpNode


def interpreter(ast):
    return visit(ast)

class Number:
    def __init__(self, value):
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

    def __repr__(self):
        return str(self.value)


def visit(node:Node) -> any: 
    if isinstance(node,NumberNode):
        return visit_NumberNode(node)
    elif isinstance(node,BinOpNode):
        return visit_BinOpNode(node)
    elif isinstance(node, UnaryOpNode):
        return visit_UnaryOpNode(node)

    no_visit_method(node)

def no_visit_method(node: Node):
    raise Exception(f'No visit_{type(node).__name__} method defined')


def visit_NumberNode(node: Node):
    return Number(node.tok.value)


def visit_BinOpNode(node: Node):
    left = visit(node.left_node)
    right = visit(node.right_node)

    if node.op_tok.type == TokenTypes.TT_PLUS:
        result = left.added_to(right)
    elif node.op_tok.type == TokenTypes.TT_MINUS:
        result = left.subtracted_by(right)
    elif node.op_tok.type == TokenTypes.TT_MUL:
        result = left.multiplied_by(right)
    elif node.op_tok.type == TokenTypes.TT_DIV:
        result = left.divided_by(right)
    return result


def visit_UnaryOpNode( node:Node):
    number = visit(node.node)

    if node.op_tok.type == TokenTypes.TT_MINUS:
        number = number.multiplied_by(Number(-1))

    return number


def run(fn: str = '', text: str = ''):
    ast, _ = myParser.run(fn, text)
    solution = interpreter(ast)
    return solution, None
