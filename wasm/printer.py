from .model import (
    WasmVisitor,
    Module,
    Func,
    BinaryOperation,
    Call,
    Param,
    Const,
    Local,
    SetLocal,
    GetLocal,
    Result,
)


class WasmPrinter(WasmVisitor):
    def __init__(self):
        self.indentation = 0

    def visit_module(self, module: Module):
        result = "(module\n"

        self.indentation += 1
        instructions = [instruction.accept(self) for instruction in module.instructions]
        result += "\n".join(instructions)
        self.indentation -= 1
        result += ")\n"

        return result

    def visit_param(self, param: Param):
        result = "(param "

        if param.name:
            result += param.name + " "

        result += param.type
        result += ")"

        return result

    def visit_func(self, func: Func):
        result = self.with_indentation("(func")

        if func.name:
            result += " " + func.name

        if func.import_:
            imports = " ".join([f'"{name}"' for name in func.import_])

            result += f" (import {imports})"

        if func.export:
            result += f' (export "{func.export}")'

        if func.params:
            params = [param.accept(self) for param in func.params]
            result += " " + " ".join(params)

        if func.result:
            result += " " + func.result.accept(self)

        if func.locals:
            result += "\n"
            self.indentation += 1
            locals_ = [local.accept(self) for local in func.locals]
            result += "\n".join(locals_)
            self.indentation -= 1

        if func.instructions:
            result += "\n"
            self.indentation += 1
            for instruction in func.instructions:
                result += instruction.accept(self)
            self.indentation -= 1
            result += self.with_indentation("")

        result += ")\n"

        return result

    def visit_binary_operation(self, binary_operation: BinaryOperation):
        result = self.with_indentation(f"({binary_operation.op}\n")

        self.indentation += 1
        result += binary_operation.left.accept(self)
        result += binary_operation.right.accept(self)
        self.indentation -= 1

        result += self.with_indentation(")") + "\n"

        return result

    def visit_result(self, result: Result):
        return f"(result {result.type})"

    def visit_const(self, const: Const):
        return self.with_indentation(f"({const.type}.const {const.val})") + "\n"

    def visit_local(self, local: Local):
        return self.with_indentation(f"(local {local.name} {local.type})")

    def visit_set_local(self, set_local: SetLocal):
        result = self.with_indentation(f"(set_local {set_local.name}") + "\n"

        self.indentation += 1
        result += set_local.val.accept(self)
        self.indentation -= 1

        result += self.with_indentation(")") + "\n"

        return result

    def visit_get_local(self, get_local: GetLocal):
        return self.with_indentation(f"(get_local {get_local.name})") + "\n"

    def visit_call(self, call: Call):
        result = self.with_indentation("(call\n")

        self.indentation += 1
        result += self.with_indentation(call.name) + "\n"
        for instruction in call.arguments:
            result += instruction.accept(self)
        self.indentation -= 1

        result += self.with_indentation(")") + "\n"

        return result

    def with_indentation(self, str):
        return ("    " * self.indentation) + str


def pretty_print(module: Module):
    return module.accept(WasmPrinter())
