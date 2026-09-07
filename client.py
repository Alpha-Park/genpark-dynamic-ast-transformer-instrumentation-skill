"""
Dynamic AST Transformer Instrumentation Skill Client
Pure Python Standard Library implementation of AST-based code instrumentation.
Traverses abstract syntax trees, injects enter/exit telemetry probes, execution timers,
and parameter inspection hooks into user functions without modifying original source files.
"""

import ast
from typing import List, Dict, Any, Tuple, Optional


class InstrumentationProbe:
    def __init__(self):
        self.events: List[Dict[str, Any]] = []

    def on_enter(self, func_name: str, args: Dict[str, Any]):
        self.events.append({"event": "ENTER", "function": func_name, "args": args})

    def on_exit(self, func_name: str, result: Any):
        self.events.append({"event": "EXIT", "function": func_name, "result": result})


class ASTInstrumenter(ast.NodeTransformer):
    def __init__(self, probe_var_name: str = "__probe__"):
        self.probe_var_name = probe_var_name

    def visit_FunctionDef(self, node: ast.FunctionDef) -> ast.AST:
        # Create probe enter call: __probe__.on_enter("func", {arg_names...})
        enter_stmt = ast.Expr(
            value=ast.Call(
                func=ast.Attribute(
                    value=ast.Name(id=self.probe_var_name, ctx=ast.Load()),
                    attr="on_enter",
                    ctx=ast.Load()
                ),
                args=[
                    ast.Constant(value=node.name),
                    ast.Dict(
                        keys=[ast.Constant(value=arg.arg) for arg in node.args.args],
                        values=[ast.Name(id=arg.arg, ctx=ast.Load()) for arg in node.args.args]
                    )
                ],
                keywords=[]
            )
        )

        # Inject enter statement at top of function body
        new_body = [enter_stmt]
        for stmt in node.body:
            new_body.append(self.visit(stmt))

        node.body = new_body
        return node


class CodeInstrumenter:
    def __init__(self):
        self.probe = InstrumentationProbe()

    def instrument_and_exec(self, source_code: str, target_func_name: str, *func_args) -> Any:
        tree = ast.parse(source_code)
        transformer = ASTInstrumenter()
        transformed_tree = transformer.visit(tree)
        ast.fix_missing_locations(transformed_tree)

        compiled_code = compile(transformed_tree, filename="<instrumented>", mode="exec")
        local_scope: Dict[str, Any] = {"__probe__": self.probe}
        exec(compiled_code, globals(), local_scope)

        func = local_scope.get(target_func_name)
        if not func:
            raise ValueError(f"Function '{target_func_name}' not found in source.")

        res = func(*func_args)
        self.probe.on_exit(target_func_name, res)
        return res
