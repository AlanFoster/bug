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
    If,
    Return,
    Drop,
    Nop,
    Memory,
    SetGlobal,
    GetGlobal,
    Global,
    Import,
    Store,
)


class WasmPrinter(WasmVisitor):
    def __init__(self):
        self.indentation = 0

    def visit_module(self, module: Module):
        result = "(module\n"

        self.indentation += 1
        imports = [import_.accept(self) for import_ in module.imports]
        result += "\n".join(imports)
        instructions = [instruction.accept(self) for instruction in module.instructions]
        result += "\n".join(instructions)
        self.indentation -= 1
        result += ")\n"

        return result

    def visit_import(self, import_: Import):
        result = self.with_indentation("(func")

        if import_.name:
            result += " " + import_.name

        if import_.import_:
            imports = " ".join([f'"{name}"' for name in import_.import_])

            result += f" (import {imports})"

        if import_.params:
            params = [param.accept(self) for param in import_.params]
            result += " " + " ".join(params)

        if import_.result.type is not None:
            result += " " + import_.result.accept(self)

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

        if func.export:
            result += f' (export "{func.export}")'

        if func.params:
            params = [param.accept(self) for param in func.params]
            result += " " + " ".join(params)

        if func.result.type is not None:
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

    def visit_if(self, if_: If):
        result = self.with_indentation("(if\n")

        self.indentation += 1
        if if_.result.type is not None:
            result += self.with_indentation(if_.result.accept(self)) + "\n"

        if if_.condition:
            result += if_.condition.accept(self)

        result += self.with_indentation("(then") + "\n"
        self.indentation += 1
        for instruction in if_.then_statements:
            result += instruction.accept(self)
        self.indentation -= 1
        result += self.with_indentation(")") + "\n"

        if if_.else_statements:
            result += self.with_indentation("(else") + "\n"
            self.indentation += 1
            for instruction in if_.else_statements:
                result += instruction.accept(self)
            self.indentation -= 1
            result += self.with_indentation(")") + "\n"
        self.indentation -= 1
        result += self.with_indentation(")") + "\n"

        return result

    def visit_drop(self, _drop: Drop):
        return self.with_indentation("(drop)") + "\n"

    def visit_return(self, return_: Return):
        result = self.with_indentation("(return")

        if return_.expression:
            result += "\n"
            self.indentation += 1
            result += return_.expression.accept(self)
            self.indentation -= 1
            result += self.with_indentation(")") + "\n"
        else:
            result += ")\n"

        return result

    def visit_nop(self, nop: Nop):
        return self.with_indentation("(nop)") + "\n"

    def visit_global(self, global_: Global):
        result = self.with_indentation(f"(global {global_.name} ({global_.type})")
        result += "\n"
        self.indentation += 1
        result += global_.value.accept(self)
        self.indentation -= 1
        result += self.with_indentation(")") + "\n"

        return result

    def visit_get_global(self, get_global: GetGlobal):
        return self.with_indentation(f"(global.get {get_global.name})") + "\n"

    def visit_set_global(self, set_global: SetGlobal):
        result = self.with_indentation(f"(global.set {set_global.name}") + "\n"

        self.indentation += 1
        result += set_global.val.accept(self)
        self.indentation -= 1

        result += self.with_indentation(")") + "\n"

        return result

    def visit_memory(self, memory: Memory):
        result = self.with_indentation("(memory")
        if memory.export:
            result += f' (export "{memory.export}")'
        result += f" {memory.size}"
        result += ")\n"

        return result

    def visit_store(self, store: Store):
        result = self.with_indentation(f"({store.type}.store") + "\n"
        self.indentation += 1
        result += store.location.accept(self)
        result += store.val.accept(self)
        self.indentation -= 1
        result += self.with_indentation(")") + "\n"

        return result

    def visit_load(self, store: Store):
        result = self.with_indentation(f"({store.type}.load") + "\n"
        self.indentation += 1
        result += store.location.accept(self)
        self.indentation -= 1
        result += self.with_indentation(")") + "\n"

        return result

    def with_indentation(self, str):
        return ("    " * self.indentation) + str


def pretty_print(module: Module) -> str:
    return module.accept(WasmPrinter())
