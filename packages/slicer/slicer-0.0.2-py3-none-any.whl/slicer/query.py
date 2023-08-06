import ast
import heapq


def _top_k(data, k=5, desc=True):
    result = heapq.nlargest(k, data)
    if not desc:
        result = list(reversed(result))
    return result


def _abs(data):
    return [abs(x) for x in data]


class Query:
    func_map = {
        "max": (True, max),
        "min": (True, min),
        "maxabs": (True, lambda x: max(_abs(x))),
        "minabs": (True, lambda x: min(_abs(x))),
        "top": (False, _top_k),
    }

    def __init__(self, qry):
        prefix = None
        if qry[0] in "@!~":
            prefix = qry[0]
            qry = qry[1:]

        full_ast = ast.parse(qry).body[0].value

        if prefix == "@":
            self.qry_type = "scalar"
            self.compute_time = "pre"
        elif prefix == "!":
            self.qry_type = "function"
            self.compute_time = "pre"
        elif prefix == "~":
            self.qry_type = "function"
            self.compute_time = "post"
        else:
            if isinstance(full_ast, (ast.Name, ast.Num, ast.Str, ast.NameConstant)):
                self.qry_type = "scalar"
                self.compute_time = "pre"
            elif isinstance(full_ast, ast.Call):
                self.qry_type = "function"
                self.compute_time = "post"
            else:
                self.qry_type = "unknown"
                self.compute_time = "pre"

        if self.qry_type == "scalar":
            scalar_ast = full_ast
            self._value = Query._ast_scalar_to_obj(scalar_ast)
        elif self.qry_type == "function":
            func_ast = full_ast
            func_name = func_ast.func.id
            func_args = []
            for arg_ast in func_ast.args:
                arg = Query._ast_scalar_to_obj(arg_ast)
                func_args.append(arg)

            func_kwargs = {}
            for arg_ast in func_ast.keywords:
                func_kwargs[arg_ast.arg] = Query._ast_scalar_to_obj(arg_ast.value)

            self.name = func_name
            self.args = func_args
            self.kwargs = func_kwargs
        else:  # pragma: no cover
            raise ValueError(f"Could not parse: {qry}")

    def value(self):
        if self.qry_type == "function":
            is_element, f = self.__class__.func_map[self.name]

            def eval(data):
                return f(data, *self.args, **self.kwargs)

            return is_element, eval
        elif self.qry_type == "scalar":
            return self._value

    @staticmethod
    def _ast_scalar_to_obj(scalar_ast):
        if isinstance(scalar_ast, ast.Num):
            return scalar_ast.n
        elif isinstance(scalar_ast, ast.Str):
            return scalar_ast.s
        elif isinstance(scalar_ast, ast.Name):
            return scalar_ast.id
        elif isinstance(scalar_ast, ast.NameConstant):
            return scalar_ast.value
        else:
            raise ValueError(f"Cannot parse {scalar_ast}")
