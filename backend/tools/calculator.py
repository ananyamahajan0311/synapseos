import ast
import operator

operators = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
}


def evaluate(node):
    if isinstance(node, ast.Constant):
        return node.value

    if isinstance(node, ast.BinOp):
        left = evaluate(node.left)
        right = evaluate(node.right)

        return operators[type(node.op)](left, right)

    raise Exception("Invalid expression")


def calculate(expression):
    tree = ast.parse(expression, mode="eval")

    result = evaluate(tree.body)

    return {
        "status": "success",
        "message": str(result)
    }