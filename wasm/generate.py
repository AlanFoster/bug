from .model import WasmVisitor, Module, Func, BinaryOperation, Call, Param, Const


class WasmPrinter(WasmVisitor):
    def __init__(self):
        self.indentation = 0

    def visitModule(self, module: Module):
        result = "(module\n"

        self.indentation += 1
        for instruction in module.instructions:
            result += instruction.accept(self) + "\n"
        self.indentation -= 1
        result += ")\n"

        return result

    def visitParam(self, param: Param):
        return self.with_indentation(f"(param {param.type})") + "\n"

    def visitFunc(self, func: Func):
        result = self.with_indentation("(func\n")

        self.indentation += 1

        if func.name:
            result += self.with_indentation(func.name) + "\n"

        if func.import_:
            imports = " ".join([f'"{name}"' for name in func.import_])

            result += self.with_indentation(f"(import {imports})") + "\n"

        if func.export:
            result += self.with_indentation(f'(export "{func.export}")') + "\n"

        if func.params:
            for param in func.params:
                result += param.accept(self)

        if func.instructions:
            for instruction in func.instructions:
                result += instruction.accept(self)
        self.indentation -= 1
        result += self.with_indentation(")") + "\n"

        return result

    def visitBinaryOperation(self, binary_operation: BinaryOperation):
        result = self.with_indentation(f"({binary_operation.op}\n")

        self.indentation += 1
        result += binary_operation.left.accept(self)
        result += binary_operation.right.accept(self)
        self.indentation -= 1

        result += self.with_indentation(")") + "\n"

        return result

    def visitConst(self, const: Const):
        return self.with_indentation(f"({const.val_type}.const {const.val})") + "\n"

    def visitCall(self, call: Call):
        result = self.with_indentation("(call\n")

        self.indentation += 1
        result += self.with_indentation(call.var) + "\n"
        for instruction in call.arguments:
            result += instruction.accept(self)
        self.indentation -= 1

        result += self.with_indentation(")") + "\n"

        return result

    def with_indentation(self, str):
        return ("    " * self.indentation) + str


def generate(module: Module):
    return module.accept(WasmPrinter())
