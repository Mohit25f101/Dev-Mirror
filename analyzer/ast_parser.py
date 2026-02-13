import ast

CONTROL_NODES = (ast.If, ast.For, ast.While, ast.Try, ast.With)


class CodeAnalyzer(ast.NodeVisitor):

    def __init__(self):
        self.function_count = 0
        self.function_lengths = []
        self.current_depth = 0
        self.max_depth = 0

    def visit_FunctionDef(self, node):
        self.function_count += 1
        start_line = node.lineno
        end_line = max(
            getattr(n, "lineno", start_line) for n in ast.walk(node))
        self.function_lengths.append(end_line - start_line + 1)
        self.generic_visit(node)

    def visit(self, node):
        if isinstance(node, CONTROL_NODES):
            self.current_depth += 1
            self.max_depth = max(self.max_depth, self.current_depth)
            super().visit(node)
            self.current_depth -= 1
        else:
            super().visit(node)


def parse_code(code: str) -> dict:
    try:
        tree = ast.parse(code)
    except SyntaxError:
        return {"error": "Invalid Python code"}

    analyzer = CodeAnalyzer()
    analyzer.visit(tree)

    avg_function_length = (sum(analyzer.function_lengths) /
                           len(analyzer.function_lengths)
                           if analyzer.function_lengths else 0)

    return {
        "function_count": analyzer.function_count,
        "avg_function_length": round(avg_function_length, 2),
        "max_nesting_depth": analyzer.max_depth
    }
